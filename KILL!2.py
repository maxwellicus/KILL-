import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

class Player(pygame.sprite.Sprite):
   def __init__(self):
       pygame.sprite.Sprite.__init__(self) #call Sprite initializer
       self.image, self.rect = load_image('smiley.png', -1)
       self.rect.centerx, self.rect.centery = 600, 300

   def revert(self):
       self.health = 100
       self.mana = 3
       self.money = 0
       self.score = 0
       self.maxHealth = 100
       self.maxMana = 5
       self.speed = 5
       self.refireRate = 2
       self.numberOfShots = 1
       self.healthRegen = 1
       self.manaRegen = 1
       self.spell = 3
       self.rect.centerx, self.rect.centery = 600, 300
       
   def update(self, x, y):
       self.rect = self.rect.move((x,y))

class Score(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('red')
        self.score=0

    def update(self, change):
        self.owner.score += change

    def show (self):
        self.font = pygame.font.Font(None, 40)
        msg = "Score: %d" % self.owner.score
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(1000, 10)

    def post(self):
        self.font = pygame.font.Font(None, 100)
        msg = "Score: %d" % self.owner.score
        self.rect = self.image.get_rect().move(600, 200)
        self.image = self.font.render(msg, 0, self.color)

class Money(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('gold')
        self.money=0

    def update(self, change):
        self.owner.money += change

    def show (self):
        self.font = pygame.font.Font(None, 40)
        msg = "Money: %d" % self.owner.money
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(1000, 40)

    def post(self):
        self.font = pygame.font.Font(None, 100)
        msg = "Money: %d" % self.owner.money
        self.rect = self.image.get_rect().move(600, 300)
        self.image = self.font.render(msg, 0, self.color)

class Health(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('green')

    def update(self,change):
        self.owner.health += change

    def show(self):
        self.font = pygame.font.Font(None, 40)
        msg = "Health: %d/%d" % (self.owner.health,self.owner.maxHealth)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 10)

    def post(self):
        self.font = pygame.font.Font(None, 100)
        msg = "Health: %d/%d" % (self.owner.health, self.owner.maxHealth)
        self.rect = self.image.get_rect().move(600, 400)
        self.image = self.font.render(msg, 0, self.color)

class Mana(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.mana=3
        self.maxmana=3

    def update(self,change):
        self.owner.mana+=change

    def show(self):
        self.font = pygame.font.Font(None, 40)
        msg = "Mana: %d/%d" % (self.owner.mana,self.owner.maxMana)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(1000, 570)

    def post(self):
        self.font = pygame.font.Font(None, 100)
        msg = "Mana: %d/%d" % (self.owner.mana, self.owner.maxMana)
        self.rect = self.image.get_rect().move(600, 500)
        self.image = self.font.render(msg, 0, self.color)

class Ammo(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('black')

    def show(self,pistol,shotGun,machineGun):
        self.font = pygame.font.Font(None, 40)
        if self.owner.weapon==1:
            msg = "Ammo: %d/%d" % (pistol.ammo,pistol.clipSize)
        elif self.owner.weapon==2:
            msg = "Ammo: %d/%d" % (machineGun.ammo,machineGun.clipSize)
        elif self.owner.weapon==3:
            msg = "Ammo: %d/%d" % (shotGun.ammo,shotGun.clipSize)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 570)

class Reload(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('black')

    def show(self,reloadTimer):
        self.font = pygame.font.Font(None, 40)
        msg = "Reload: %d" % (reloadTimer)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 540)

class EquippedWeapon(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('black')

    def show(self):
        self.font = pygame.font.Font(None, 40)
        if self.owner.weapon==1:
            msg = "Weapon: Pistol"
        elif self.owner.weapon==2:
            msg = "Weapon: Machinegun"
        elif self.owner.weapon==3:
            msg = "Weapon: Shotgun"
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 510)

class EquippedSpell(pygame.sprite.Sprite):
    def __init__(self, owner):
        self.owner = owner
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('blue')

    def show(self):
        self.font = pygame.font.Font(None, 40)
        if self.owner.spell==1:
            msg = "Spell: Airstrike"
        elif self.owner.spell==2:
            msg = "Spell: Heal"
        elif self.owner.spell==3:
            msg = "Spell: Teleport"
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(1000, 540)

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('crosshair.png', -1)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Enemy(pygame.sprite.Sprite):
    """ Generic enemy class, all enemies will inherit from Enemy """
    health = 1
    speed = 1
    attackSpeed=60
    attackPower=1
    attackTimer=0
    collide=0
    distance=999
    
    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.distance = findDistance(self.rect.centerx, self.rect.centery, playerx, playery)
        if self.collide==0:
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            self.movex = self.speed*math.cos(angle*math.pi/180)
            self.movey = self.speed*math.sin(angle*math.pi/180)*-1
            self.rect = self.rect.move(self.movex,self.movey)
        elif self.collide==1 and self.attackTimer==0:
            self.attack(health)
            self.attackTimer=self.attackSpeed
        if self.attackTimer>0:
            self.attackTimer-=1
        self.collide=0

    def spawn(self,second,spawner,enemies):
        if second==0:
            spawner+=1
        spawn = random.randint(1,spawner)
        if spawn>=1000:
            enemy=self.randomEnemy()
            if enemy!=0:
                enemies.add(enemy)
        return spawner

    def randomEnemy(self):
        """ returns a new (randomly, based on the level) enemy object at (x, y) """
        
        maxEnemy=78
        maxSpawn=600
        maxPosition=6
        
        enemy = random.randint(1,maxEnemy)
        spawn = random.randint(1,maxSpawn)
        position = random.randint(1,maxPosition)

        if position==1:#TopLeft
            x,y = spawn,0
        elif position==2:#TopRight
            x,y = 600+spawn,0
        elif position==3:#Right
            x,y = 1200,spawn
        elif position==4:#BottomLeft
            x,y = spawn,600
        elif position==5:#BottomRight
            x,y = 600+spawn,600
        elif position==6:#Left
            x,y = 0,spawn
             
        if enemy<=maxEnemy:
            return RocketTurret(x, y)
        else:
            return 0

    def hurt(self,enemy,damage,player,score,money,health,enemies,splatters,explosions):
        splat = load_sound('splat.wav')
        splat.play()
        enemy.health -= damage
        if self.health <= 0:
            enemy.die(enemy,enemies,player,score,money,health,splatters,explosions)

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        enemy.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(enemy.rect.centerx, enemy.rect.centery))

    def collision(self,enemy,enemies,player,score,money,health,splatters,explosions):
        self.collide=1

    def attack(self,health):
        ouch = load_sound('ouch.wav')
        health.update(-self.attackPower)
        ouch.play()
    
class Zombie(Enemy):
    """ basic Zombie enemy """
    health = 3
    speed = 3
    attackSpeed=60
    attackPower=5
    attackTimer=0
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('zombie.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

class Runner(Enemy):
    """ basic Runner enemy """
    health = 1
    speed = 7
    attackSpeed=20
    attackPower=1
    attackTimer=0
    lungeDistance=200
    lungeAngle=0
    lungeSpeed=20
    lungeTimer=0
    lungeMovement=15
    lungeAttack=0
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('runner.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.distance = findDistance(self.rect.centerx, self.rect.centery, playerx, playery)
        angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
        if self.lungeTimer==0 and self.attackTimer==0:
            self.movex = self.speed*math.cos(angle*math.pi/180)
            self.movey = self.speed*math.sin(angle*math.pi/180)*-1
            self.rect = self.rect.move(self.movex,self.movey)            
        if self.distance<=self.lungeDistance and self.lungeTimer==0 and self.attackTimer==0:
            self.lungeAngle=angle
            self.lungeTimer=self.lungeSpeed
            self.lungeAttack=0
        if self.lungeTimer>0:
            self.lunge(health)
        if self.attackTimer>0:
            self.attackTimer-=1
        self.collide=0

    def lunge(self,health):
        self.lungeTimer-=1
        self.movex = self.lungeMovement*math.cos(self.lungeAngle*math.pi/180)
        self.movey = self.lungeMovement*math.sin(self.lungeAngle*math.pi/180)*-1
        self.rect = self.rect.move(self.movex,self.movey)
        if self.collide==1 and self.lungeAttack==0:
            self.attack(health)
            self.lungeAttack=1
        if self.lungeTimer==0:
            self.attackTimer=self.attackSpeed

    def attack(self,health):
        ouch = load_sound('ouch.wav')
        health.update(-self.attackPower)
        ouch.play()

class BombDude(Enemy):
    """ basic Runner enemy """
    health = 1
    speed = 2
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bombDude.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny
        move=random.randint(0,1)
        self.movex=1
        self.movey=1
        if spawnx==0:
            self.movex=1
            if move==0:
                self.movey=-1
            elif move==1:
                self.movey=1
        elif spawnx==1200:
            self.movex=-1
            if move==0:
                self.movey=-1
            elif move==1:
                self.movey=1
        elif spawny==0:
            self.movey=1
            if move==0:
                self.movex=-1
            elif move==1:
                self.movex=1
        elif spawny==600:
            self.movey=-1
            if move==0:
                self.movex=-1
            elif move==1:
                self.movex=1

    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.rect = self.rect.move(self.movex*self.speed,self.movey*self.speed)
        if self.rect.centerx<=0:
            self.movex=1
        elif self.rect.centerx>=1200:
            self.movex=-1
        elif self.rect.centery<=0:
            self.movey=1
        elif self.rect.centery>=600:
            self.movey=-1
        

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        enemy.kill()
        score.update(1)
        money.update(1)
        explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery,player,score,money,health,enemy,enemies,splatters,explosions))

    def collision(self,enemy,enemies,player,score,money,health,splatters,explosions):
        ouch = load_sound('ouch.wav')
        enemy.kill()
        health.update(-attackPower)
        explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery,player,score,money,health,enemy,enemies,splatters,explosions))
        ouch.play()
    
class Arrow(Enemy):
    health = 1
    speed = 20
    attackPower=5
    movex=0
    movey=0

    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('arrow.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny
        if spawnx==0:
            self.movex=1
            self.movey=0
            self.image=pygame.transform.rotate(self.image,-90)
        elif spawnx==1200:
            self.movex=-1
            self.movey=0
            self.image=pygame.transform.rotate(self.image,90)
        elif spawny==0:
            self.movex=0
            self.movey=1
            self.image=pygame.transform.flip(self.image,0,1)
        elif spawny==600:
            self.movex=0
            self.movey=-1

    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.rect = self.rect.move(self.movex*self.speed,self.movey*self.speed)
        if self.rect.centerx<=0:
            self.image=pygame.transform.flip(self.image,1,0)
            self.movex=1
            self.movey=0
        elif self.rect.centerx>=1200:
            self.image=pygame.transform.flip(self.image,1,0)
            self.movex=-1
            self.movey=0
        elif self.rect.centery<=0:
            self.image=pygame.transform.flip(self.image,0,1)
            self.movex=0
            self.movey=1
        elif self.rect.centery>=600:
            self.image=pygame.transform.flip(self.image,0,1)
            self.movex=0
            self.movey=-1

    def collision(self,enemy,enemies,player,score,money,health,splatters,explosions):
        ouch = load_sound('ouch.wav')
        enemy.kill()
        health.update(-self.attackPower)
        ouch.play()

class Seeker(Enemy):
    health = 1
    speed = 20
    attackPower=5
    scanTimer=60
    angle=0
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('seeker.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny
        #if spawnx==0:
            #self.image=pygame.transform.rotate(self.image,-90)
        #elif spawnx==1200:
            #self.image=pygame.transform.rotate(self.image,90)
        #elif spawny==0:
            #self.image=pygame.transform.flip(self.image,0,1)

    def collision(self,enemy,enemies,player,score,money,health,splatters,explosions):
        ouch = load_sound('ouch.wav')
        enemy.kill()
        health.update(-self.attackPower)
        ouch.play()

    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.movex=0
        self.movey=0
        if self.scanTimer>0:
            self.scanTimer-=1
            self.movex=0
            self.movey=0
        elif self.scanTimer==0:
            if self.rect.centerx<=0:
                self.movex=1
            elif self.rect.centerx>=1200:
                self.movex=-1
            elif self.rect.centery<=0:
                self.movey=1
            elif self.rect.centery>=600:
                self.movey=-1
            else:
                x, y=self.rect.centerx, self.rect.centery
                self.image, self.rect = load_image('seeker.png', -1)
                self.rect.centerx, self.rect.centery=x, y
                self.angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.scanTimer=-1
        elif self.scanTimer<0:
            self.movex = self.speed*math.cos(self.angle*math.pi/180)
            self.movey = self.speed*math.sin(self.angle*math.pi/180)*-1
            if self.rect.centerx<=0:
                self.scanTimer=60
            elif self.rect.centerx>=1200:
                self.scanTimer=60
            elif self.rect.centery<=0:
                self.scanTimer=60
            elif self.rect.centery>=600:
                self.scanTimer=60
        self.rect = self.rect.move(self.movex,self.movey)
            
            

class PregnantBitch(Enemy):
    health = 5
    speed = 2
    attackSpeed=60
    attackPower=1
    attackTimer=0
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('pregnantBitch.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        enemy.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(enemy.rect.centerx, enemy.rect.centery))
        cry = load_sound('cry.wav')
        cry.play()
        for babies in range (1,random.randint(1,3)):
            enemies.add(Baby(enemy.rect.centerx+random.randint(-100,100), enemy.rect.centery+random.randint(-100,100)))

    def update(self, playerx, playery, enemyBullets, enemies, health):
        if self.collide==0:
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            self.movex = self.speed*math.cos(angle*math.pi/180)
            self.movey = self.speed*math.sin(angle*math.pi/180)*-1
            self.rect = self.rect.move(self.movex,self.movey)
        elif self.collide==1 and self.attackTimer==0:
            self.die(enemy,enemies,player,score,money,health,splatters,explosions)
        if self.attackTimer>0:
            self.attackTimer-=1
        self.collide=0

class Baby(Enemy):
    health = 1
    speed = 15
    attackSpeed=1
    attackPower=1
    attackTimer=0
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('baby.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

class BlobLarge(Enemy):
    health = 5
    speed = 2
    attackPower=5
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('blobLarge.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        enemy.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(enemy.rect.centerx, enemy.rect.centery))
        for blobs in range (1,3):
            enemies.add(BlobMedium(enemy.rect.centerx+random.randint(-100,100), enemy.rect.centery+random.randint(-100,100)))

    def update(self, playerx, playery, enemyBullets, enemies, health):
        if self.collide==0:
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            self.movex = self.speed*math.cos(angle*math.pi/180)
            self.movey = self.speed*math.sin(angle*math.pi/180)*-1
            self.rect = self.rect.move(self.movex,self.movey)
        elif self.collide==1 and self.attackTimer==0:
            self.attack(health)
            self.die(enemy,enemies,player,score,money,health,splatters,explosions)
        self.collide=0

class BlobMedium(Enemy):
    health = 3
    speed = 3
    attackPower=3
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('BlobMedium.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        enemy.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(enemy.rect.centerx, enemy.rect.centery))
        for blobs in range (1,3):
            enemies.add(BlobSmall(enemy.rect.centerx+random.randint(-50,50), enemy.rect.centery+random.randint(-50,50)))

    def update(self, playerx, playery, enemyBullets, enemies, health):
        if self.collide==0:
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            self.movex = self.speed*math.cos(angle*math.pi/180)
            self.movey = self.speed*math.sin(angle*math.pi/180)*-1
            self.rect = self.rect.move(self.movex,self.movey)
        elif self.collide==1 and self.attackTimer==0:
            self.attack(health)
            self.die(enemy,enemies,player,score,money,health,splatters,explosions)
        self.collide=0

class BlobSmall(Enemy):
    health = 1
    speed = 4
    attackSpeed=60
    attackPower=1
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('BlobSmall.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def update(self, playerx, playery, enemyBullets, enemies, health):
        if self.collide==0:
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            self.movex = self.speed*math.cos(angle*math.pi/180)
            self.movey = self.speed*math.sin(angle*math.pi/180)*-1
            self.rect = self.rect.move(self.movex,self.movey)
        elif self.collide==1 and self.attackTimer==0:
            self.attack(health)
            self.die(enemy,enemies,player,score,money,health,splatters,explosions)
        self.collide=0

class BulletTurret(Enemy):
    health = 5
    speed = 0
    power=1
    bulletTimer=60
    attackSpeed=60
    attackPower=5
    attackTimer=0
    
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('turretBase.png', -1)
        if spawnx==0:
            self.rect.centerx, self.rect.centery = spawnx+100, spawny
        elif spawny==0:
            self.rect.centerx, self.rect.centery = spawnx, spawny+100
        elif spawnx==1200:
            self.rect.centerx, self.rect.centery = spawnx-100, spawny
        elif spawny==600:
            self.rect.centerx, self.rect.centery = spawnx, spawny-100

    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.bulletTimer-=1
        if self.bulletTimer==0:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            enemyBullets.add(Bullet(self.rect.centerx, self.rect.centery, playerx, playery, angle, self.power))
            self.bulletTimer=self.attackSpeed

    def collision(self,enemy,enemies,player,score,money,health,splatters,explosions):
        health.update(0)
        
class RocketTurret(Enemy):
    health = 5
    speed = 0
    bulletTimer=60
    attackSpeed=60
    attackPower=10
    attackTimer=0
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('turretBase.png', -1)
        if spawnx==0:
            self.rect.centerx, self.rect.centery = spawnx+100, spawny
        elif spawny==0:
            self.rect.centerx, self.rect.centery = spawnx, spawny+100
        elif spawnx==1200:
            self.rect.centerx, self.rect.centery = spawnx-100, spawny
        elif spawny==600:
            self.rect.centerx, self.rect.centery = spawnx, spawny-100

    def update(self, playerx, playery, enemyBullets, enemies, health):
        self.bulletTimer-=1
        if self.bulletTimer==0:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            enemies.add(Rocket(self.rect.centerx, self.rect.centery))
            self.bulletTimer=self.attackSpeed

    def collision(self,enemy,enemies,player,score,money,health,splatters,explosions):
        health.update(0)
        
class Rocket (Enemy):
    health = 1
    speed = 7
    attackSpeed=60
    attackPower=10
    attackTimer=0

    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('rocket.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def attack(self,health):
        ouch = load_sound('ouch.wav')
        health.update(-self.attackPower)
        ouch.play()
        self.die()

    def hurt(self,enemy,damage,player,score,money,health,enemies,splatters,explosions):
        splat = load_sound('splat.wav')
        splat.play()
        enemy.health -= damage
        if self.health <= 0:
            enemy.die()
    def die(self):
        self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    penetration = 1
    damage = 1
    speed = 15
    
    def __init__(self, turretx, turrety, playerx, playery, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet.png', -1)
        self.rect.centerx, self.rect.centery = turretx, turrety
        self.image = pygame.transform.rotate(self.image, angle)
        self.movex = self.speed*math.cos(angle*math.pi/180)
        self.movey = self.speed*math.sin(angle*math.pi/180)*-1

    def update(self):
        self.rect = self.rect.move(self.movex,self.movey)
        x = self.rect.centerx
        y = self.rect.centery
        if x < 0 or y < 0 or x > 1200 or y > 600:
            self.kill()

    def collision(self,health):
        ouch = load_sound('ouch.wav')
        self.kill()
        health.update(-1)
        ouch.play()
        

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


class Splatter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('blood.png', -1)
        self.rect.centerx, self.rect.centery = x, y
        self.life = 12

    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()

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
        mana.update(-10)
        health.update(10)

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

class costImage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
    def costDisplay(self, cost, level):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.update(0)
        if level==4:
            self.msg = "Complete"
        else:
            self.msg = "Cost: %d" % cost
        self.image = self.font.render(self.msg, 0, self.color)
        self.rect = self.image.get_rect().move(self.x, self.y)
        
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
                self.owner.health += 1
                self.owner.maxHealth += 1
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
                self.owner.healthRegen += 1
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

class playGameButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('playGameButton.png', 1)
        self.rect.topleft = 10, 390

class exitButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('exitButton.png', 1)
        self.rect.topleft = 220, 390

class mainMenuButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('mainmenuButton.png', 1)
        self.rect.topleft = 10, 390

class upgradeScreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('upgradeScreenButton.png', 1)
        self.rect.topleft = 10, 10

class magicScreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('magicScreenButton.png', 1)
        self.rect.topleft = 220, 10

class weaponScreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('weaponScreenButton.png', 1)
        self.rect.topleft = 430, 10

class backButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('backButton.png', 1)
        self.rect.topleft = 990, 340
        
def findAngle(firstx, firsty, secondx, secondy):
    if firstx<secondx and firsty>secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)
    elif firstx>secondx and firsty>secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)+180
    elif firstx>secondx and firsty<secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)-180
    elif firstx<secondx and firsty<secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)
    elif firstx==secondx and firsty==secondy:
        angle = 0
    elif firstx==secondx and firsty>secondy:
        angle = 90
    elif firstx==secondx and firsty<secondy:
        angle = -90
    elif firstx>secondx and firsty==secondy:
        angle = 360
    elif firstx<secondx and firsty==secondy:
        angle = 180
    return angle

def findDistance(firstx, firsty, secondx, secondy):
    return math.sqrt(math.pow(secondx-firstx,2)+math.pow(secondy-firsty,2))
    
    
def main():
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
   pygame.mixer.music.play()

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
              reloadTimer=weapon.startReload(player,pistol,machineGun,shotGun)#auto reload when clip is empty and try to fire

        #regenerate health
          healthRegenTimer+=player.healthRegen
          if healthRegenTimer>=3600 and player.health<player.maxHealth:
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
          enemies.update(player.rect.centerx, player.rect.centery, enemyBullets, enemies, health)
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
                 bottomspritesdraw(screen)
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
