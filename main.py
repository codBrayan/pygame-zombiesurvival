import pygame
import os
import random

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
hitTrueLeft = False

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
lifeZombie = 5

blood = pygame.image.load("files/blood.png")




def hitBox(left,right, playerPosX,playerPosY,CoordsZombie):
    hitSword = False
    hitSword_in_Left = False
    areaHit_X = playerPosX-5
    areaHit_Y = playerPosY
    areaDrawCircleX = playerPosX 
    areaDrawCircleY = playerPosY

    if left:
        areaHit_X = playerPosX-20
        areaHit_Y = playerPosY
        areaDrawCircleY +=20
        hitSword_in_Left=True
    if right:
        areaHit_X = playerPosX+5
        areaHit_Y = playerPosY
        areaDrawCircleX +=25
        areaDrawCircleY +=20

    pygame.draw.circle(screen,white,(areaDrawCircleX,areaDrawCircleY),22) # shows a HitBox for user
    #pygame.draw.rect(screen, white, (areaHit_X, areaHit_Y, 40, 40)) # HITBOX

    pixelsAreaHit_X = list(range(areaHit_X, areaHit_X + 50))
    pixelsAreaHit_Y = list(range(areaHit_Y, areaHit_Y + 25))


    for zombie in CoordsZombie:
        coords=CoordsZombie.get(zombie)
        zombieX = coords[0]
        zombieY = coords[1]
        pixelsXZombie = list(range(zombieX, zombieX + widthZombie))
        pixelsYZombie = list(range(zombieY, zombieY + heightZombie))

        AreaHitX = len(list(set(pixelsAreaHit_X) & (set(pixelsXZombie))))
        AreaHitY = len(list(set(pixelsAreaHit_Y) & (set(pixelsYZombie))))

        if AreaHitX and AreaHitY > 0:
            hitSword = True
            return hitSword, hitSword_in_Left, coords, zombie

    zombie = [0, 0]
    return hitSword, hitSword_in_Left, zombie,  zombie


def spawnPlayer(posX, posY):
    screen.blit(imagePlayerGaming,(posX,posY))  

def damage_in_zombie(leftHit, zombieHit):
    if leftHit:
        zombieHit[0] -= 10
        zombieHit[1] += 10
    else:
        zombieHit[0] += 10
        zombieHit[1] += 10

def spawnZombies(quantZombie):
    dictBoxZombies = {}
    dictLifeZombies = {}

    # Spawning corect quantity and making a dictionary with {numberZombie : coordinates}
    for index in range(0,quantZombie):
        zombiepositionX=(random.randrange(0,250))
        if zombiepositionX > widthZombie:
            zombiepositionX -= widthZombie
        zombiepositionY=(random.randrange(0,300))
        if zombiepositionY > heightPlayer:
            zombiepositionY -= heightPlayer

        cordintZombie=[zombiepositionX,zombiepositionY]
        dictBoxZombies.update({f'{index}' : cordintZombie})
    # Creating a dict with their respective lifes
    for zombie in dictBoxZombies:
        dictLifeZombies.update({f'{zombie}' : lifeZombie})
    return dictBoxZombies, dictLifeZombies
        


while gaming:
    levelRound = 1

    # create a aleatory spawn Zombie
    if round:
        quantZombie = levelRound + 2
        dictZombies_in_Round, dictLife_Zombies = spawnZombies((quantZombie))

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
 
        #Assets of player on screen
        if playerPositionX + playerMovementX + widthPlayer < widthScreen and playerPositionX + playerMovementX > 0:
            playerPositionX = playerPositionX + playerMovementX
        if playerPositionY + playerMovementY + heightPlayer < heightScreen and playerPositionY + playerMovementY > 0:
            playerPositionY = playerPositionY + playerMovementY

        screen.fill(darkBlue) 
        spawnPlayer(playerPositionX, playerPositionY)

        #Assets of zombies on screen / Verify lifes / Create list of coords
        for zombie in dictZombies_in_Round:
            coord = dictZombies_in_Round.get(zombie)
            life = (dictLife_Zombies.get(zombie))
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

            if life > 0:
                screen.blit(imageZombie,(zombiepositionX,zombiepositionY))

        # Analysing hit
        if event_Hit:
            hitTrue, hitTrueLeft, CoordZombieHitd , numberZombieHitd = hitBox(left,right, playerPositionX, playerPositionY, dictZombies_in_Round) #Analising if it hit
            
            if hitTrue:
                lifeZombie = dictLife_Zombies.get(numberZombieHitd)
                damage_in_zombie(hitTrueLeft, CoordZombieHitd)
                dictLife_Zombies.update({f'{numberZombieHitd}':lifeZombie-1})


        event_Hit = False
        pygame.display.update()
        clock.tick(40)
