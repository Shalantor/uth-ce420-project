import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time
from player import *

class Enemy(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y):
        #super constructor
        super().__init__(x,y)
        self.symbol = "e"
