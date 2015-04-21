#import things
import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

#create paths to other folders
sys.path.insert(0,'functions')
sys.path.insert(0,'classes')

#import functions
from load_image import load_image
from load_sound import load_sound
from findAngle import findAngle
from findDistance import findDistance
from splatter import Splatter
from explosion import Explosion
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    """ Generic enemy class, all enemies will inherit from Enemy """

    health = 1
    speed = 1
    attackSpeed=60
    attackPower=1
    attackTimer=0
    collide=0
    distance=999
    
    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
        
        maxEnemy=103
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

        if enemy<=25:
            return Zombie(x, y)
        elif enemy<=50:
            return Runner(x, y)
        elif enemy<=60:
            return Arrow(x,y)
        elif enemy<=70:
            return BombDude(x,y)
        elif enemy<=72:
            return PregnantBitch(x,y)
        elif enemy<=74:
            return BlobLarge(x,y)
        elif enemy<=75:
            return BulletTurret(x,y)
        elif enemy<=76:
            return RocketTurret(x,y)
        elif enemy<=78:
            return Seeker(x,y)
        elif enemy<=maxEnemy:
            return Charger(x,y)
        else:
            return 0

    def hurt(self,enemy,damage,player,score,money,health,enemies,splatters,explosions):
        splat = load_sound('splat.wav')
        splat.play()
        enemy.health -= damage
        if self.health <= 0:
            enemy.die(enemy,enemies,player,score,money,health,splatters,explosions)

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        self.kill()
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
    
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('runner.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny
        
class Charger(Enemy):
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
        self.image, self.rect = load_image('charger.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
    attackPower = 1
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

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
        health.update(-self.attackPower)
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

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
        self.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(self.rect.centerx, self.rect.centery))
        cry = load_sound('cry.wav')
        cry.play()
        for babies in range (1,random.randint(1,3)):
            enemies.add(Baby(self.rect.centerx+random.randint(-100,100), self.rect.centery+random.randint(-100,100)))

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
        self.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(self.rect.centerx, self.rect.centery))
        for blobs in range (1,3):
            enemies.add(BlobMedium(self.rect.centerx+random.randint(-100,100), self.rect.centery+random.randint(-100,100)))

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
        self.kill()
        score.update(1)
        money.update(1)
        splatters.add(Splatter(self.rect.centerx, self.rect.centery))
        for blobs in range (1,3):
            enemies.add(BlobSmall(self.rect.centerx+random.randint(-50,50), self.rect.centery+random.randint(-50,50)))

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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

    def update(self, playerx, playery, enemyBullets, enemies, health, enemy, player, score, money, splatters, explosions):
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
