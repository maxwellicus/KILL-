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

class Player(pygame.sprite.Sprite):

	def __init__(self):
	   pygame.sprite.Sprite.__init__(self) #call Sprite initializer
	   self.image, self.rect = load_image('smiley.png', -1)
	   self.rect.centerx, self.rect.centery = 600, 300

	def revert(self):
		self.health = 100
		self.mana = 3
		self.money = 0
		self.score = 0
		self.maxHealth = 100
		self.maxMana = 5
		self.speed = 5
		self.refireRate = 2
		self.numberOfShots = 1
		self.healthRegen = 1
		self.manaRegen = 1
		self.spell = 3
		self.rect.centerx, self.rect.centery = 600, 300

	def update(self, x, y):
		self.rect = self.rect.move((x,y))