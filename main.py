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
round = True
gaming = True
event_Hit = False
hitSword = False
left = False
right = False
hitTrue = False

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




def hitBox(left,right, playerPosX,playerPosY,listCoordsZombie):
    hitSword = False
    hitSword_in_Left = False
    if left:
        areaHit_X = playerPosX
        areaHit_Y = playerPosY+25
        hitSword_in_Left=True
    elif right:
        areaHit_X = playerPosX+30
        areaHit_Y = playerPosY+25
    else:
        areaHit_X = playerPosX+15
        areaHit_Y = playerPosY+10

    pygame.draw.circle(screen,white,(areaHit_X,areaHit_Y),25) # shows a HitBox for user

    pixelsAreaHit_X = list(range(areaHit_X, areaHit_X + 50))
    pixelsAreaHit_Y = list(range(areaHit_Y, areaHit_Y + 25))

    for zombie in listCoordsZombie:
        zombieX = zombie[0]
        zombieY = zombie[1]
        pixelsXZombie = list(range(zombieX, zombieX + widthZombie))
        pixelsYZombie = list(range(zombieY, zombieY + heightZombie))

        AreaHitX = len(list(set(pixelsAreaHit_X) & (set(pixelsXZombie))))
        AreaHitY = len(list(set(pixelsAreaHit_Y) & (set(pixelsYZombie))))

        if AreaHitX and AreaHitY > 0:
            hitSword = True
            return hitSword, hitSword_in_Left



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

    # Spawning corect quantity and making a dictionary with {nomberZombie : coordinates}
    for index in range(0,quantZombie):
        zombiepositionX=(random.randrange(0,250))
        if zombiepositionX > widthZombie:
            zombiepositionX -= widthZombie
        zombiepositionY=(random.randrange(0,300))
        if zombiepositionY > heightPlayer:
            zombiepositionY -= heightPlayer

        cordintZombie=[zombiepositionX,zombiepositionY]
        dictBoxZombies.update({f'{index}' : cordintZombie})
    


    return dictBoxZombies
        


while gaming:

    levelRound = 1

    # Aleatory spawn Zombie
    if round:
        quantZombie = levelRound + 2
        dictZombies_in_Round = spawnZombies((quantZombie))
        print(dictZombies_in_Round)

    while round:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.system("cls")
                print("Jogo encerrado!")
                quit()
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
            
            # Spawn zombies on screen and geting coords
            listCoordZombies = []
            for zombie in dictZombies_in_Round:
                coord = dictZombies_in_Round.get(zombie)
                screen.blit(imageZombie,((coord)[0],(coord)[1]))
                listCoordZombies.append(coord)


            for zombie in listCoordZombies:
                
                zombiepositionX = coord[0]
                zombiepositionY = coord[1]
                if zombiepositionX + widthZombie > widthScreen:
                    zombiepositionX = widthScreen - widthZombie
                if zombiepositionX < 0:
                    zombiepositionX = 0
                if zombiepositionY + heightZombie > heightScreen:
                    zombiepositionY = heightScreen - heightZombie
                if zombiepositionY < 0:
                    zombiepositionY = 0



                '''
                A partir desde ponto é apresentado um erro

                -Qual era o objetivo em construir este jogo:
                 Desenvolver um game que aumentava as quantidades de zombies por round

                -Funções essenciais que ainda precisam ser adicionadas:

                  - Função que deleta os zumbis quando o player mata
                  - Função que faz os zombies irem de atras da posição do player

                Prazo estimado de conclusão: 26/11.
                '''

                # Analysing hit
                if event_Hit:
                    hitTrue, hitTrueLeft = hitBox(left,right, playerPositionX, playerPositionY, listCoordZombies) #Analising if it hit

                if hitTrue:
                    lifeZombie = damage_in_zombie(lifeZombie,hitTrueLeft, zombiepositionX,zombiepositionY)
                
        
            event_Hit = False
            pygame.display.update()
            clock.tick(40)


