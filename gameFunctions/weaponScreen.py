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

def weaponScreen():

	from initialize import *
	weaponPause=1
	
	#Weapon Screen
	while weaponPause==1:
		clock.tick(60)
		crosshair.update()

		#controls
		for event in pygame.event.get():
			#quit
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
					weaponPause=0
					pause=0

			#click buttons
			elif event.type == MOUSEBUTTONDOWN:
				#equip weapons
				for weapon in weapons:
					if pygame.sprite.collide_rect(crosshair, weapon):
						weapon.click()
				#go back
				if pygame.sprite.collide_rect(crosshair, goBack):
					weaponPause=0

		#show everything
		for weapon in weapons:
			weapon.show()
		health.show()
		score.show()
		money.show()
		ammo.show(pistol,shotGun,machineGun)
		reloadGun.show(reloadGun.timer)
		equippedWeapon.show()
		equippedSpell.show()
		screen.blit(pauseBackground_surface, (0,0))
		bottomsprites = pygame.sprite.RenderPlain((weapons,weaponCosts,goBack))
		bottomsprites.draw(screen)
		middlesprites = pygame.sprite.RenderPlain((score, money, health, mana, ammo, reloadGun, equippedWeapon, equippedSpell))
		middlesprites.draw(screen)
		topSprite = pygame.sprite.RenderPlain((crosshair))
		topSprite.draw(screen)
		pygame.display.flip()