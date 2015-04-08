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
from explosion import Explosion

class Magic(pygame.sprite.Sprite):
    """ super class for all magic """
    level = 0
    pictures = []
    
    def __init__(self, owner, costsGroup):
        pygame.sprite.Sprite.__init__(self)
        self.costsGroup = costsGroup
        self.owner = owner
        self.owner.spell=3

    def chooseSpell(self,airStrike,heal,teleport,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        if self.owner.spell==1:
            airStrike.use(crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)
        elif self.owner.spell==2 and player.health<player.maxHealth:
            heal.use(crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)    
        elif self.owner.spell==3:
            teleport.use(crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)

    def changeSpell(self,spellChange):
        self.owner.spell+=spellChange
        if self.owner.spell>3:
            self.owner.spell=1
        if self.owner.spell<1:
            self.owner.spell=3

class AirStrikeMagic(Magic):
    price=10
    def __init__(self, owner, costsGroup):
        super(AirStrikeMagic, self).__init__(owner, costsGroup)
        self.costSprite = costImage(10, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def click(self):
        self.owner.spell=1

    def use(self,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        mana.update(-1)
        explosions.add(Explosion(crosshair.rect.centerx, crosshair.rect.centery,player,score,money,health,enemy,enemies,splatters,explosions))

    def show(self):
        if self.owner.spell==1:
            self.image, self.rect = load_image('airStrike.eqipped.png')
        else:
            self.image, self.rect = load_image('airStrike.png')
        self.rect.topleft = 10, 40
        self.costSprite.costDisplay(self.price, self.level)

class HealMagic(Magic):
    price=10
    def __init__(self, owner, costsGroup):
        super(HealMagic, self).__init__(owner, costsGroup)
        self.costSprite = costImage(220, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def click(self):
        self.owner.spell=2

    def use(self,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        if player.health<player.maxHealth:
            mana.update(-1)
            health.update(10)
            if player.health>player.maxHealth:
                player.health=player.maxHealth

    def show(self):
        if self.owner.spell==2:
            self.image, self.rect = load_image('heal.equipped.png')
        else:
            self.image, self.rect = load_image('heal.png')
        self.rect.topleft = 220, 40
        self.costSprite.costDisplay(self.price, self.level)

class TeleportMagic(Magic):
    price=10
    def __init__(self, owner, costsGroup):
        super(TeleportMagic, self).__init__(owner, costsGroup)
        self.costSprite = costImage(440, 10)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def click(self):
        self.owner.spell=3

    def use(self,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        mana.update(-1)
        player.rect.centerx=crosshair.rect.centerx
        player.rect.centery=crosshair.rect.centery

    def show(self):
        if self.owner.spell==3:
            self.image, self.rect = load_image('teleport.equipped.png')
        else:
            self.image, self.rect = load_image('teleport.png')
        self.rect.topleft = 440, 40
        self.costSprite.costDisplay(self.price, self.level)