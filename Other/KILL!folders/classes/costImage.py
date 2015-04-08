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

class costImage(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
    def costDisplay(self, cost, level):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.update(0)
        if level==4:
            self.msg = "Complete"
        else:
            self.msg = "Cost: %d" % cost
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(self.x, self.y)