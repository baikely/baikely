import pygame

def run():
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
        pygame.display.flip() # Update display
        clock.tick(60) # Use 60 FPS