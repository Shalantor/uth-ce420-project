import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *

MAX_VERT_DISTANCE = 200
MAX_HORIZ_DISTANCE = 100
MAX_HEIGT_MULTIPLICATOR = 3
MAX_HORIZONTAL_MULTIPLICATOR = 3
SHOOTING_FREQUENCY = 1
SPEED = 3
MAX_STEPS = 20
STAY_IDLE_TIME = 1

class Enemy3(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y):
        #super constructor
        super().__init__(x,y)
        self.symbol = "e3"
        self.canFly = True

        #time since last shot
        self.lastShotTime = time.time()

        self.startHeight = self.rect.top
        self.stepsRemaining = 0
        self.lastMove = "up"
        self.idleTime = time.time()

        self.health = 100

    #Override update function
    def update(self,player,world):
        #decide what to do depending on player position
        left = right = up = down = shooting = shootUp =  False
        horizDiff = abs(player.rect.centerx - self.rect.centerx)
        vertDiff = abs(player.rect.centery - self.rect.centery)

        #Player is near
        if horizDiff < MAX_HORIZ_DISTANCE and vertDiff < MAX_VERT_DISTANCE:
            #turn to player
            if player.rect.center >= self.rect.center:
                if self.direction != "right":
                    self.direction = "right"
                    right = True
            elif player.rect.center < self.rect.center:
                if self.direction != "left":
                    self.direction = "left"
                    left = True
            shooting = True
            #Now move to height of player
            if player.rect.centery >= self.rect.centery:
                down = True
            if player.rect.centery < self.rect.centery:
                up = True
        #Idle movement
        else:
            if self.stepsRemaining == 0:
                self.idleTime = time.time()
                doWhat = ["up","down","left","right"]
                self.lastMove = random.choice(doWhat)
                self.stepsRemaining = MAX_STEPS
            if time.time() - self.idleTime >= STAY_IDLE_TIME:
                if self.lastMove == "up":
                    if self.startHeight - MAX_HEIGT_MULTIPLICATOR * self.rect.h <= self.rect.top:
                        up = True
                    self.stepsRemaining -= 1
                elif self.lastMove == "down":
                    down = True
                    self.stepsRemaining -= 1
                elif self.lastMove == "right":
                    right = True
                    self.stepsRemaining -= 1
                else:
                    left = True
                    self.stepsRemaining -= 1




        super().update(up, down, left, right, shooting, shootUp, world, shootTime = SHOOTING_FREQUENCY, speed = SPEED)
