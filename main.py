import pygame
import os
import random
from functions import *


try:
    pygame.init()
    os.system("cls")
    print("Inicialização do game com sucesso!")
except:
    print("Ocorreu um erro ao tentar iniciar o game")



#ASSETS
gaming = True
notDied = True
hitBox = False
hitSword = False
left = False
right = False
# - layout screen
heightScreen = 250
widthScreen = 300
clock = pygame.time.Clock()
screen = pygame.display.set_mode((widthScreen,heightScreen))
pygame.display.set_caption("Game survival 1")

# - colors
white = (255, 255, 255)
black = (0, 0, 0)
darkBlue = (0, 1, 18)

# - player
imagePLayer_right = pygame.image.load("files/player_rightMove.png")
imagePlayer_left = pygame.image.load("files/player_leftMove.png")
imagePlayerGaming = imagePlayer_left
playerPositionX = 50
playerPositionY = 50
playerMovementX = 0
playerMovementY = 0
speed_displacmt = 4 
heightPlayer = 35
widthPlayer = 25

# - zombies
imageZombie = pygame.image.load("files/zombie.png")
widthZombie = 30
heightZombie = 40
zombiepositionX=(random.randrange(0,250)-widthZombie)
zombiepositionY=(random.randrange(0,300)-heightZombie)
zombiePosition = (zombiepositionX,zombiepositionY)


def damageArea(hit,left,right, playerPosX,playerPosY):
    hitSword = False
    hitSwordLeft = False

    if left:
        areaHit_X = playerPosX
        areaHit_Y = playerPosY+25
    if right:
        areaHit_X = playerPosX+30
        areaHit_Y = playerPosY+25
        hitSwordLeft=True

    if hit:
        pygame.draw.circle(screen,white,(areaHit_X,areaHit_Y),25)

        pixelsAreaHit_X = list(range(areaHit_X, areaHit_X + 50))
        pixelsAreaHit_Y = list(range(areaHit_Y, areaHit_Y + 25))
        pixelsXZombie = list(range(zombiepositionX, zombiepositionX + widthZombie))
        pixelsYZombie = list(range(zombiepositionY, zombiepositionY + heightZombie))

        AreaHitX = len(list(set(pixelsAreaHit_X) & set(pixelsXZombie)))
        AreaHitY = len(list(set(pixelsAreaHit_Y) & set(pixelsYZombie)))

        if AreaHitX and AreaHitY > 0:
            hitSword = True
    
    return hitSword, hitSwordLeft
    

def hit_in_zombie(lifeZombie,leftHit, zombiepos_X, zombiePos_Y):
    if lifeZombie < 2:
        if leftHit:
            zombiepos_X += 10
            zombiePos_Y += 10
        else:
            zombiepos_X -= 10
            zombiePos_Y += 10

    return zombiepos_X, zombiePos_Y
    


while gaming:
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            os.system("cls")
            print("Jogo encerrado!")
            gaming = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hitBox = True
            elif event.key == pygame.K_w:
                playerMovementY = speed_displacmt * -1
            elif event.key == pygame.K_s:
                playerMovementY = speed_displacmt
            elif event.key == pygame.K_a:
                imagePlayerGaming = imagePlayer_left 
                playerMovementX = speed_displacmt * -1
                left=True
                right=False
            elif event.key == pygame.K_d:
                imagePlayerGaming = imagePLayer_right
                playerMovementX = speed_displacmt
                right = True
                left = False
        elif event.type == pygame.KEYUP:
                playerMovementX = 0
                playerMovementY = 0
                
    if gaming:
        #Assets of player on screen
        if playerPositionX + playerMovementX + widthPlayer < widthScreen and playerPositionX + playerMovementX > 0:
            playerPositionX = playerPositionX + playerMovementX
        if playerPositionY + playerMovementY + heightPlayer < heightScreen and playerPositionY + playerMovementY > 0:
            playerPositionY = playerPositionY + playerMovementY
        
        if zombiepositionX + widthZombie < widthScreen and zombiepositionX > 0:
            zombiepositionX = zombiepositionX
        else:
            zombiepositionX = widthScreen - widthZombie
        if zombiepositionY + heightZombie <= heightScreen and zombiepositionY >= 0:
            zombiepositionY = zombiepositionY
        else:
            zombiepositionY = heightScreen - heightZombie

        
        screen.fill(darkBlue) 
        hitSword, hitSwordLeft = damageArea(hitBox, left,right, playerPositionX, playerPositionY)
        screen.blit(imagePlayerGaming,(playerPositionX,playerPositionY))
        screen.blit(imageZombie,(zombiepositionX,zombiepositionY))

        if hitSword:
            zombiepositionX, zombiepositionY =  hit_in_zombie(1,hitSwordLeft, zombiepositionX,zombiepositionY)


    hitSword = False
    hitBox = False
    pygame.display.update()
    clock.tick(40)
