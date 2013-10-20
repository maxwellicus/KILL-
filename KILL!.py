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
       self.health = 5
       self.mana = 3
       self.money = 0
       self.score = 0
       self.maxHealth = 5
       self.maxMana = 3
       self.speed = 3
       self.refireRate = 2
       self.numberOfShots = 1
       self.healthRegen = 1
       self.manaRegen = 1
       self.spell=3
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
        self.rect = self.image.get_rect().move(10, 560)

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
        self.rect = self.image.get_rect().move(10, 510)

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
        #self.health=3
        #self.maxHealth=3

    def update(self,change):
        self.owner.health += change

    def show(self):
        self.font = pygame.font.Font(None, 40)
        msg = "Health: %d/%d" % (self.owner.health,self.owner.maxHealth)
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 460)

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
        self.rect = self.image.get_rect().move(10, 410)

    def post(self):
        self.font = pygame.font.Font(None, 100)
        msg = "Mana: %d/%d" % (self.owner.mana, self.owner.maxMana)
        self.rect = self.image.get_rect().move(600, 500)
        self.image = self.font.render(msg, 0, self.color)

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
    
    def update(self, playerx, playery, enemyBullets, second, enemies):
        angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
        self.movex = self.speed*math.cos(angle*math.pi/180)
        self.movey = self.speed*math.sin(angle*math.pi/180)*-1
        self.rect = self.rect.move(self.movex,self.movey)

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
        
        maxEnemy=76
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
        elif enemy<=maxEnemy:
            return RocketTurret(x,y)
        else:
            return 0
        #if enemy<=maxEnemy:
            #return Seeker(x,y)
        

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
        ouch = load_sound('ouch.wav')
        enemy.kill()
        health.update(-1)
        splatters.add(Splatter(enemy.rect.centerx, enemy.rect.centery))
        ouch.play()
    
class Zombie(Enemy):
    """ basic Zombie enemy """
    health = 3
    speed = 3
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('zombie.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

class Runner(Enemy):
    """ basic Runner enemy """
    health = 1
    speed = 7
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('runner.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

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

    def update(self, playerx, playery, enemyBullets, second, enemies):
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
        health.update(-1)
        explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery,player,score,money,health,enemy,enemies,splatters,explosions))
        ouch.play()
    
class Arrow(Enemy):
    health = 1
    speed = 20
    
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('arrow.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny
        self.movex=0
        self.movey=0
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

    def update(self, playerx, playery, enemyBullets, second, enemies):
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
        

class Seeker(Enemy):
    health = 1
    speed = 20
    
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('arrow.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny
        self.angle=0
        if spawnx==0:
            self.angle=90
            self.image=pygame.transform.rotate(self.image,self.angle)
        elif spawnx==1200:
            self.angle=-90
            self.image=pygame.transform.rotate(self.image,self.angle)
        elif spawny==0:
            self.angle=180
            self.image=pygame.transform.rotate(self.image,self.angle)
        elif spawny==600:
            self.angle=360
            

    def update(self, playerx, playery, enemyBullets, second, enemies):
        playerAngle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
        if self.rect.centerx<=0 or self.rect.centerx>=1200 or self.rect.centery<=0 or self.rect.centery>=600:
            self.angle+=1
            self.image=pygame.transform.rotate(self.image,1)
        if self.angle<=playerAngle+10 or self.angle>=playerAngle-10:
            self.movex = self.speed*math.cos(self.angle*math.pi/180)
            self.movey = self.speed*math.sin(self.angle*math.pi/180)*-1
        if self.rect.centerx>=0 or self.rect.centerx<=1200 or self.rect.centery>=0 or self.rect.centery<=600:
            self.movex = self.speed*math.cos(self.angle*math.pi/180)
            self.movey = self.speed*math.sin(self.angle*math.pi/180)*-1
            

class PregnantBitch(Enemy):
    health = 5
    speed = 2
    
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

class Baby(Enemy):
    health = 1
    speed = 15
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('baby.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

class BlobLarge(Enemy):
    health = 5
    speed = 2
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

class BlobMedium(Enemy):
    health = 3
    speed = 3
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

class BlobSmall(Enemy):
    health = 1
    speed = 4
    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('BlobSmall.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

class BulletTurret(Enemy):
    health = 5
    speed = 0
    
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

    def update(self, playerx, playery, enemyBullets, second, enemies):
        if second==0:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            enemyBullets.add(Bullet(self.rect.centerx, self.rect.centery, playerx, playery, angle))

class RocketTurret(Enemy):
    health = 5
    speed = 0
    
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

    def update(self, playerx, playery, enemyBullets, second, enemies):
        if second==0:
            gunshot = load_sound('gunshot.wav')
            gunshot.play()
            angle = findAngle(self.rect.centerx, self.rect.centery, playerx, playery)
            enemies.add(Rocket(self.rect.centerx, self.rect.centery))

class Rocket (Enemy):
    health = 1
    speed = 7

    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('rocket.png', -1)
        self.rect.centerx, self.rect.centery = spawnx, spawny

    def die(self,enemy,enemies,player,score,money,health,splatters,explosions):
        enemy.kill()

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
    speed = 20
    
    def __init__(self, playerx, playery, crossx, crossy, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet.png', -1)
        self.rect.centerx, self.rect.centery = playerx, playery
        self.image = pygame.transform.rotate(self.image, angle)
        self.movex = self.speed*math.cos(angle*math.pi/180)
        self.movey = self.speed*math.sin(angle*math.pi/180)*-1

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
            bullets.add(Bullet(player.rect.centerx, player.rect.centery, crosshair.rect.centerx, crosshair.rect.centery, bulletAngle))
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

    def collision(self,health):
        ouch = load_sound('ouch.wav')
        self.kill()
        health.update(-1)
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

class Magic(pygame.sprite.Sprite):
    """ super class for all magic """
    level = 0
    pictures = []
    
    def __init__(self, owner, costsGroup):
        pygame.sprite.Sprite.__init__(self)
        self.costsGroup = costsGroup
        self.owner = owner
        self.owner.spell=3

    #def show(self):
        #self.image, self.rect = load_image('airStrike.png')
        #self.rect.topleft = 220, 340
        #self.costSprite.costDisplay(self.price, self.level)

    def chooseSpell(self,airstrike,heal,teleport,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        if player.mana>0:
            if self.owner.spell==1:
                airstrike.use(crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)
            elif self.owner.spell==2 and player.health<player.maxHealth:
                heal.use(crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)    
            elif self.owner.spell==3:
                teleport.use(crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)


class AirStrikeMagic(Magic):
    price=10
    def __init__(self, owner, costsGroup):
        super(AirStrikeMagic, self).__init__(owner, costsGroup)
        self.costSprite = costImage(220, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def equip(self):
        self.owner.spell=1
        self.show()
        #self.rect.topleft = 220, 340
        #explosion = load_sound('explosion.wav')
        #explosion.play()

    def use(self,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        mana.update(-1)
        explosions.add(Explosion(crosshair.rect.centerx, crosshair.rect.centery,player,score,money,health,enemy,enemies,splatters,explosions))

    def show(self):
        if self.owner.spell==1:
            self.image, self.rect = load_image('airStrike.eqipped.png')
        else:
            self.image, self.rect = load_image('airStrike.png')
        self.rect.topleft = 220, 340
        self.costSprite.costDisplay(self.price, self.level)

    #def revert(self):
        #self.level=0
        #self.price=10
        #self.show()
        #self.rect.topleft = 10, 40

    #def upgrade(self):
        #try:
            #if self.owner.money >= self.price:
                #self.level+=1
                #self.owner.money -= self.price
                #self.price *= 2
                #self.show()
                #self.owner.health += 1
                #self.owner.maxHealth += 1
                #self.rect.topleft = 10, 40
        #except StopIteration:
            #return

    #def costDisplay(self):
        #super(maxHealthUpgrade, self).costDisplay()
        #self.image = self.font.render(self.msg, 0, self.color)
        #self.rect = self.image.get_rect().move(500, 500)

class HealMagic(Magic):
    price=10
    def __init__(self, owner, costsGroup):
        super(HealMagic, self).__init__(owner, costsGroup)
        self.costSprite = costImage(430, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def equip(self):
        self.owner.spell=2
        self.show()

    def use(self,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        mana.update(-1)
        health.update(1)

    def show(self):
        if self.owner.spell==2:
            self.image, self.rect = load_image('heal.equipped.png')
        else:
            self.image, self.rect = load_image('heal.png')
        self.rect.topleft = 430, 340
        self.costSprite.costDisplay(self.price, self.level)

class TeleportMagic(Magic):
    price=10
    def __init__(self, owner, costsGroup):
        super(TeleportMagic, self).__init__(owner, costsGroup)
        self.costSprite = costImage(640, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()

    def equip(self):
        self.owner.spell=3
        self.show()

    def use(self,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions):
        mana.update(-1)
        player.rect.centerx=crosshair.rect.centerx
        player.rect.centery=crosshair.rect.centery

    def show(self):
        if self.owner.spell==3:
            self.image, self.rect = load_image('teleport.equipped.png')
        else:
            self.image, self.rect = load_image('teleport.png')
        self.rect.topleft = 640, 340
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
        self.costSprite = costImage(850, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 850, 340
        
    def revert(self):
        self.level=0
        self.price=10
        self.show()
        self.rect.topleft = 850, 340

    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.mana += 1
                self.owner.maxMana += 1
                self.rect.topleft = 850, 340
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
        self.costSprite = costImage(1060, 310)
        self.costSprite.costDisplay(self.price, self.level)
        self.costSprite.add(self.costsGroup)
        self.show()
        self.rect.topleft = 1060, 340

    def revert(self):
        self.level=0
        self.price=5
        self.show()
        self.rect.topleft = 1060, 340
        
    def upgrade(self):
        try:
            if self.owner.money >= self.price:
                self.level+=1
                self.owner.money -= self.price
                self.price *= 2
                self.show()
                self.owner.manaRegen += 1
                self.rect.topleft = 1060, 340
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

class mainMenuButton(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('mainmenuButton.png', 1)
        self.rect.topleft = 100, 390
        
        
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
    
    
def main():
#initializing
   pygame.init()
   window = pygame.display.set_mode((1200, 600))
   pygame.display.set_caption('KILL!')
   screen = pygame.display.get_surface()
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
   costs = pygame.sprite.Group()
   mainMenuButtons = pygame.sprite.Group()
   deathScreenButtons = pygame.sprite.Group()

#initialize buttons
   playGame=playGameButton()
   mainMenuButtons.add(playGame)
   mainMenu=mainMenuButton()
   deathScreenButtons.add(mainMenu)

#initialize upgrades
   upgrade=Upgrade(player,costs)
   maxHealth=maxHealthUpgrade(player, costs)
   upgrades.add(maxHealth)
   refireRate=refireRateUpgrade(player,costs)
   upgrades.add(refireRate)
   movementSpeed=movementSpeedUpgrade(player,costs)
   upgrades.add(movementSpeed)
   numberOfShots=numberOfShotsUpgrade(player,costs)
   upgrades.add(numberOfShots)
   healthRegen=healthRegenUpgrade(player,costs)
   upgrades.add(healthRegen)
   maxMana=maxManaUpgrade(player,costs)
   upgrades.add(maxMana)
   manaRegen=manaRegenUpgrade(player,costs)
   upgrades.add(manaRegen)

#initialize spells
   magic=Magic(player,costs)
   airStrike=AirStrikeMagic(player,costs)
   spells.add(airStrike)
   heal=HealMagic(player,costs)
   spells.add(heal)
   teleport=TeleportMagic(player,costs)
   spells.add(teleport)

#initialize groups
   score = Score(player)
   money = Money(player)
   health = Health(player)
   mana = Mana(player)
   bullet = Bullet(-100,-100,-100,-100,1)
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
                   if pygame.sprite.collide_rect(crosshair, button):
                       
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
             if event.type == MOUSEBUTTONDOWN and event.button==3:
                 magic.chooseSpell(airStrike,heal,teleport,crosshair,player,score,money,health,mana,enemy,enemies,splatters,explosions)
                     

        #spawn enemies
          spawner = enemy.spawn(second, spawner, enemies)

       #detect collision
          for enemy in enemies:
              if pygame.sprite.collide_rect(enemy, player):
                  enemy.collision(enemy,enemies,player,score,money,health,splatters,explosions)
                  if(player.health<=0):
                      wilhelm.play()
                      dead=1
                                  
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

       #fire gun
          bulletTimer+=1
          if fire==1:
              if bulletTimer>=60/(2*player.refireRate):
                  bulletTimer=0
                  bullet.fire(player,bullets,crosshair)

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
           
       #update everything
          enemies.update(player.rect.centerx, player.rect.centery, enemyBullets, second, enemies)
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

       #Draw Everything
          bottomsprites = pygame.sprite.RenderPlain((player, bullets, enemies, splatters, explosions, enemyBullets))
          topSprite = pygame.sprite.RenderPlain((crosshair, score, money, health, mana))
          screen.blit(background_surface, (0,0))
          bottomsprites.draw(screen)
          topSprite.draw(screen)
          pygame.display.flip()

        #Pause Screen Loop
          while pause==1:
             clock.tick(60)
             crosshair.update()
             for event in pygame.event.get():
                 if event.type == QUIT:
                     pygame.quit()
                 if event.type == KEYDOWN:
                     if event.key == K_p or event.key == K_ESCAPE or event.key == K_SPACE:
                         pause=0
                 elif event.type == MOUSEBUTTONDOWN:
                     for upgrade in upgrades:
                        if pygame.sprite.collide_rect(crosshair, upgrade):
                            upgrade.upgrade()
                     for magic in spells:
                        if pygame.sprite.collide_rect(crosshair, magic):
                            magic.equip()
                            
             health.show()
             score.show()
             money.show()
             screen.blit(pauseBackground_surface, (0,0))
             bottomsprites = pygame.sprite.RenderPlain((upgrades, spells, costs, score, money, health, mana))
             bottomsprites.draw(screen)
             topSprite = pygame.sprite.RenderPlain((crosshair))
             topSprite.draw(screen)
             pygame.display.flip()

          #Death Screen Loop
          while dead==1:
             clock.tick(60)
             crosshair.update()
             score.post()
             money.post()
             health.post()
             mana.post()
             bottomSprites = pygame.sprite.RenderPlain((bullets,enemies,splatters,explosions))
             mediumSprites = pygame.sprite.RenderPlain((player))
             topSprites = pygame.sprite.RenderPlain((score,money,health,mana,mainMenu))
             crosshairSprite = pygame.sprite.RenderPlain((crosshair))
             screen.blit(background_surface, (0,0))
             bottomSprites.draw(screen)
             mediumSprites.draw(screen)
             topSprites.draw(screen)
             crosshairSprite.draw(screen)
             pygame.display.flip()
             for event in pygame.event.get():
                 if event.type == QUIT:
                     pygame.quit()
                 elif event.type == MOUSEBUTTONDOWN:
                     for button in deathScreenButtons:
                         if pygame.sprite.collide_rect(crosshair, button):
                             dead=0
                             game=0
                        #empty groups
                             bullets.empty()
                             enemies.empty()
                             splatters.empty()
                             explosions.empty()
                             enemyBullets.empty()

if __name__ == '__main__': main()
