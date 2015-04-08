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

class Bullet(pygame.sprite.Sprite):
    penetration = 1
    damage = 1
    speed = 70
    
    def __init__(self, playerx, playery, crossx, crossy, angle,damage):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet.png', -1)
        self.rect.centerx, self.rect.centery = playerx, playery
        self.image = pygame.transform.rotate(self.image, angle)
        self.movex = self.speed*math.cos(angle*math.pi/180)
        self.movey = self.speed*math.sin(angle*math.pi/180)*-1
        self.damage=damage

    def update(self):
        self.rect = self.rect.move(self.movex,self.movey)
        x = self.rect.centerx
        y = self.rect.centery
        if x < 0 or y < 0 or x > 1200 or y > 600:
            self.kill()

    def fire(self,player,bullets,crosshair):
        gunshot = load_sound('gunshot.wav')
        gunshot.play()
        bulletAngle=findAngle(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery)
        if player.numberOfShots==1:
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle,damage))
        elif player.numberOfShots==2:
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+5))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle-5))
        elif player.numberOfShots==3:
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+10))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle-10))
        elif player.numberOfShots==4:
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+5))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle-5))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+15))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle-15))
        elif player.numberOfShots==5:
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+10))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle-10))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+20))
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle-20))
        self.damage=damage

    def collision(self,health):
        ouch = load_sound('ouch.wav')
        self.kill()
        health.update(-self.damage)
        ouch.play()