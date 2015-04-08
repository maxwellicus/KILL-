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
from costImage import costImage
from bullet import Bullet

class Weapon(pygame.sprite.Sprite):
    """ super class for all magic """

    level = 0
    pictures = []
    
    def __init__(self, owner, costsGroup):
        pygame.sprite.Sprite.__init__(self)
        self.costsGroup = costsGroup
        self.owner = owner
        self.owner.weapon=1
        
    def chooseFire(self,bulletTimer,bullets,pistol,machineGun,shotGun,crosshair,player):
        if self.owner.weapon==1:
            return pistol.fire(bulletTimer,bullets,crosshair,player)
        elif self.owner.weapon==2:
            return machineGun.fire(bulletTimer,bullets,crosshair,player)   
        elif self.owner.weapon==3:
            return shotGun.fire(bulletTimer,bullets,crosshair,player)

    def startReload(self,player,pistol,machineGun,shotGun):
        if self.owner.weapon==1:
            return pistol.reloadTimer
        elif self.owner.weapon==2:
            return machineGun.reloadTimer   
        elif self.owner.weapon==3:
            return shotGun.reloadTimer

    def finishReload(self,player,pistol,machineGun,shotGun):
        if self.owner.weapon==1:
            pistol.ammo=pistol.clipSize
        elif self.owner.weapon==2:
            machineGun.ammo=machineGun.clipSize   
        elif self.owner.weapon==3:
            shotGun.ammo=shotGun.clipSize

    def changeWeapon(self,weaponChange):
        self.owner.weapon+=weaponChange
        if self.owner.weapon>3:
            self.owner.weapon=1
        if self.owner.weapon<1:
            self.owner.weapon=3

    def chooseAmmo(self,pistol,machineGun,shotGun):
        if self.owner.weapon==1:
            return pistol.ammo
        elif self.owner.weapon==2:
            return machineGun.ammo  
        elif self.owner.weapon==3:
            return shotGun.ammo

    def chooseClipSize(self,pistol,machineGun,shotGun):
        if self.owner.weapon==1:
            return pistol.clipSize
        elif self.owner.weapon==2:
            return machineGun.clipSize  
        elif self.owner.weapon==3:
            return shotGun.clipSize

class PistolWeapon(Weapon):
    price=0
    clipSize=6
    ammo=6
    reloadTimer=20
    rateOfFire=10
    power=1
    accuracy=0
    def __init__(self, owner, costsGroup):
        super(PistolWeapon, self).__init__(owner, costsGroup)
        self.costSprite = costImage(10, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def revert(self):
        self.price=0
        self.clipSize=6
        self.ammo=6
        self.reloadTimer=20
        self.rateOfFire=10
        self.power=1
        self.accuracy=0

    def click(self):
        self.owner.weapon=1

    def fire(self,bulletTimer,bullets,crosshair,player):
        if bulletTimer>=self.rateOfFire:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            self.ammo-=1
            bulletAngle=findAngle(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery)+random.randint(-self.accuracy,self.accuracy)
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle,self.power))
            return 0
        else:
            return bulletTimer

    def reloadGun(self,player):
        self.ammo=self.clipSize
        return self.reloadTimer

    def show(self):
        if self.owner.weapon==1:
            self.image, self.rect = load_image('pistol.equipped.png')
        else:
            self.image, self.rect = load_image('pistol.png')
        self.rect.topleft = 10, 40
        self.costSprite.costDisplay(self.price, self.level)

class MachineGunWeapon(Weapon):
    price=100
    clipSize=50
    ammo=50
    reloadTimer=30
    rateOfFire=4
    power=1
    accuracy=10
    
    def __init__(self, owner, costsGroup):
        super(MachineGunWeapon, self).__init__(owner, costsGroup)
        self.costSprite = costImage(220, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def revert(self):
        self.price=100
        self.clipSize=50
        self.ammo=50
        self.reloadTimer=30
        self.rateOfFire=4
        self.power=1
        accuracy=10

    def click(self):
        self.owner.weapon=2

    def fire(self,bulletTimer,bullets,crosshair,player):
        if bulletTimer>=self.rateOfFire:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            self.ammo-=1
            bulletAngle=findAngle(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery)+random.randint(-self.accuracy,self.accuracy)
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle,self.power))
            return 0
        else:
            return bulletTimer

    def show(self):
        if self.owner.weapon==2:
            self.image, self.rect = load_image('machineGun.equipped.png')
        else:
            self.image, self.rect = load_image('machineGun.png')
        self.rect.topleft = 220, 40
        self.costSprite.costDisplay(self.price, self.level)

class ShotGunWeapon(Weapon):
    price=200
    clipSize=6
    ammo=6
    reloadTimer=30
    rateOfFire=20
    power=1
    accuracy=10
    numberOfShots=3
    
    def __init__(self, owner, costsGroup):
        super(ShotGunWeapon, self).__init__(owner, costsGroup)
        self.costSprite = costImage(430, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def revert(self):
        self.price=200
        self.clipSize=6
        self.ammo=6
        self.reloadTimer=30
        self.rateOfFire=20
        self.power=1
        self.accuracy=10
        self.numberOfShots=3

    def click(self):
        self.owner.weapon=3

    def fire(self,bulletTimer,bullets,crosshair,player):
        if bulletTimer>=self.rateOfFire:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            self.ammo-=1
            bulletAngle=findAngle(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery)
            for shot in range(self.numberOfShots):
                bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle+random.randint(-self.accuracy,self.accuracy),self.power))
            return 0
        else:
            return bulletTimer

    def show(self):
        if self.owner.weapon==3:
            self.image, self.rect = load_image('shotGun.equipped.png')
        else:
            self.image, self.rect = load_image('shotGun.png')
        self.rect.topleft = 430, 40
        self.costSprite.costDisplay(self.price, self.level)