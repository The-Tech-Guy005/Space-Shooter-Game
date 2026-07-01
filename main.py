import pygame
import math
import random

pygame.init()
score = 0
font = pygame.font.Font(None,36)
def is_collision(bullet_x, bullet_y, enemy_x, enemy_y):

    distance = math.sqrt(
        (bullet_x - enemy_x) ** 2 +
        (bullet_y - enemy_y) ** 2
    )

    if distance < 20:
        return True

    return False

def show_score():
    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (10, 10))

def game_over():
    text = font.render(
        "GAME OVER",
        True,
        (255, 0, 0)
    )

    screen.blit(text, (300, 250))

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")

# Player coordinates
player_x = 375
player_y = 450
player_speed = 10

enemy_x = 350
enemy_y = 50

enemy_speed = 1
enemy_direction = 1

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

    enemy_x += enemy_speed * enemy_direction

    if enemy_y >= player_y:
        game_over()
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    if not running:
        continue

    if enemy_x >= 750:
        enemy_direction = -1
        enemy_y += 40

    if enemy_x <= 0:
        enemy_direction = 1
        enemy_y += 40

    collision = is_collision(
    bullet_x,
    bullet_y,
    enemy_x,
    enemy_y
    )

    if collision and enemy_y < player_y:

        score += 1

        bullet_state = "ready"
        bullet_y = player_y

        enemy_x = random.randint(0, 750)
        enemy_y = 50
        enemy_speed += 0.1

    pygame.draw.rect(
    screen,
    (255, 0, 0),
    (enemy_x, enemy_y, 50, 50)
    )
    show_score()

    pygame.display.update()

    

pygame.quit()