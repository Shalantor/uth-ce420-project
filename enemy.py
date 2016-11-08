import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *

MAX_VERT_DISTANCE = 300
MAX_HORIZ_DISTANCE = 300
MAX_STEPS = 4
MAX_IDLE_TIME = 2
MAX_MOVE_TIME = 0.5
DURATION = 1

class Enemy(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y):
        #super constructor
        super().__init__(x,y)
        self.symbol = "e"
        self.stepsTook = 0
        self.standTime = time.time()
        self.standing = True
        self.startMoveTime = 0

        #Direction facing 0 for right, 1 for left
        self.currentDirection = 1

    #Override update function
    def update(self,player,world):
        #decide what to do depending on where the player stands
        #If player near move towards him for example
        playerX = player.rect.centerx
        playerY = player.rect.centery
        left = right = up = down = shooting = False
        if abs(playerX - self.rect.centerx) < MAX_HORIZ_DISTANCE and abs(playerY - self.rect.centery) < MAX_VERT_DISTANCE:
            if playerX < self.rect.centerx :
                left = True
            elif playerX > self.rect.centerx:
                right = True
        elif self.standing : #Stand still
            left = right = False
            if time.time() - self.standTime > MAX_IDLE_TIME:
                self.standing = False
                self.startMoveTime = time.time()
        else:   #Move right or left for a while
            if self.currentDirection == 0:
                right = True
            else:
                left = True
            #check for end
            if time.time() - self.startMoveTime > MAX_MOVE_TIME:
                self.currentDirection = (self.currentDirection + 1) % 2
                self.standing = True
                self.standTime = time.time()


        super().update(up, down, left, right, shooting, world)
