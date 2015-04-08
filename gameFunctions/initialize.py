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

def initialize():

	#initializing
	pygame.init()
	window = pygame.display.set_mode((1200, 600))
	pygame.display.set_caption('KILL!')
	screen = pygame.display.get_surface()
	from pygame.locals import *
	flags = FULLSCREEN | DOUBLEBUF
	#screen = pygame.display.set_mode(resolution, flags, bpp)
	pygame.mouse.set_visible(0)

	#Create Backgrounds
	background = os.path.join('data', 'background.png')
	background_surface = pygame.image.load(background)
	mainMenuBackground = os.path.join('data', 'mainMenu.png')
	mainMenuBackground_surface = pygame.image.load(mainMenuBackground)
	pauseBackground = os.path.join('data', 'pause.png')
	pauseBackground_surface = pygame.image.load(pauseBackground)

	#Display Background
	screen.blit(background_surface, (0, 0))
	pygame.display.flip()

	#play music
	music = os.path.join('data', 'Throwing Fire.wav')
	pygame.mixer.music.load(music)
	#pygame.mixer.music.play()

	#load sound effects
	wilhelm = load_sound('wilhelm.wav')

	#prepare preparations
	spawnx, spawny = -100, -100
	playerx, playery = -10, -10
	crossx, crossy = -20, -20
	splatterx, splattery = -100, -100

	#Prepare Game Objects
	clock = pygame.time.Clock()
	crosshair = Crosshair()
	enemy = Enemy()

	#initialize player
	player_file_name = os.path.join("data", "smiley.png")
	player_surface = pygame.image.load(player_file_name)
	screen.blit(player_surface, (0,0))
	movex, movey = 0,0
	player = Player()

	#Initialize groups
	bullets = pygame.sprite.Group()
	enemyBullets = pygame.sprite.Group()
	enemies = pygame.sprite.Group()
	splatters = pygame.sprite.Group()
	explosions = pygame.sprite.Group()
	upgrades = pygame.sprite.Group()
	spells = pygame.sprite.Group()
	weapons = pygame.sprite.Group()
	upgradeCosts = pygame.sprite.Group()
	magicCosts = pygame.sprite.Group()
	weaponCosts = pygame.sprite.Group()
	mainMenuButtons = pygame.sprite.Group()
	pauseScreenButtons = pygame.sprite.Group()
	deathScreenButtons = pygame.sprite.Group()

	#initialize buttons
	playGame=playGameButton()
	mainMenuButtons.add(playGame)
	exitGame=exitButton()
	mainMenuButtons.add(exitGame)
	deathScreenButtons.add(exitGame)
	mainMenu=mainMenuButton()
	deathScreenButtons.add(mainMenu)
	upgradeButton=upgradeScreenButton()
	weaponButton=weaponScreenButton()
	magicButton=magicScreenButton()
	pauseScreenButtons.add(upgradeButton)
	pauseScreenButtons.add(weaponButton)
	pauseScreenButtons.add(magicButton)
	goBack=backButton()
	exitGame=exitButton()

	#initialize upgrades
	upgrade=Upgrade(player,upgradeCosts)
	maxHealth=maxHealthUpgrade(player,upgradeCosts)
	upgrades.add(maxHealth)
	refireRate=refireRateUpgrade(player,upgradeCosts)
	upgrades.add(refireRate)
	movementSpeed=movementSpeedUpgrade(player,upgradeCosts)
	upgrades.add(movementSpeed)
	numberOfShots=numberOfShotsUpgrade(player,upgradeCosts)
	upgrades.add(numberOfShots)
	healthRegen=healthRegenUpgrade(player,upgradeCosts)
	upgrades.add(healthRegen)
	maxMana=maxManaUpgrade(player,upgradeCosts)
	upgrades.add(maxMana)
	manaRegen=manaRegenUpgrade(player,upgradeCosts)
	upgrades.add(manaRegen)

	#initialize spells
	magic=Magic(player,magicCosts)
	airStrike=AirStrikeMagic(player,magicCosts)
	spells.add(airStrike)
	heal=HealMagic(player,magicCosts)
	spells.add(heal)
	teleport=TeleportMagic(player,magicCosts)
	spells.add(teleport)

	#initialize weapons
	weapon=Weapon(player,weaponCosts)
	pistol=PistolWeapon(player,weaponCosts)
	weapons.add(pistol)
	machineGun=MachineGunWeapon(player,weaponCosts)
	weapons.add(machineGun)
	shotGun=ShotGunWeapon(player,weaponCosts)
	weapons.add(shotGun)

	#initialize HUD
	score = Score(player)
	money = Money(player)
	health = Health(player)
	mana = Mana(player)
	ammo = Ammo(player)
	reloadGun = Reload(player)
	equippedWeapon = EquippedWeapon(player)
	equippedSpell = EquippedSpell(player)

	#inititialize other groups
	bullet = Bullet(-100,-100,-100,-100,1,1)
	enemyBullet = EnemyBullet(-100,-100,-100,-100,1)