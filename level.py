import pygame
from pygame.locals import *
import sys
from level import *
from player import *
from camera import *
from enemy import *
from enemy2 import *
from enemy3 import *

PLATFORM_STEPS = 30

class Key(pygame.sprite.Sprite):
    '''Class that represents key which player needs to access end level door'''
    def __init__(self,x,y):
        self.symbol = "F"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/star/star1.png").convert()
        self.image = pygame.transform.scale(self.image,(30,30))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class Fountain(pygame.sprite.Sprite):
    '''Class that represents a fountain restoring energy'''
    def __init__(self,x,y):
        self.symbol = "F"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/star/star1.png").convert()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]


class Wings(pygame.sprite.Sprite):
    '''Class that represents wings , to make player fly'''
    def __init__(self,x,y):
        self.symbol = "W"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/star/star1.png").convert()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class higherJump(pygame.sprite.Sprite):
    '''Object for player to collect , so he can jump higher'''
    def __init__(self,x,y):
        self.symbol = "J"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/star/star1.png").convert()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class Spawn(pygame.sprite.Sprite):
    '''Class that represents a spawn point for the player when he dies'''
    def __init__(self,x,y):
        self.symbol = "S"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/star/star1.png").convert()
        self.image = pygame.transform.scale(self.image,(50,80))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class Heart(pygame.sprite.Sprite):
    '''Class for heart that replenishes player health'''
    def __init__(self,x,y):
        self.symbol = "L"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/heart.png").convert()
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        self.healthValue = 30 #TODO:remove hardcoded value

class Coin(pygame.sprite.Sprite):
    '''Class for coins , for player to collect in levels'''
    def __init__(self,x,y):
        self.symbol = "C"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/coin.png").convert()
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]


class Star(pygame.sprite.Sprite):
    '''Class for a star, that makes player invincible for a while'''
    def __init__(self,x,y):
        self.symbol = "I"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("megaman/star/star1.png").convert()
        self.image = pygame.transform.scale(self.image,(30,30))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        self.starFrames = 8
        self.curFrame = 0
        self.lastSpinTime = time.time()
        self.spinFrequency = 0.1
        self.starImages = ["megaman/star/star1.png","megaman/star/star2.png",
                           "megaman/star/star3.png","megaman/star/star4.png",
                           "megaman/star/star5.png","megaman/star/star6.png",
                           "megaman/star/star7.png","megaman/star/star8.png"]

    def update(self):
        if time.time() - self.lastSpinTime > self.spinFrequency:
            oldCenter = self.rect.center
            self.curFrame = (self.curFrame + 1) % self.starFrames
            self.image = pygame.image.load(self.starImages[self.curFrame])
            if self.curFrame == 2 or self.curFrame == 4:
                self.image = pygame.transform.scale(self.image,(30,40))
            elif self.curFrame == 3:
                self.image = pygame.transform.scale(self.image,(15,40))
            else:
                self.image = pygame.transform.scale(self.image,(40,40))
            self.image.set_colorkey((255,255,255))
            self.lastSpinTime = time.time()
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter


class BreakableBlock(pygame.sprite.Sprite):
    '''Class for breakable blocks'''
    def __init__(self,x,y):
        self.symbol = "B"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("world/obstacle.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

class PlatformHorizontal(pygame.sprite.Sprite):
    '''Class for platforms that move horizontally'''
    def __init__(self,x,y):
        self.symbol = "H"
        self.x = x - 25
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("world/obstacle.png").convert()
        self.image = pygame.transform.scale(self.image,(75,25))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        self.maxLeft = self.rect.left - self.rect.w
        self.maxRight = self.rect.left + self.rect.w
        self.speed = (self.maxRight - self.maxLeft) // PLATFORM_STEPS
        self.direction = "right"

    #Makes platform move right and left periodically
    #Platforms must move the player with them as well
    def move(self,player):
        onPlatform = False
        if self.direction == "right":
            if player.rect.bottom == self.rect.top and player.rect.left < self.rect.right and player.rect.right > self.rect.left:
                player.rect.left += self.speed
                onPlatform = True
            self.rect.left += self.speed
            if self.rect.left >= self.maxRight:
                self.rect.left = self.maxRight
                self.direction = "left"
            #If colliding with player, push player to right
            if player.rect.colliderect(self.rect):
                player.rect.left = self.rect.right
        elif self.direction == "left":
            if player.rect.bottom == self.rect.top and player.rect.left < self.rect.right and player.rect.right > self.rect.left:
                player.rect.left -= self.speed
                onPlatform = True
            self.rect.left -= self.speed
            if self.rect.left <= self.maxLeft:
                self.rect.left = self.maxLeft
                self.direction = "right"
            #if colliding with player, push player to left
            if player.rect.colliderect(self.rect):
                player.rect.right = self.rect.left


class PlatformVertical(pygame.sprite.Sprite):
    '''Class for platforms that move vertically'''
    def __init__(self,x,y):
        self.symbol = "V"
        self.x = x - 25
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("world/obstacle.png").convert()
        self.image = pygame.transform.scale(self.image,(75,25))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        self.maxTop = self.y - 3 * self.rect.h
        self.minTop = self.y + 3 * self.rect.h
        self.speed = (self.minTop - self.maxTop) // PLATFORM_STEPS
        self.direction = "up"

    #Makes platform move up and down periodically
    #Platforms must move the player with them as well
    def move(self,player):
        onPlatform = False
        if self.direction == "up":
            #Check if player is on platform
            if player.rect.bottom == self.rect.top and player.rect.left < self.rect.right and player.rect.right > self.rect.left:
                player.rect.top -= self.speed
                onPlatform = True
            self.rect.top -= self.speed
            if self.rect.top <= self.maxTop:
                self.rect.top = self.maxTop
                if onPlatform:
                    player.rect.bottom = self.rect.top
                self.direction = "down"
        elif self.direction == "down":
            #check if player is on platform
            if player.rect.bottom == self.rect.top and player.rect.left < self.rect.right and player.rect.right > self.rect.left:
                player.rect.top += self.speed
                onPlatform = True
            self.rect.top += self.speed

            #Check if platform has hit player from top
            if self.rect.colliderect(player.rect):
                if player.contact:
                    self.direction = "up"
                    self.rect.bottom = player.rect.top
                else:
                    player.rect.top += self.speed

            if self.rect.top >= self.minTop:
                self.rect.top = self.minTop
                if onPlatform:
                    player.rect.bottom = self.rect.top
                self.direction = "up"


class Obstacle(pygame.sprite.Sprite):
    '''Class for create obstacles'''
    def __init__(self, x, y):
        self.symbol = "X"
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("world/obstacle.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]


class Level(object):
    '''Read a map and create a level'''
    def __init__(self, open_level):
        self.level1 = []
        self.world = []
        self.enemies= []
        self.platformsVertical = []
        self.platformsHorizontal = []
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")
        self.foundEnemy = False
        self.enemies2 = []
        self.enemies3 = []
        self.breakBlocks = []
        self.stars = []
        self.coins = []
        self.hearts = []
        self.spawnPoints = []
        self.wings = []
        self.jumpBoosts = []
        self.fountains = []
        self.keys = []

    def create_level(self, x, y,playerId):
        for l in self.level:
            self.level1.append(l)

        for row in self.level1:
            for col in row:
                if col == "X":
                    obstacle = Obstacle(x, y)
                    self.world.append(obstacle)
                    self.all_sprite.add(self.world)
                elif col == "P":
                    self.player = Player(x,y)
                    self.all_sprite.add(self.player)
                elif col == "E":
                    self.foundEnemy = True
                elif col == "1" and self.foundEnemy:
                    self.foundEnemy = False
                    enemy = Enemy(x-25,y,playerId)
                    self.enemies.append(enemy)
                    self.all_sprite.add(self.enemies)
                elif col == "2" and self.foundEnemy:
                    self.foundEnemy = False
                    enemy = Enemy2(x-25,y,playerId)
                    self.enemies2.append(enemy)
                    self.all_sprite.add(self.enemies2)
                elif col == "3" and self.foundEnemy:
                    self.foundEnemy = False
                    enemy = Enemy3(x-25,y,playerId)
                    self.enemies3.append(enemy)
                    self.all_sprite.add(self.enemies3)
                elif col == "V":
                    platformV = PlatformVertical(x,y)
                    self.platformsVertical.append(platformV)
                    self.world.append(platformV)
                    self.all_sprite.add(self.platformsVertical)
                elif col == "H":
                    platformH = PlatformHorizontal(x,y)
                    self.platformsHorizontal.append(platformH)
                    self.world.append(platformH)
                    self.all_sprite.add(self.platformsHorizontal)
                elif col == "B":
                    breakBlock = BreakableBlock(x,y)
                    self.breakBlocks.append(breakBlock)
                    self.world.append(breakBlock)
                    self.all_sprite.add(self.breakBlocks)
                elif col == "I":
                    star = Star(x,y)
                    self.stars.append(star)
                    self.all_sprite.add(self.stars)
                elif col == "C":
                    coin = Coin(x,y)
                    self.coins.append(coin)
                    self.all_sprite.add(self.coins)
                elif col == "L":
                    heart = Heart(x,y)
                    self.hearts.append(heart)
                    self.all_sprite.add(self.hearts)
                elif col == "S":
                    spawnPoint = Spawn(x,y)
                    self.spawnPoints.append(spawnPoint)
                    self.all_sprite.add(self.spawnPoints)
                elif col == "W":
                    wings = Wings(x,y)
                    self.wings.append(wings)
                    self.all_sprite.add(self.wings)
                elif col == "J":
                    jumpBoost = higherJump(x,y)
                    self.jumpBoosts.append(jumpBoost)
                    self.all_sprite.add(self.jumpBoosts)
                elif col == "F":
                    fountain = Fountain(x,y)
                    self.fountains.append(fountain)
                    self.all_sprite.add(self.fountains)
                elif col == "K":
                    key = Key(x,y)
                    self.keys.append(key)
                    self.all_sprite.add(self.keys)
                x += 25
            y += 25
            x = 0

    def get_size(self):
        lines = self.level1
        #line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)
