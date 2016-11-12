import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *

SHOOTING_FREQUENCY = 3
MAX_VERT_DISTANCE = 500
MAX_HORIZ_DISTANCE = 200

class Enemy2(Player,pygame.sprite.Sprite):

        #constructor
        def __init__(self,x,y):
            #super constructor
            super().__init__(x,y)
            self.symbol = "e2"

            #time since last shot
            self.lastShotTime = time.time()

            #health
            self.health = 100

        #Override update function
        def update(self,player,world):
            #decide what to do depending on player position
            left = right = up = down = shooting = False
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

            super().update(up, down, left, right, shooting, world,SHOOTING_FREQUENCY)
