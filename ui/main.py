from queue import Empty
from ui.alert import Alert
import pygame
from multiprocessing import Queue
import math
from ui.ultrasonic import UltrasonicSensor
from ui.mode import Mode
from typing import List, Tuple
import os
import subprocess

URBAN_THRESHOLD = 0.5
SUBURBAN_THRESHOLD = 2

# Load images
bg = pygame.image.load("ui/bg2.jpeg")
bike = pygame.image.load("ui/bike-teal.png")
bike = pygame.transform.scale(bike, (72, 128))
bike_detected = pygame.image.load("ui/bike-red.png")
bike_detected = pygame.transform.scale(bike_detected, (54, 96))
car = pygame.image.load("ui/car.png")
car = pygame.transform.scale(car, (29, 64))

car_on_left = False
car_on_right = False
bike_on_left = False
bike_on_right = False
mode = Mode.SUBURBAN

# Handles an event passed in from another of the processes.
def handle_event(event: dict):
    global car_on_left
    global car_on_right
    global bike_on_left
    global bike_on_right
    if event["type"] == "cv":
        car_on_left = False
        car_on_right = False
        bike_on_left = False
        bike_on_right = False
        for detection in event["detections"]:
            if detection["object"] == "car":
                if detection["position"] == "left":
                    car_on_left = True
                else:
                    car_on_right = True
            elif detection["object"] == "bicycle":
                if detection["position"] == "left":
                    bike_on_left = True
                else:
                    bike_on_right = True

def draw_ultrasonic(screen: pygame.Surface, font: pygame.font.Font, center: Tuple[int, int], distance: float, start_angle: float, end_angle: float):
    surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    radius = int(30 + distance * 100 / 5)
    mid_angle = (start_angle + end_angle) / 2
    pygame.draw.arc(
        surface,
        (255, max(0, min(255, int((distance - 0.5) / 4 * 255))), 0, 160),
        [center[0] - radius, center[1] - radius, radius * 2, radius * 2],
        math.radians(start_angle),
        math.radians(end_angle),
        radius
    )
    text = font.render(f"{math.floor(distance * 100)} cm", True, (255, 255, 255))
    text_x = center[0] + math.cos(math.radians(mid_angle)) * (radius + 6)
    text_y = center[1] - math.sin(math.radians(mid_angle)) * (radius + 6)
    if mid_angle < 240:
        text_x -= text.get_width()
    elif mid_angle < 300:
        text_x -= text.get_width() / 2
    screen.blit(surface, (0, 0))
    screen.blit(text, (text_x, text_y))

# Draws the UI.
def draw(screen: pygame.Surface, font: pygame.font.Font, sensors: List[UltrasonicSensor]):
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, -10))
    center = (screen.get_width() // 2, screen.get_height() // 2 - 50)
    screen.blit(bike, (center[0] - bike.get_width() // 2, center[1] - bike.get_height() // 2))
    if car_on_left:
        screen.blit(car, (screen.get_width() / 2 - 50 - car.get_width() / 2, 225))
    if car_on_right:
        screen.blit(car, (screen.get_width() / 2 + 50 - car.get_width() / 2, 225))
    if bike_on_left:
        screen.blit(bike_detected, (screen.get_width() / 2 - 100 - bike_detected.get_width() / 2, 209))
    if bike_on_right:
        screen.blit(bike_detected, (screen.get_width() / 2 + 100 - bike_detected.get_width() / 2, 209))
    for sensor in sensors:
        distance = sensor.distance()
        if distance is not None:
            draw_ultrasonic(screen, font, center, distance, sensor.start_angle, sensor.end_angle)



# Creates the window and updates it continually.
# Also sounds alerts when needed.
def run(queue: Queue, sensors: List[UltrasonicSensor]):
    # Set up
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("Baike")
    pygame.font.init()
    pygame.mixer.init()
    beep = pygame.mixer.Sound("ui/beep.mp3")
    screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    font = pygame.font.SysFont("Helvetica", 18)
    
    global play_vehicle_alert
    play_vehicle_alert = False
    def on_vehicle_alert():
        global play_vehicle_alert
        play_vehicle_alert = True

    distance_alert = Alert(beep.play, debounce_time=0.5)
    car_left_alert = Alert(on_vehicle_alert, debounce_time=5)
    car_right_alert = Alert(on_vehicle_alert, debounce_time=5)
    bike_left_alert = Alert(on_vehicle_alert, debounce_time=5)
    bike_right_alert = Alert(on_vehicle_alert, debounce_time=5)
    
    # Main loop
    running = True
    while running:
        # Read any Pygame events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Read any incoming events from the shared queue.
        while True:
            try:
                handle_event(queue.get_nowait())
            except Empty:
                break

        # Perform any UI updates here.
        draw(screen, font, sensors)
        threshold = URBAN_THRESHOLD if mode == Mode.URBAN else SUBURBAN_THRESHOLD
        if os.getenv("BEEPBEEPBEEP") or any(sensor.distance <= threshold for sensor in sensors):
            distance_alert.set()
            distance_alert.reset()
        car_left_alert.update(car_on_left)
        car_right_alert.update(car_on_right)
        bike_left_alert.update(bike_on_left)
        bike_right_alert.update(bike_on_right)
        if play_vehicle_alert:
            statement = ""
            if car_on_left and car_on_right:
                statement += "Cars on both sides. "
            elif car_on_left:
                statement += "Car on left. "
            elif car_on_right:
                statement += "Car on right. "
            if bike_on_left and bike_on_right:
                statement += "Bikes on both sides. "
            elif bike_on_left:
                statement += "Bike on left. "
            elif bike_on_right:
                statement += "Bike on right. "
            if len(statement) > 0:
                subprocess.Popen(["espeak", statement])
            play_vehicle_alert = False
        
        pygame.display.flip() # Update display
        clock.tick(60) # Use 60 FPS
