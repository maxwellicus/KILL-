#import things
import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

#create paths to other folders
sys.path.insert(0,'functions')

#import functions
from load_image import load_image
from load_sound import load_sound
from findAngle import findAngle
from findDistance import findDistance

class playGameButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('playGameButton.png', 1)
        self.rect.topleft = 10, 390

class exitButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('exitButton.png', 1)
        self.rect.topleft = 220, 390

class mainMenuButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('mainmenuButton.png', 1)
        self.rect.topleft = 10, 390

class upgradeScreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('upgradeScreenButton.png', 1)
        self.rect.topleft = 10, 10

class magicScreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('magicScreenButton.png', 1)
        self.rect.topleft = 220, 10

class weaponScreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('weaponScreenButton.png', 1)
        self.rect.topleft = 430, 10

class backButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('backButton.png', 1)
        self.rect.topleft = 990, 340