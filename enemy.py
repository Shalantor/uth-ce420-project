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
DELAY = 1

class Enemy(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y):
        #super constructor
        super().__init__(x,y)
        self.symbol = "e"
        self.stepsTook = 0
        self.lastMoveTime = time.time()

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
        #Else move randomly
        elif time.time() - self.lastMoveTime > DELAY:
            self.lastMoveTime = time.time()
            if self.stepsTook == 0:
                self.currentDirection = (self.currentDirection + 1) % 2
            if self.currentDirection == 0:
                right = True
                self.stepsTook = (self.stepsTook + 1) % MAX_STEPS
            else:
                left = True
                self.stepsTook = (self.stepsTook + 1) % MAX_STEPS

        super().update(up, down, left, right, shooting, world)
