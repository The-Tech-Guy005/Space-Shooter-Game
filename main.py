import pygame

# Start all pygame modules
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption("Space Shooter")

# Game loop variable
running = True

while running:

    # Check all events
    for event in pygame.event.get():

        # If user clicks the close button
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with dark blue color
    screen.fill((0, 0, 50))
    pygame.draw.rect(screen, (255,255,255), (375,500, 50, 50))

    # Update the screen
    pygame.display.update()

# Close pygame properly
pygame.quit()