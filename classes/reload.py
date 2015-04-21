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

class Reload(pygame.sprite.Sprite):

    timer=-1
	
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('black')

    def show(self,reloadTimer):
        self.font = pygame.font.Font(None, 40)
        msg = "Reload: %d" % (reloadTimer)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 540)