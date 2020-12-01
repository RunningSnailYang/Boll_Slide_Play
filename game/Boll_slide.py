import Boll_slide_load
import pygame
import random
from sys import exit
from pygame.locals import *

FPS = 60 # Set the frequency of the loop
SCREENWIDTH = 700 # Set the width of the screen
SCREENHEIGHT = 700 # Set the height of the screen
PLATFORM_SPEED = -4 # Set the speed of the platforms' upward movement
DOWN_SPEED = 4 # Set the speed of the boll's downward movement
ROW_SPEED = 10 # Set the speed of the boll's lateral movement
pygame.init() # Initialize the game
# Create the clock, which is used to control the loop frequency of the game
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption('Boll-slide')

# IMAGES: Dict of the objects' images
# HITMASKS: Dict of the objects' hitmasks, \
# the hitmask is a list of lists. shape: [width, height], type: bool
IMAGES, HITMASKS = Boll_slide_load.load()
STAB = (-50, -10)
class GameState:
    # Create game class
    def __init__(self):
        self.socre = 0
        self.playerx = 350 # Set initial x-value of the boll
        self.playery = 230 # Set initial y-value of the boll
        self.platform = [] # A queue used to store the current platforms on the screen
        self.move_x = 0 # The speed of movement on x-coordinate
        self.move_y = 0 # The speed of movement on y-coordinate
        # Initialize 5 random safe platforms on the screen
        for i in range(5):
            platform = self.Randomplatform() # Generate a platform on the top randomly
            platform['y'] -= 140 * (i+1) # Adjust the y-value of the platform
            platform['platform'] = 0 # Make the platform safe
            self.platform.append(platform) # Add the platform in the platform queue

    def frame_step(self): # Core of running of a game
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
        # Lateral movement of the boll (Change self.playerx)
        if (self.playerx <= -2 or action == 'right') and self.move_x < 0:
            pass
        elif (self.playerx >= 652 or action == 'left') and self.move_x > 0:
            pass
        else:
            self.playerx += self.move_x

        # Longitudinal movement of the boll (Change self.playery)
        if action == 'follow':
            self.move_y = PLATFORM_SPEED
        else:
            self.move_y = DOWN_SPEED
        self.playery += self.move_y

        # Rerange the platforms
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
        pygame.display.update() # Update the display of the screen
        # Set the frequency of the loop, which should be written in the loop
        FPSCLOCK.tick(FPS)


    def isCrash(self):
        # pygame.Rect(left, top, width, height)
        playerRect = pygame.Rect(self.playerx, self.playery, 50, 50) # Rect of Boll
        platformRect = [] # Rects of platforms
        platformCrash = []
        platformtag = [] # Types of platforms
        for i in range(len(self.platform)):
            # Rect of the platform
            platformCup = pygame.Rect(self.platform[i]['x'],self.platform[i]['y'], 200,35)
            platformtag.append(self.platform[i]['platform']) # Type of the platform
            platformRect.append(platformCup)
        stabRect = pygame.Rect(-50,-10,700,35) # Rect of the top stabs
        for i in range(len(platformtag)):
            # flagCup can be 'maintain', 'die', 'left', 'right', 'follow'
            if platformtag[i] == 1: # The platform is dangerous
                flagCup = pixelCollision(playerRect, platformRect[i], HITMASKS['player'], HITMASKS['platform2'],1)
                platformCrash.append(flagCup)
            else: # The platform is safe
                flagCup = pixelCollision(playerRect, platformRect[i], HITMASKS['player'], HITMASKS['platform1'],0)
                platformCrash.append(flagCup)
        # Check the collision between the boll and the top stabs
        flagCup = pixelCollision(playerRect, stabRect, HITMASKS['player'], HITMASKS['stab'], 1)
        platformCrash.append(flagCup)
        flagCup = 'maintain'
        for i in range(len(platformCrash)):
            if platformCrash[i] != 'maintain':
                flagCup = platformCrash[i]
                if flagCup == 'die':
                    return flagCup
        # flagCup can be 'maintain', 'die', 'left', 'right', 'follow', \
        # which is used to indicate the type of movement of the boll
        return flagCup

    def Randomplatform(self):
        # Generate a new platform
        platform = {}
        # platform: dict. keys: 'x', 'y', 'platform'
        # 'x': The x-value of the platform
        # 'y': The y-value of the platform
        # 'platform': The type of the platform. 0: safe, 1: dangerous
        platform['x'] = random.randint(-10,510)
        platform['y'] = 700
        Cup = [x['platform'] for x in self.platform]
        length = len(self.platform) # The number of the current platforms
        if length >= 3 and sum(Cup[length-2:length]) == 2:
        # sum(Cup[length-2:length]): The number of the dangerous platforms \
        # in the last two platforms
            platform['platform'] = 0
        elif random.random() < 0.4:
            platform['platform'] = 1
        else:
            platform['platform'] = 0
        return platform
    
def pixelCollision(rect1, rect2, hitmask1, hitmask2, tag):
    # rect1, rect2: The rects of two objects. Type: pygame.Rect
    # hitmask1, hitmask2: Hitmasks of two objects. Type: List of lists of bools
    # tag: If the hit is dangerous
    rect = rect1.clip(rect2) # The intersected rect of rect1 and rect2
    if rect.width == 0 or rect.height == 0: # No intersection between the two rects
        return 'maintain'
    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y
    # Check if there is intersection between the two objects (Not Rect)
    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                if tag == 1:
                    return 'die'
                elif y1+y < 40 and x2+x < 100:
                    return 'left' # The boll can only move to the left
                elif y1+y < 40 and x2+x > 100:
                    return 'right' # The boll can only move to the right
                else:
                    return 'follow' # The boll is supposed to move with the platform
    return 'maintain'

            

    





