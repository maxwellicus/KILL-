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

#from mainMenu import mainMenu

def main():

	#initialize everything
	from initialize import *

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

		#Game Loop
		while game==1:
			clock.tick(60)

		#Timers
			time+=1
			second+=1
			if second >= 60:
				second=0

		#Controls
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
				if event.type == KEYDOWN:
					if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
						pause=1

				#reload weapon
					if event.key == K_r and weapon.chooseAmmo(pistol,machineGun,shotGun)<weapon.chooseClipSize(pistol,machineGun,shotGun):
						reloadTimer=weapon.startReload(player,pistol,machineGun,shotGun)

				#change spell
					if event.key == K_e:
						magic.changeSpell(1)
					elif event.key == K_q:
						magic.changeSpell(-1)
			                 
				#player movement
					if event.key == K_d:
						movex = player.speed
					elif event.key == K_a:
						movex = -player.speed
					if event.key == K_s:
						movey = player.speed
					elif event.key == K_w:
						movey = -player.speed
			         
				if event.type == KEYUP:
					if event.key == K_d:
						movex = 0
					elif event.key == K_a:
						movex = 0
					if event.key == K_s:
						movey = 0
					elif event.key == K_w:
						movey = 0

			#shooting
				if event.type == MOUSEBUTTONDOWN and event.button==1:
					fire=1
				elif event.type == MOUSEBUTTONUP and event.button==1:
					fire=0

			#magic
				if event.type == MOUSEBUTTONDOWN and event.button==3 and player.mana>0:
					magic.chooseSpell(airStrike,heal,teleport,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)

			#change weapon
				if event.type == MOUSEBUTTONDOWN and event.button==4:
					weapon.changeWeapon(1)
					reloadTimer=-1
				elif event.type == MOUSEBUTTONDOWN and event.button==5:
					weapon.changeWeapon(-1)
					reloadTimer=-1

		#spawn enemies
			spawner = enemy.spawn(second, spawner, enemies)

		#detect collision
			for enemy in enemies:
				if pygame.sprite.collide_rect(enemy, player):
					enemy.collision(enemy,enemies,player,score,money,health,splatters,explosions)
                                  
				for bullet in bullets:
					if pygame.sprite.collide_rect(enemy, bullet):
						enemy.hurt(enemy,bullet.damage,player,score,money,health,enemies,splatters,explosions)
						bullet.penetration-=1
						if not bullet.penetration:
							bullet.kill()

			for enemyBullet in enemyBullets:
				if pygame.sprite.collide_rect(enemyBullet, player):
					enemyBullet.collision(health)
					if(player.health<=0):
						wilhelm.play()
						dead=1

		#reload timer
			if reloadTimer>0:
				reloadTimer-=1
			elif reloadTimer==0:
				weapon.finishReload(player,pistol,machineGun,shotGun)
				reloadTimer=-1

		#fire gun
			bulletTimer+=1
			if fire==1 and reloadTimer<0 and weapon.chooseAmmo(pistol,machineGun,shotGun)>0:
				bulletTimer=weapon.chooseFire(bulletTimer,bullets,pistol,machineGun,shotGun,crosshair,player)
			elif fire==1 and reloadTimer<0 and weapon.chooseAmmo(pistol,machineGun,shotGun)==0:
				reloadTimer=weapon.startReload(player,pistol,machineGun,shotGun)

		#regenerate health
			healthRegenTimer+=1
			if healthRegenTimer>=player.healthRegen and player.health<player.maxHealth:
				health.update(1)
				healthRegenTimer=0

		#regenerate mana
			manaRegenTimer+=player.manaRegen
			if manaRegenTimer>=1800 and player.mana<player.maxMana:
				mana.update(1)
				manaRegenTimer=0

		#check if dead
			if(player.health<=0):
				wilhelm.play()
				dead=1
           
		#update/show everything
			enemies.update(player.rect.centerx, player.rect.centery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions)
			bullets.update()
			enemyBullets.update()
			player.update(movex, movey)
			crosshair.update()
			splatters.update()
			explosions.update()
			score.show()
			money.show()
			health.show()
			mana.show()
			ammo.show(pistol,shotGun,machineGun)
			reloadGun.show(reloadTimer)
			equippedWeapon.show()
			equippedSpell.show()

		#Draw Everything
			bottomsprites = pygame.sprite.RenderPlain((player, bullets, enemies, splatters, explosions, enemyBullets))
			topSprite = pygame.sprite.RenderPlain((crosshair, score, money, health, mana, ammo, reloadGun, equippedWeapon, equippedSpell))
			screen.blit(background_surface, (0,0))
			bottomsprites.draw(screen)
			topSprite.draw(screen)
			pygame.display.flip()

		#Pause Screen Loop
			while pause==1:
				clock.tick(60)
				crosshair.update()
             	
			#initialize values
				upgradeScreen=0
				weaponScreen=0
				magicScreen=0
             
			#controls
				for event in pygame.event.get():
                 	#quit
					if event.type == QUIT:
						pygame.quit()
					if event.type == KEYDOWN:
						if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
							pause=0
					elif event.type == MOUSEBUTTONDOWN:
                     	#click buttons
						for pauseScreenButton in pauseScreenButtons:
							if pygame.sprite.collide_rect(crosshair, pauseScreenButton):
                            	#upgrade screen
								if pygame.sprite.collide_rect(crosshair,upgradeButton):
									upgradeScreen=1
                            	#magic screen
								elif pygame.sprite.collide_rect(crosshair,magicButton):
									magicScreen=1
                            	#weapon screen
								elif pygame.sprite.collide_rect(crosshair,weaponButton):
									weaponScreen=1
                        	#go back
							if pygame.sprite.collide_rect(crosshair,goBack):
								pause=0

			#show everything
				health.show()
				score.show()
				money.show()
				ammo.show(pistol,shotGun,machineGun)
				reloadGun.show(reloadTimer)
				equippedWeapon.show()
				equippedSpell.show()
				screen.blit(pauseBackground_surface, (0,0))
				bottomsprites = pygame.sprite.RenderPlain((pauseScreenButtons,goBack))
				bottomsprites.draw(screen)
				middlesprites = pygame.sprite.RenderPlain((score, money, health, mana, ammo, reloadGun, equippedWeapon, equippedSpell))
				middlesprites.draw(screen)
				topSprite = pygame.sprite.RenderPlain((crosshair))
				topSprite.draw(screen)
				pygame.display.flip()

			#Upgrade Screen
				while upgradeScreen==1:
					clock.tick(60)
					crosshair.update()

				#controls
					for event in pygame.event.get():
						#quit
						if event.type == QUIT:
							pygame.quit()
						if event.type == KEYDOWN:
							if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
								upgradeScreen=0
								pause=0
					#click buttons
						elif event.type == MOUSEBUTTONDOWN:
							#upgrade things
							for upgrade in upgrades:
								if pygame.sprite.collide_rect(crosshair, upgrade):
									upgrade.upgrade()
							#go back
							if pygame.sprite.collide_rect(crosshair, goBack):
								upgradeScreen=0

					#show everything
					health.show()
					score.show()
					money.show()
					ammo.show(pistol,shotGun,machineGun)
					reloadGun.show(reloadTimer)
					equippedWeapon.show()
					equippedSpell.show()
					screen.blit(pauseBackground_surface, (0,0))
					bottomsprites = pygame.sprite.RenderPlain((upgrades,upgradeCosts,goBack))
					bottomsprites.draw(screen)
					middlesprites = pygame.sprite.RenderPlain((score, money, health, mana, ammo, reloadGun, equippedWeapon, equippedSpell))
					middlesprites.draw(screen)
					topSprite = pygame.sprite.RenderPlain((crosshair))
					topSprite.draw(screen)
					pygame.display.flip()

				#Magic Screen
				while magicScreen==1:
					clock.tick(60)
					crosshair.update()
                 
					#controls
					for event in pygame.event.get():
						#quit
						if event.type == QUIT:
							pygame.quit()
						if event.type == KEYDOWN:
							if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
								magicScreen=0
								pause=0
						#click buttons
						elif event.type == MOUSEBUTTONDOWN:
							#equip spell
							for magic in spells:
								if pygame.sprite.collide_rect(crosshair, magic):
									magic.click()
							#go back
							if pygame.sprite.collide_rect(crosshair, goBack):
								magicScreen=0

					#show everything
					for magic in spells:
						magic.show()
					health.show()
					score.show()
					money.show()
					ammo.show(pistol,shotGun,machineGun)
					reloadGun.show(reloadTimer)
					equippedWeapon.show()
					equippedSpell.show()
					screen.blit(pauseBackground_surface, (0,0))
					bottomsprites = pygame.sprite.RenderPlain((spells,magicCosts,goBack))
					bottomsprites.draw(screen)
					middlesprites = pygame.sprite.RenderPlain((score, money, health, mana, ammo, reloadGun, equippedWeapon, equippedSpell))
					middlesprites.draw(screen)
					topSprite = pygame.sprite.RenderPlain((crosshair))
					topSprite.draw(screen)
					pygame.display.flip()

				#Weapon Screen
				while weaponScreen==1:
					clock.tick(60)
					crosshair.update()

					#controls
					for event in pygame.event.get():
						#quit
						if event.type == QUIT:
							pygame.quit()
						if event.type == KEYDOWN:
							if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
								weaponScreen=0
								pause=0

						#click buttons
						elif event.type == MOUSEBUTTONDOWN:
							#equip weapons
							for weapon in weapons:
								if pygame.sprite.collide_rect(crosshair, weapon):
									weapon.click()
							#go back
							if pygame.sprite.collide_rect(crosshair, goBack):
								weaponScreen=0

					#show everything
					for weapon in weapons:
						weapon.show()
					health.show()
					score.show()
					money.show()
					ammo.show(pistol,shotGun,machineGun)
					reloadGun.show(reloadTimer)
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
                 
			#Death Screen Loop
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

if __name__ == '__main__': main()
