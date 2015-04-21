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
from costImage import costImage

class Upgrade(pygame.sprite.Sprite):
    """ super class for all upgrades """
    level = 0
    pictures = []
    
    def __init__(self, owner, costsGroup):
        pygame.sprite.Sprite.__init__(self)
        self.costsGroup = costsGroup
        self.owner = owner

    def show(self):
        self.image, self.rect = load_image(self.pictures[self.level], 1)
        self.rect.topleft = 10, 40
        self.costSprite.costDisplay(self.price, self.level)
        
class maxHealthUpgrade(Upgrade):
    """ increase max health """
    pictures = ['maxHealth0.png', 'maxHealth1.png', 
                'maxHealth2.png', 'maxHealth3.png', 
                'maxHealth4.png']
    price=10
    
    def __init__(self, owner, costsGroup):
        super(maxHealthUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(10, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def revert(self):
        self.level=0
        self.price=10
        self.show()
        self.rect.topleft = 10, 40

    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.health += 25
                self.owner.maxHealth += 25
                self.rect.topleft = 10, 40
        except StopIteration:
            return

    def costDisplay(self):
        super(maxHealthUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(500, 500)

        
class refireRateUpgrade(Upgrade):
    pictures = ['refireRate0.png', 'refireRate1.png',
                'refireRate2.png', 'refireRate3.png',
                'refireRate4.png']
    price=10
                
    def __init__(self, owner, costsGroup):
        super(refireRateUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(220, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 220, 40

    def revert(self):
        self.level=0
        self.price=10
        self.show()
        self.rect.topleft = 220, 40
    
    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.refireRate += 1
                self.rect.topleft = 220, 40
        except StopIteration:
                return
            
    def costDisplay(self):
        super(refireRateUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(600, 600)


class movementSpeedUpgrade(Upgrade):
    """ increase max health """
    pictures = ['movementSpeed0.png', 'movementSpeed1.png', 
                'movementSpeed2.png', 'movementSpeed3.png', 
                'movementSpeed4.png']
    price=5
    
    def __init__(self, owner, costsGroup):
        super(movementSpeedUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(430, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 430, 40

    def revert(self):
        self.level=0
        self.price=5
        self.show()
        self.rect.topleft = 430, 40
        
    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.speed += 1
                self.rect.topleft = 430, 40
        except StopIteration:
            return

    def costDisplay(self):
        super(movementSpeedUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(500, 500)

class numberOfShotsUpgrade(Upgrade):
    pictures = ['numberOfBullets0.png', 'numberOfBullets1.png', 
                'numberOfBullets2.png', 'numberOfBullets3.png', 
                'numberOfBullets4.png']
    price=20
    
    def __init__(self, owner, costsGroup):
        super(numberOfShotsUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(640, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 640, 40

    def revert(self):
        self.level=0
        self.price=20
        self.show()
        self.rect.topleft = 640, 40
        
    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.numberOfShots += 1
                self.rect.topleft = 640, 40
        except StopIteration:
            return

    def costDisplay(self):
        super(numberOfShotsUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(500, 500)
             
class healthRegenUpgrade(Upgrade):
    pictures = ['healthRegen0.png', 'healthRegen1.png', 
                'healthRegen2.png', 'healthRegen3.png', 
                'healthRegen4.png']
    price=5
    
    def __init__(self, owner, costsGroup):
        super(healthRegenUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(850, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 850, 40

    def revert(self):
        self.level=0
        self.price=5
        self.show()
        self.rect.topleft = 850, 40
        
    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.healthRegen = self.owner.healthRegen / 2
                self.rect.topleft = 850, 40
        except StopIteration:
            return

    def costDisplay(self):
        super(healthRegenUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(500, 500)

class maxManaUpgrade(Upgrade):
    """ increase max health """
    pictures = ['maxMana0.png', 'maxMana1.png', 
                'maxMana2.png', 'maxMana3.png', 
                'maxMana4.png']
    price=10

    def __init__(self, owner, costsGroup):
        super(maxManaUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(220, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 220, 340
        
    def revert(self):
        self.level=0
        self.price=10
        self.show()
        self.rect.topleft = 220, 340

    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.mana += 1
                self.owner.maxMana += 1
                self.rect.topleft = 220, 340
        except StopIteration:
            return

    def costDisplay(self):
        super(maxManaUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(500, 500)

class manaRegenUpgrade(Upgrade):
    pictures = ['manaRegen0.png', 'manaRegen1.png', 
                'manaRegen2.png', 'manaRegen3.png', 
                'manaRegen4.png']
    price=5
    
    def __init__(self, owner, costsGroup):
        super(manaRegenUpgrade, self).__init__(owner, costsGroup)
        self.costSprite = costImage(430, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 430, 340

    def revert(self):
        self.level=0
        self.price=5
        self.show()
        self.rect.topleft = 430, 340
        
    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.manaRegen += 1
                self.rect.topleft = 430, 340
        except StopIteration:
            return

    def costDisplay(self):
        super(healthRegenUpgrade, self).costDisplay()
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(500, 500)
