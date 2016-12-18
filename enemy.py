import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *
from databaseUtils import *

MAX_VERT_DISTANCE = 300
MAX_HORIZ_DISTANCE = 300
MAX_IDLE_TIME = 2
MAX_MOVE_TIME = 0.5
MIN_DISTANCE = 10
JUMP_FREQUENCY = 1

class Enemy(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y,playerId):
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
        difficulty = getDifficulty(playerId)
        self.health = 50 * (difficulty + 1)

        #movement speed
        self.horiz_mov_incr = 3

        #Load images
        self.jump_left = ["megaman/enemy/jump_left/jl1.png","megaman/enemy/jump_left/jl2.png",
                         "megaman/enemy/jump_left/jl3.png","megaman/enemy/jump_left/jl4.png"]

        self.jump_right = ["megaman/enemy/jump_right/jr1.png","megaman/enemy/jump_right/jr2.png",
                         "megaman/enemy/jump_right/jr3.png","megaman/enemy/jump_right/jr4.png"]

        self.shootLeft = ["megaman/enemy/shoot_left/s_l1.png","megaman/enemy/shoot_left/s_l2.png",
                          "megaman/enemy/shoot_left/s_l3.png","megaman/enemy/shoot_left/s_l4.png","megaman/enemy/shoot_left/s_l5.png"]

        self.shootRight = ["megaman/enemy/shoot_right/s_r1.png","megaman/enemy/shoot_right/s_r2.png",
                          "megaman/enemy/shoot_right/s_r3.png","megaman/enemy/shoot_right/s_r4.png","megaman/enemy/shoot_right/s_r5.png"]

        self.standLeft = ["megaman/enemy/stand/s_l.png"]
        self.standRight = ["megaman/enemy/stand/s_r.png"]

        self.run_left = ["megaman/enemy/move_left/e1.png","megaman/enemy/move_left/e2.png",
                         "megaman/enemy/move_left/e3.png", "megaman/enemy/move_left/e4.png",
                         "megaman/enemy/move_left/e5.png", "megaman/enemy/move_left/e6.png",
                         "megaman/enemy/move_left/e7.png", "megaman/enemy/move_left/e8.png","megaman/enemy/move_left/e9.png"]

        self.run_right = ["megaman/enemy/move_right/e1.png","megaman/enemy/move_right/e2.png",
                         "megaman/enemy/move_right/e3.png", "megaman/enemy/move_right/e4.png",
                         "megaman/enemy/move_right/e5.png", "megaman/enemy/move_right/e6.png",
                         "megaman/enemy/move_right/e7.png", "megaman/enemy/move_right/e8.png","megaman/enemy/move_right/e9.png"]

        #Set number of frames
        self.stand_frames = 1
        self.run_frames = 9
        self.jump_frames = 4
        self.shoot_frames = 5


    #Override update function
    def updateEnemy(self,player,world):
        #decide what to do depending on where the player stands
        #If player near move towards him for example
        left = right = up = down = shooting = shootUp = combo = False
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


        super().update(up, down, left, right, shooting, shootUp, combo, world)
