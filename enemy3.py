import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time,random
from player import *

MAX_VERT_DISTANCE = 200
MAX_HORIZ_DISTANCE = 500
MAX_HEIGHT_MULTIPLICATOR = 3
MAX_HORIZONTAL_MULTIPLICATOR = 3
MAX_STEPS = 20
STAY_IDLE_TIME = 1

class Enemy3(Player,pygame.sprite.Sprite):

    #constructor
    def __init__(self,x,y,playerId):
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

        difficulty = getDifficulty(playerId)
        self.health = 50 * (difficulty + 1)
        self.horiz_mov_incr = 3
        self.shooting_frequency = 1
        self.damage = (difficulty + 1) * 10

        self.projectileImage = pygame.image.load("megaman/enemy3/fire.png").convert()
        self.projectileImage.set_colorkey(None)

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
        #decide what to do depending on player position
        left = right = up = down = shooting = shootUp = combo = False
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
                    if self.startHeight - MAX_HEIGHT_MULTIPLICATOR * self.rect.h <= self.rect.top:
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

        super().update(up, down, left, right, shooting, shootUp, combo, world)
