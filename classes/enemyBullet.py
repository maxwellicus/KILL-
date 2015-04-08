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

class EnemyBullet(pygame.sprite.Sprite):
    penetration = 1
    damage = 1
    speed = 15
    
    def __init__(self, turretx, turrety, playerx, playery, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet.png', -1)
        self.rect.centerx, self.rect.centery = turretx, turrety
        self.image = pygame.transform.rotate(self.image, angle)
        self.movex = self.speed*math.cos(angle*math.pi/180)
        self.movey = self.speed*math.sin(angle*math.pi/180)*-1

    def update(self):
        self.rect = self.rect.move(self.movex,self.movey)
        x = self.rect.centerx
        y = self.rect.centery
        if x < 0 or y < 0 or x > 1200 or y > 600:
            self.kill()

    def collision(self,health):
        ouch = load_sound('ouch.wav')
        self.kill()
        health.update(-1)
        ouch.play()