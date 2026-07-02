import pygame
import math
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

laser_sound = pygame.mixer.Sound("sounds/laser.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
explosion_sound.set_volume(1.0)

pygame.mixer.music.load(
    "sounds/background.wav"
)
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

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

num_enemies = 5

enemy_x = []
enemy_y = []
enemy_speed = []
enemy_direction = []

for i in range(num_enemies):
    enemy_x.append(random.randint(0, 750))
    enemy_y.append(random.randint(50, 150))
    enemy_speed.append(1)
    enemy_direction.append(1)

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
                    laser_sound.play()
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

    for i in range(num_enemies):

        enemy_x[i] += enemy_speed[i] * enemy_direction[i]

        if enemy_y[i] >= player_y:
            game_over()
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

        if not running:
            continue

        if enemy_x[i] >= 750:
            enemy_direction[i] = -1
            enemy_y[i] += 40

        if enemy_x[i] <= 0:
            enemy_direction[i] = 1
            enemy_y[i] += 40

        pygame.draw.rect(
        screen,
        (255, 0, 0),
        (enemy_x[i], enemy_y[i], 50, 50)
        )

    collision = is_collision(
    bullet_x,
    bullet_y,
    enemy_x[i],
    enemy_y[i]
    )

    if collision and enemy_y[i] < player_y:
        explosion_sound.play()
        
        score += 1

        bullet_state = "ready"
        bullet_y = player_y

        enemy_x[i] = random.randint(0, 750)
        enemy_y[i] = random.randint(50,150)
        enemy_speed[i] += 0.01

   
    show_score()

    pygame.display.update()

    

pygame.quit()