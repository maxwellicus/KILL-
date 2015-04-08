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

class Mana(pygame.sprite.Sprite):
	
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.mana=3
        self.maxmana=3

    def update(self,change):
        self.owner.mana+=change

    def show(self):
        self.font = pygame.font.Font(None, 40)
        msg = "Mana: %d/%d" % (self.owner.mana,self.owner.maxMana)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(1000, 570)

    def post(self):
        self.font = pygame.font.Font(None, 100)
        msg = "Mana: %d/%d" % (self.owner.mana, self.owner.maxMana)
        self.rect = self.image.get_rect().move(600, 500)
        self.image = self.font.render(msg, 0, self.color)