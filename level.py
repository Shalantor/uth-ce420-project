import pygame
from pygame.locals import *
import sys
from level import *
from player import *
from camera import *
from enemy import *

PLATFORM_STEPS = 30

class PlatformVertical(pygame.sprite.Sprite):
    '''Class for platforms that move vertially'''
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
            if player.rect.bottom == self.rect.top and player.rect.left < self.rect.right and player.rect.right > self.rect.left:
                player.rect.top += self.speed
                onPlatform = True
            self.rect.top += self.speed
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
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")
        self.foundEnemy = False

    def create_level(self, x, y):
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
                elif col == "1":
                    enemy = Enemy(x-25,y)
                    self.enemies.append(enemy)
                    self.all_sprite.add(self.enemies)
                elif col == "V":
                    platformV = PlatformVertical(x,y)
                    self.platformsVertical.append(platformV)
                    self.world.append(platformV)
                    self.all_sprite.add(self.platformsVertical)
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
