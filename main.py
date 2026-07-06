import pygame
import math
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

player_img = pygame.image.load("images/player.png")
enemy_img = pygame.image.load("images/enemy.png")
background_img = pygame.image.load("images/background.png")
icon_img = pygame.image.load("images/icon.png")
explosion_img = pygame.image.load(
    "images/explosion.png"
)

explosion_img = pygame.transform.scale(
    explosion_img,
    (80, 80)
)

player_img = pygame.transform.scale(
    player_img,
    (64, 64)
)

enemy_img = pygame.transform.scale(
    enemy_img,
    (50, 50)
)

background_img = pygame.transform.scale(
    background_img,
    (800, 600)
)

icon_img = pygame.transform.scale(
    icon_img,
    (64, 64)
)

laser_sound = pygame.mixer.Sound("sounds/laser.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
explosion_sound.set_volume(1.0)

pygame.mixer.music.load(
    "sounds/background.wav"
)
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

score = 0
high_score = 0
font = pygame.font.Font(None,36)
def is_collision(bullet_x, bullet_y, enemy_x, enemy_y):

    distance = math.sqrt(
        (bullet_x - enemy_x) ** 2 +
        (bullet_y - enemy_y) ** 2
    )

    if distance < 60:
        return True

    return False

def show_score():
    score_text = font.render(
        f"Score: {score} High Score: {high_score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (10, 10))

def game_over():
    text = font.render(
        f"GAME OVER! SCORE: {score}",
        True,
        (255, 0, 0)
    )

    screen.blit(text, (300, 250))

def show_start_screen():
    screen.fill((0, 0, 20))

    title = font.render("SPACE SHOOTER", True, (255,255,255))
    text1 = font.render("Arrow Keys : Move", True, (255,255,255))
    text2 = font.render("Space : Shoot", True, (255,255,255))
    text3 = font.render("Press ENTER to Start", True, (255,255,0))

    screen.blit(title, (250,200))
    screen.blit(text1, (250,280))
    screen.blit(text2, (250,320))
    screen.blit(text3, (220,400))

    pygame.display.update()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(icon_img)

# Player coordinates
player_x = 375
player_y = 450
player_speed = 10

num_enemies = 8

max_enemies = 50

enemy_x = []
enemy_y = []
enemy_speed = []
enemy_direction = []

for i in range(num_enemies):
    enemy_x.append(random.randint(0, 750))
    enemy_y.append(random.randint(50, 150))
    enemy_speed.append(3)
    enemy_direction.append(1)

bullet_x = 0
bullet_y = player_y

bullet_speed = 20
bullet_state = "ready"

explosion_timer = 0
explosion_x = 0
explosion_y = 0

stars = []

for i in range(150):
    stars.append([
        random.randint(0, 800),
        random.randint(0, 600)
    ])


show_start_screen()


waiting = True

while waiting:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False
clock = pygame.time.Clock()
paused = False
running = True


while running:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_SPACE:
                
                if bullet_state == "ready":
                    laser_sound.play()
                    bullet_x = player_x + 20
                    bullet_y = player_y
                    bullet_state = "fire"
                    
    if paused:
        text = font.render("PAUSED", True, (255,255,255))
        screen.blit(text, (320,300))
        pygame.display.update()
        continue
    # Get all keys currently pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < 750:
        player_x += player_speed

    screen.blit(background_img, (0,0))

    for star in stars:
        radius = random.choice([1, 1, 1, 2, 2, 3])

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (star[0], star[1]),
            radius
        )

    screen.blit(
        player_img,
        (player_x, player_y)
    )

    

    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = player_y

    if score > 300:
        bullet_speed = 22

    if score > 500:
        bullet_speed = 25

    else:
        bullet_speed = 20

    if bullet_state == "fire":
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (bullet_x, bullet_y, 5, 20)
        )
        bullet_y -= bullet_speed

    for i in range(num_enemies):

        if score < 50:
            enemy_speed[i] = 3

        elif score < 100:
            enemy_speed[i] = 4

        elif score < 200:
            enemy_speed[i] = 5

        elif score < 300:
            enemy_speed[i] = 6

        elif score < 400:
            enemy_speed[i] = 7

        elif score < 500:
            enemy_speed[i] = 8

        else:
            enemy_speed[i] = 10

        enemy_x[i] += enemy_speed[i] * enemy_direction[i]

        if (
            enemy_x[i] < player_x + 64
            and enemy_x[i] + 50 > player_x
            and enemy_y[i] < player_y + 64
            and enemy_y[i] + 50 > player_y
        ):
            game_over()
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
            break

        if not running:
            continue

        if enemy_x[i] >= 750:
            enemy_direction[i] = -1
            enemy_y[i] += 40

        if enemy_x[i] <= 0:
            enemy_direction[i] = 1
            enemy_y[i] += 40

        screen.blit(
            enemy_img,
            (enemy_x[i], enemy_y[i])
        )

        collision = is_collision(
        bullet_x + 2,
        bullet_y,
        enemy_x[i] + 25,
        enemy_y[i] + 25
        )
        def add_enemy():
            enemy_x.append(random.randint(0, 750))
            enemy_y.append(random.randint(50, 150))
            enemy_speed.append(1)
            enemy_direction.append(1)

        if collision and enemy_y[i] < player_y:
            explosion_x = enemy_x[i]
            explosion_y = enemy_y[i]
            explosion_timer = 15
            explosion_sound.play()

        
            score += 1

            if score in [20, 50, 100, 200, 300, 400, 500]:

               for j in range(5):
                enemy_x.append(random.randint(0, 750))
                enemy_y.append(random.randint(50, 150))
                enemy_speed.append(3)
                enemy_direction.append(1)

               num_enemies += 5

            if score > high_score:
                high_score = score

            if score % 10 == 0 and num_enemies < max_enemies:
                add_enemy()
                num_enemies += 1

            bullet_state = "ready"
            bullet_y = player_y

            enemy_x[i] = random.randint(0, 750)
            enemy_y[i] = random.randint(50,150)
            

        if enemy_y[i] + 50 >= player_y:
            game_over()
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
            break

    if explosion_timer > 0:

        screen.blit(
            explosion_img,
            (explosion_x - 15,
            explosion_y - 15)
        )

        explosion_timer -= 1

   
    show_score()
    clock.tick(60)
    pygame.display.update()

    

pygame.quit()