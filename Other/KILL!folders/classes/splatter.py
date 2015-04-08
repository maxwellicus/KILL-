#import things
import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

#create paths to other folders
sys.path.insert(0,'functions')
sys.path.insert(0,'enemies')

#import functions
from load_image import load_image
from load_sound import load_sound
from findAngle import findAngle
from findDistance import findDistance

class Splatter(pygame.sprite.Sprite):
	
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('blood.png', -1)
        self.rect.centerx, self.rect.centery = x, y
        self.life = 12

    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()