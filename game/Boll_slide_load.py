import pygame
def load():
    IMAGES, HITMASKS = {}, {}

    IMAGES['player'] = pygame.image.load('assets/sprites/Boll1.png').convert_alpha()
    IMAGES['platform1'] = pygame.image.load('assets/sprites/platform11.png').convert_alpha()
    IMAGES['platform2'] = pygame.image.load('assets/sprites/platform21.png').convert_alpha()
    IMAGES['stab'] = pygame.image.load('assets/sprites/stab1.png').convert_alpha()
    IMAGES['background'] = pygame.image.load('assets/sprites/background1.jpg').convert()

    HITMASKS['player'] = getHitmask1(IMAGES['player'])
    HITMASKS['platform1'] = getHitmask1(IMAGES['platform1'])
    HITMASKS['platform2'] = getHitmask1(IMAGES['platform2'])
    HITMASKS['stab'] = getHitmask1(IMAGES['stab'])
    return IMAGES, HITMASKS

def getHitmask1(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask
    


