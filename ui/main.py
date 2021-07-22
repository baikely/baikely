import pygame

def run():
    # Set up
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))

    # Set background
    screen.fill((255, 255, 255))

    # Draw text
    font = pygame.font.SysFont("Helvetica", 24)
    text_surface = font.render("HERE'S A WINDOW", False, (0, 0, 0))
    screen.blit(text_surface, (100, 100))
    text_surface = font.render("I FEEL TIRED", False, (0, 255, 255))
    screen.blit(text_surface, (100, 300))

    car = pygame.image.load("ui/car.png")
    car = pygame.transform.scale(car, (50, 50))
    screen.blit(car, (100, 124))

    # Main loop
    running = True
    while running:
        pygame.display.flip() # Update display
        clock.tick(60) # Use 60 FPS