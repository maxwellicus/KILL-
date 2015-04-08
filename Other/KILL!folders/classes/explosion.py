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

class Explosion(pygame.sprite.Sprite):
    damage=3
    
    def __init__(self, x, y,player,score,money,health,enemy,enemies,splatters,explosions):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('explosion.png', -1)
        explosion = load_sound('explosion.wav')
        explosion.play()
        self.rect.centerx, self.rect.centery = x, y
        self.life = 12
        for enemy in enemies:
            if pygame.sprite.collide_rect(self,enemy):
                enemy.hurt(enemy,self.damage,player,score,money,health,enemies,splatters,explosions)
        if pygame.sprite.collide_rect(self,player):
            health.update(-1)

    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()