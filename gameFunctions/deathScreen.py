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

#import classes
from player import Player
from score import Score
from money import Money
from health import Health
from mana import Mana
from ammo import Ammo
from reload import Reload
from equippedWeapon import EquippedWeapon
from equippedSpell import EquippedSpell
from crosshair import Crosshair
from enemy import Enemy
from splatter import Splatter
from explosion import Explosion
from bullet import Bullet
from enemyBullet import EnemyBullet
from weapon import Weapon
from weapon import PistolWeapon
from weapon import MachineGunWeapon
from weapon import ShotGunWeapon
from costImage import costImage
from magic import Magic
from magic import HealMagic
from magic import AirStrikeMagic
from magic import TeleportMagic
from upgrade import Upgrade
from upgrade import maxHealthUpgrade
from upgrade import refireRateUpgrade
from upgrade import movementSpeedUpgrade
from upgrade import numberOfShotsUpgrade
from upgrade import healthRegenUpgrade
from upgrade import maxManaUpgrade
from upgrade import manaRegenUpgrade
from buttons import playGameButton
from buttons import exitButton
from buttons import mainMenuButton
from buttons import upgradeScreenButton
from buttons import magicScreenButton
from buttons import weaponScreenButton
from buttons import backButton

from pauseScreen import pauseScreen
from upgradeScreen import upgradeScreen
from weaponScreen import weaponScreen
from magicScreen import magicScreen

def deathScreen():

	from initialize import *

	dead=1

	while dead==1:
		clock.tick(60)
		crosshair.update()
     
		#show everything
		score.post()
		money.post()
		health.post()
		mana.post()
		bottomSprites = pygame.sprite.RenderPlain((bullets,enemies,splatters,explosions))
		mediumSprites = pygame.sprite.RenderPlain((player))
		topSprites = pygame.sprite.RenderPlain((score,money,health,mana,deathScreenButtons))
		crosshairSprite = pygame.sprite.RenderPlain((crosshair))
		screen.blit(background_surface, (0,0))
		bottomSprites.draw(screen)
		mediumSprites.draw(screen)
		topSprites.draw(screen)
		crosshairSprite.draw(screen)
		pygame.display.flip()

		#controls
		for event in pygame.event.get():
			#quit
			if event.type == QUIT:
				pygame.quit()
			elif event.type == MOUSEBUTTONDOWN:
				for button in deathScreenButtons:
					if pygame.sprite.collide_rect(crosshair, exitGame):
						pygame.quit()
					#main menu
					elif pygame.sprite.collide_rect(crosshair, mainMenu):
						dead=0
						game=0
					#empty groups
						bullets.empty()
						enemies.empty()
						splatters.empty()
						explosions.empty()
						enemyBullets.empty()