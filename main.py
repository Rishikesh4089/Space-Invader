import math
import pygame
import os
import sys
import random
from pygame import mixer

# File Locating
def resource_path(relative_path):
    """Get the absolute path to a resource, works for both development and bundled executables."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".") 
    
    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Background
background_image_path = resource_path("assets/background.png")
background = pygame.image.load(background_image_path)

# Background music
background_music = resource_path("sound-effects/background.wav")
mixer.music.load(background_music)
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon_path = resource_path("assets/spaceship.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Player
playerImg_path = resource_path("assets/player1.png")
playerImg = pygame.image.load(playerImg_path)
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5
enemyImg_path = resource_path("assets/enemy.png")

def reset_enemies():
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemyX_change.clear()
    enemyY_change.clear()
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load(enemyImg_path))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(50)

reset_enemies()

# Bullet
bullet_image_path = resource_path("assets/bullet.png")
bulletImg = pygame.image.load(bullet_image_path)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 32)
is_game_over = False

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(restart_text, (240, 320))

def reset_game():
    global playerX, playerX_change, bulletX, bulletY, bullet_state, score_value, is_game_over
    playerX = 370
    playerX_change = 0
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    is_game_over = False
    reset_enemies()

laser_path = resource_path("sound-effects/laser.wav")
explosion_path = resource_path("sound-effects/explosion.wav")
# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if not is_game_over:
                if event.key == pygame.K_LEFT:
                    playerX_change = -6
                if event.key == pygame.K_RIGHT:
                    playerX_change = 6
                if event.key == pygame.K_UP and bullet_state == "ready":
                    bullet_sound = mixer.Sound(laser_path)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            else:
                if event.key == pygame.K_r:
                    reset_game()

        if event.type == pygame.KEYUP and not is_game_over:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    if not is_game_over:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                is_game_over = True
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_Sound = mixer.Sound(explosion_path)
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    if is_game_over:
        game_over()

    pygame.display.update()

