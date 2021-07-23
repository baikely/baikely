from queue import Empty
import pygame
from multiprocessing import Queue

# Handles an event passed in from another of the processes.
def handle_event(event: dict):
    if event["type"] == "test":
        print(event["test"])

# Creates the window and updates it continually.
def run(queue: Queue):
    # Set up
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("Baike")
    pygame.font.init()
    screen = pygame.display.set_mode((480, 320))

    # Set background
    screen.fill((255, 255, 255))

    # Draw bike
    bike = pygame.image.load("ui/bike.png")
    bike = pygame.transform.scale(bike, (75, 75))
    screen.blit(bike, (200, 100))

    # Draw car
    car = pygame.image.load("ui/car.png")
    car = pygame.transform.scale(car, (25, 25))
    screen.blit(car, (225, 200))

    # Main loop
    running = True
    while running:
        # Read any incoming events from the shared queue.
        while True:
            try:
                handle_event(queue.get_nowait())
            except Empty:
                break

        # Perform any UI updates here.

        pygame.display.flip() # Update display
        clock.tick(60) # Use 60 FPS