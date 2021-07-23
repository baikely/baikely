from queue import Empty
import pygame
from multiprocessing import Queue
import math
from ui.ultrasonic import UltrasonicSensor
from typing import List

# Load images
bike = pygame.image.load("ui/bike.png")
bike = pygame.transform.scale(bike, (75, 75))
car = pygame.image.load("ui/car.png")
car = pygame.transform.scale(car, (29, 64))

# Handles an event passed in from another of the processes.
def handle_event(event: dict):
    if event["type"] == "test":
        pass

def draw_ultrasonic(screen: pygame.Surface, font: pygame.font.Font, distance: float, start_angle: float, end_angle: float):
    surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    center_x = 237
    center_y = 137
    radius = 20 + (distance * 100 // 6)
    mid_angle = (start_angle + end_angle) / 2
    pygame.draw.arc(
        surface,
        (255, 0, 0, 100),
        [center_x - radius, center_y - radius, radius * 2, radius * 2],
        math.radians(start_angle),
        math.radians(end_angle),
        radius
    )
    text = font.render(f"{math.floor(distance * 100)} cm", True, (0, 0, 0))
    text_x = center_x + math.cos(math.radians(mid_angle)) * (radius + 6)
    text_y = center_y - math.sin(math.radians(mid_angle)) * (radius + 6)
    if mid_angle < 240:
        text_x -= text.get_width()
    elif mid_angle < 300:
        text_x -= text.get_width() / 2
    screen.blit(surface, (0, 0))
    screen.blit(text, (text_x, text_y))

# Draws the UI.
def draw(screen: pygame.Surface, font: pygame.font.Font, sensors: List[UltrasonicSensor]):
    screen.fill((255, 255, 255))
    screen.blit(bike, (200, 100))
    screen.blit(car, (225, 250))
    for sensor in sensors:
        distance = sensor.distance()
        if distance is not None:
            draw_ultrasonic(screen, font, distance, sensor.start_angle, sensor.end_angle)

# Creates the window and updates it continually.
def run(queue: Queue, sensors: List[UltrasonicSensor]):
    # Set up
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("Baike")
    pygame.font.init()
    screen = pygame.display.set_mode((480, 320))
    font = pygame.font.SysFont("Helvetica", 18)
    
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
        
        pygame.display.flip() # Update display
        clock.tick(60) # Use 60 FPS
