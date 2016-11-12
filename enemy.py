import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *

MAX_VERT_DISTANCE = 300
MAX_HORIZ_DISTANCE = 300
MAX_IDLE_TIME = 2
MAX_MOVE_TIME = 0.5
DURATION = 1
SPEED = 5
MIN_DISTANCE = 10
JUMP_FREQUENCY = 1

class Enemy(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y):
        #super constructor
        super().__init__(x,y)
        self.symbol = "e1"

        #Variables used for idle enemy movement
        self.standTime = time.time()
        self.standing = True
        self.startMoveTime = 0

        #Direction facing 0 for right, 1 for left
        self.currentDirection = 1

        #Lets player jump only some times
        self.lastJumpTime = time.time()

        #health
        self.health = 100


    #Override update function
    def update(self,player,world):
        #decide what to do depending on where the player stands
        #If player near move towards him for example
        left = right = up = down = shooting = False
        horizDiff = abs(player.rect.centerx - self.rect.centerx)
        vertDiff = abs(player.rect.centery - self.rect.centery)
        if horizDiff < MAX_HORIZ_DISTANCE and vertDiff < MAX_VERT_DISTANCE:
            if horizDiff < MIN_DISTANCE :
                self.standing = True
            elif player.rect.centerx < self.rect.centerx :
                left = True
                if time.time() - self.lastJumpTime > JUMP_FREQUENCY:
                    up = bool(random.getrandbits(1))
                    self.lastJumpTime = time.time()
            elif player.rect.centerx > self.rect.centerx:
                right = True
                if time.time() - self.lastJumpTime > JUMP_FREQUENCY:
                    up = bool(random.getrandbits(1))
                    self.lastJumpTime = time.time()
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


        super().update(up, down, left, right, shooting, world, speed = SPEED)
