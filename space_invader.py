import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800,600))

background = pygame.image.load('background.png')

mixer.music.load('background.WAV')
mixer.music.play(-1)


pygame.display.set_caption("space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spacecraft.png')
playerX = 370
playerY = 460
playerX_change = 0

enemyImg = []
enemyX = []
enemyY =[]
enemyX_change = []
enemyY_change = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,739))
    enemyY.append(random.randint(20,150))
    enemyX_change.append(2)
    enemyY_change.append(40)



bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 460
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf',64)



def show_score(x,y):
    score = font.render("score :" + str(score_value), True, (255,255,255))
    screen.blit(score , (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text , (200, 250))
    




def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x , y , i):
    screen.blit(enemyImg[i],(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16 , y+10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
        
    
    


running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.WAV')
                    bullet_sound.play()
                    
                    bulletX = playerX
                    fire_bullet(playerX , bulletY)
                


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    elif playerX >=739:
        playerX = 739


    for i in range(num_of_enemy):

        if enemyY[i] > 420:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break
            
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 739:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.WAV')
            explosion_sound.play()
            bulletY = 460
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,739)
            enemyY[i] = random.randint(20,150)
        enemy(enemyX[i] , enemyY[i] , i)

    if bulletY <=0:
        bulletY = 460
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    
    
    player(playerX,playerY)
    show_score(textX,textY)
    
    pygame.display.update()
