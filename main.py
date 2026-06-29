import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")

# Player coordinates
player_x = 375
player_y = 450
player_speed = 10

bullet_x = 0
bullet_y = player_y

bullet_speed = 25
bullet_state = "ready"

running = True

while running:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                if bullet_state == "ready":
                    bullet_x = player_x + 20
                    bullet_y = player_y
                    bullet_state = "fire"
                    

    # Get all keys currently pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < 750:
        player_x += player_speed

    screen.fill((0, 0, 50))

    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (player_x, player_y, 50, 50)
    )
    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = player_y

    if bullet_state == "fire":
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (bullet_x, bullet_y, 5, 20)
        )

        bullet_y -= bullet_speed

    pygame.display.update()

    

pygame.quit()