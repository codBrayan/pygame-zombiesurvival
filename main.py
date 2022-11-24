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
# - boolVariants
gaming = True
event_Hit = False
hitSword = False
left = False
right = False
newRound = False

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
lifeZombie = 0

blood = pygame.image.load("files/blood.png")


def hitBox(hit,left,right, playerPosX,playerPosY,listPixelsZombie):
    hitSword = False
    hitSword_in_Left = False
    if left:
        areaHit_X = playerPosX
        areaHit_Y = playerPosY+25
        hitSword_in_Left=True
    elif right:
        areaHit_X = playerPosX+30
        areaHit_Y = playerPosY+25
    if hit:
        pygame.draw.circle(screen,white,(areaHit_X,areaHit_Y),25) # shows a HitBox for user

        pixelsAreaHit_X = list(range(areaHit_X, areaHit_X + 50))
        pixelsAreaHit_Y = list(range(areaHit_Y, areaHit_Y + 25))
        keys = len(listPixelsZombie)

        for zombie in range(0, keys+1):
            pixelsXZombie = list(range(listPixelsZombie[f'{zombie}'][0], listPixelsZombie[f'{zombie}'][0] + widthZombie))
            pixelsYZombie = list(range(listPixelsZombie[f'{zombie}'][1], listPixelsZombie[f'{zombie}'][1] + heightZombie))

            AreaHitX = len(list(set(pixelsAreaHit_X).intersection (set(pixelsXZombie))))
            AreaHitY = len(list(set(pixelsAreaHit_Y).intersection (set(pixelsYZombie))))

            if AreaHitX and AreaHitY > 0:
                hitSword = True
                return hitSword, hitSword_in_Left
            else:
                print("deu ruim")
    

def damage_in_zombie(lifeZombie, leftHit, zombiepos_X, zombiePos_Y):
    if leftHit:
        zombiepos_X -= 10
        zombiePos_Y += 10
        lifeZombie += 1
    else:
        zombiepos_X += 10
        zombiePos_Y += 10
        lifeZombie += 1

    return lifeZombie, zombiepos_X, zombiePos_Y


def spawnZombies(quantZombie):
    dictBoxZombies = {}

    for index in range(0,quantZombie):
        zombiepositionX=(random.randrange(0,250))
        if zombiepositionX > widthZombie:
            zombiepositionX -= widthZombie
        zombiepositionY=(random.randrange(0,300))
        if zombiepositionY > heightPlayer:
            zombiepositionY -= heightPlayer


        screen.blit(imageZombie,(zombiepositionX,zombiepositionY))
        cordintZombie=[zombiepositionX,zombiepositionY]
        dictBoxZombies.update({f'{index}' : cordintZombie})


    return dictBoxZombies 
        


while gaming:
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            os.system("cls")
            print("Jogo encerrado!")
            gaming = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                event_Hit = True
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

        screen.fill(darkBlue) 
        screen.blit(imagePlayerGaming,(playerPositionX,playerPositionY))
        dictZombies_in_Round = spawnZombies(2)

        hitTrue, hitTrueLeft = hitBox(event_Hit, left,right, playerPositionX, playerPositionY, dictZombies_in_Round) #Analising if it hit

        zombiepositionX = (list(dictZombies_in_Round.values))[1]
        zombiepositionY = (list(dictZombies_in_Round.values))[0]

        if zombiepositionX + widthZombie > widthScreen:
            zombiepositionX = widthScreen - widthZombie
        if zombiepositionX < 0:
            zombiepositionX = 0
        if zombiepositionY + heightZombie > heightScreen:
            zombiepositionY = heightScreen - heightZombie
        if zombiepositionY < 0:
            zombiepositionY = 0
        
        

        if hitTrue:
            lifeZombie = damage_in_zombie(lifeZombie,hitTrueLeft, zombiepositionX,zombiepositionY)
        

    event_Hit = False
    pygame.display.update()
    clock.tick(40)
