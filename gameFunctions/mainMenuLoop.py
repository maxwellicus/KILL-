#import things
import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

#check
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

#create paths to other folders
sys.path.insert(0,'functions')
sys.path.insert(0,'classes')
sys.path.insert(0,'gameFunctions')

#import functions
from load_image import load_image
from load_sound import load_sound
from findAngle import findAngle
from findDistance import findDistance

def mainmenuLoop():

   #Main Menu Loop
   game=0
   while 1:
       clock.tick(60)
       crosshair.update()
       for event in pygame.event.get():
           if event.type == QUIT:
                pygame.quit()
           elif event.type == MOUSEBUTTONDOWN:
               for button in mainMenuButtons:
                   if pygame.sprite.collide_rect(crosshair, exitGame):
                       pygame.quit()
                   if pygame.sprite.collide_rect(crosshair, playGame):
                       
                    #initialize game
                       game=1
                       time=0
                       second=0
                       wave=1
                       spawner=1020
                       fire=0
                       bulletTimer=0
                       healthRegenTimer=0
                       manaRegenTimer=0
                       reloadTimer=-1
                       pause=0
                       dead=0
                       movex=0
                       movey=0
                       
                    #revert everything
                       player.revert()
                       maxHealth.revert()
                       refireRate.revert()
                       movementSpeed.revert()
                       numberOfShots.revert()
                       healthRegen.revert()
                       maxMana.revert()
                       manaRegen.revert()
                       pistol.revert()
                       machineGun.revert()
                       shotGun.revert()
                       
       screen.blit(mainMenuBackground_surface, (0,0))
       bottomsprites = pygame.sprite.RenderPlain((mainMenuButtons))
       bottomsprites.draw(screen)
       topSprite = pygame.sprite.RenderPlain((crosshair))
       topSprite.draw(screen)
       pygame.display.flip()