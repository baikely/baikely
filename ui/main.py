import pygame

def run():
    # Set up
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))

    # Set background
    screen.fill((255, 255, 255))

    # Draw bike
    bike = pygame.image.load("ui/bike.png")
    bike = pygame.transform.scale(bike, (125, 125))
    screen.blit(bike, (330, 150))

    # Draw car
    car = pygame.image.load("ui/car.png")
    car = pygame.transform.scale(car, (50, 50))
    screen.blit(car, (370, 400))

    # Main loop
    running = True
    while running:
        pygame.display.flip() # Update display
        clock.tick(60) # Use 60 FPS