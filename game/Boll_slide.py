import Boll_slide_load
import pygame
import random
from sys import exit
from pygame.locals import *

FPS = 60
SCREENWIDTH = 700
SCREENHEIGHT = 700
PLATFORM_SPEED = -4
DOWN_SPEED = 4
ROW_SPEED = 10
pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption('Boll-slode')

IMAGES, HITMASKS = Boll_slide_load.load()
STAB = (-50, -10)
class GameState:
    def __init__(self):
        self.socre = 0
        self.playerx = 350
        self.playery = 230
        self.platform = []
        self.move_x = 0
        self.move_y = 0
        for i in range(5):
            platform = self.Randomplatform()
            platform['y'] -= 140 * (i+1)
            platform['platform'] = 0
            self.platform.append(platform)

    def frame_step(self):
        # Check the crash
        action = self.isCrash()
        # Check the position of the boll
        if self.playery > 700:
            action = 'die'
        # Set the playerx
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.move_x = -ROW_SPEED
                if event.key == K_RIGHT:
                    self.move_x = ROW_SPEED
            elif event.type == KEYUP:
                self.move_x = 0
        if (self.playerx <= -2 or action == 'right') and self.move_x < 0:
            pass
        elif (self.playerx >= 652 or action == 'left') and self.move_x > 0:
            pass
        else:
            self.playerx += self.move_x

        # Set the playery
        if action == 'follow':
            self.move_y = PLATFORM_SPEED
        else:
            self.move_y = DOWN_SPEED
        self.playery += self.move_y

        # Rerange the platform
        for i in range(len(self.platform)):
            self.platform[i]['y'] += PLATFORM_SPEED
        if self.platform[0]['y'] < -35:
            self.platform.pop(0)
        if self.platform[len(self.platform)-1]['y'] < 560:
            self.platform.append(self.Randomplatform())

        # If the boll die, initial it
        if action == 'die':
            self.__init__()

        # Draw the sprites
        SCREEN.blit(IMAGES['background'], (0, 0))
        for i in range(len(self.platform)):
            platformCup = self.platform[i]
            if platformCup['platform'] == 1:
                SCREEN.blit(IMAGES['platform2'],(platformCup['x'], platformCup['y']))
            if platformCup['platform'] == 0:
                SCREEN.blit(IMAGES['platform1'],(platformCup['x'], platformCup['y']))
        SCREEN.blit(IMAGES['player'],(self.playerx, self.playery))
        SCREEN.blit(IMAGES['stab'], (-50,-10))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


    def isCrash(self):
        playerRect = pygame.Rect(self.playerx, self.playery, 50, 50)
        platformRect = []
        platformCrash = []
        platformtag = []
        for i in range(len(self.platform)):
            platformCup = pygame.Rect(self.platform[i]['x'],self.platform[i]['y'], 200,35)
            platformtag.append(self.platform[i]['platform'])
            platformRect.append(platformCup)
        stabRect = pygame.Rect(-50,-10,700,35)
        for i in range(len(platformtag)):
            if platformtag[i] == 1:
                flagCup = pixelCollision(playerRect, platformRect[i], HITMASKS['player'], HITMASKS['platform2'],1)
                platformCrash.append(flagCup)
            else:
                flagCup = pixelCollision(playerRect, platformRect[i], HITMASKS['player'], HITMASKS['platform1'],0)
                platformCrash.append(flagCup)
        flagCup = pixelCollision(playerRect, stabRect, HITMASKS['player'], HITMASKS['stab'], 1)
        platformCrash.append(flagCup)
        flagCup = 'maintain'
        for i in range(len(platformCrash)):
            if platformCrash[i] != 'maintain':
                flagCup = platformCrash[i]
                if flagCup == 'die':
                    return flagCup
        return flagCup

    def Randomplatform(self):
        # Generate a new platform
        platform = {}
        platform['x'] = random.randint(-10,510)
        platform['y'] = 700
        Cup = [x['platform'] for x in self.platform]
        length = len(self.platform)
        if length >= 3 and sum(Cup[length-2:length]) == 2:
            platform['platform'] = 0
        elif random.random() < 0.4:
            platform['platform'] = 1
        else:
            platform['platform'] = 0
        return platform
    
def pixelCollision(rect1, rect2, hitmask1, hitmask2, tag):
    rect = rect1.clip(rect2)
    if rect.width == 0 or rect.height == 0:
        return 'maintain'
    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                if tag == 1:
                    return 'die'
                elif y1+y < 40 and x2+x <100:
                    return 'left'
                elif y1+y < 40 and x2+x > 100:
                    return 'right'
                else:
                    return 'follow'
    return 'maintain'

            

    




