import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *

MAX_VERT_DISTANCE = 200
MAX_HORIZ_DISTANCE = 900
JUMP_FREQUENCY = 1

class Enemy2(Player,pygame.sprite.Sprite):

        #constructor
        def __init__(self,x,y,playerId):
            #super constructor
            super().__init__(x,y)
            self.symbol = "e2"

            #time since last shot
            self.lastShotTime = time.time()
            self.lastJumpTime = time.time()

            #health
            difficulty = getDifficulty(playerId)
            self.health = 50 * (difficulty + 1)

            #shooting frequency
            self.shooting_frequency = 2

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
                if player.rect.bottom < self.rect.top and time.time() - self.lastJumpTime > JUMP_FREQUENCY:
                    self.lastJumpTime = time.time()
                    if random.randint(0,1) == 1 :
                        up = True

            super().update(up, down, left, right, shooting, shootUp, world)
