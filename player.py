import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time

HORIZ_MOV_INCR = 10 #speed of movement
VERTICAL_MOV_INCR = 20
MIN_VERTICAL_SPEED = 15
SHOOTING_FREQUENCY = 0.2
DAMAGE_DELAY = 2
DAMAGE = 10
STAND_FRAMES = 3
STAND_FRAMES_TIME = 0.2
RUN_FRAMES = 16
JUMP_FRAMES = 9
JUMP_FRAMES_TIME = 0.4

class Player(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lastShotTime = 0
        self.symbol = "P"
        self.projectileImage = pygame.image.load("world/obstacle.png").convert()
        self.projectiles = []
        self.coins = 0
        self.canFly = False
        self.isFlying = False
        self.flyDown = False
        self.health = 100
        self.energy = 100
        self.damage = DAMAGE
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.fallSpeed = 0
        self.jumpSpeed = VERTICAL_MOV_INCR
        self.contact = False
        self.jump = False
        self.image = pygame.image.load('actions/idle_right.png').convert()
        self.rect = self.image.get_rect()
        self.maxJumpHeight = self.rect.height * 1.5
        self.lastTimeDamaged = time.time() - DAMAGE_DELAY

        self.jump_left = ["megaman/jump_left/jl1.png","megaman/jump_left/jl2.png",
                         "megaman/jump_left/jl3.png","megaman/jump_left/jl4.png",
                         "megaman/jump_left/jl5.png","megaman/jump_left/jl6.png",
                         "megaman/jump_left/jl7.png","megaman/jump_left/jl8.png","megaman/jump_left/jl9.png"]

        self.jump_right = ["megaman/jump_right/jr1.png","megaman/jump_right/jr2.png",
                         "megaman/jump_right/jr3.png","megaman/jump_right/jr4.png",
                         "megaman/jump_right/jr5.png","megaman/jump_right/jr6.png",
                         "megaman/jump_right/jr7.png","megaman/jump_right/jr8.png","megaman/jump_right/jr9.png"]

        self.run_left = ["megaman/move_left/ml1.png","megaman/move_left/ml2.png",
                         "megaman/move_left/ml3.png", "megaman/move_left/ml4.png",
                         "megaman/move_left/ml5.png", "megaman/move_left/ml6.png",
                         "megaman/move_left/ml7.png", "megaman/move_left/ml8.png",
                         "megaman/move_left/ml9.png","megaman/move_left/ml10.png",
                         "megaman/move_left/ml11.png","megaman/move_left/ml12.png",
                         "megaman/move_left/ml13.png","megaman/move_left/ml14.png",
                         "megaman/move_left/ml15.png","megaman/move_left/ml16.png"]

        self.run_right = ["megaman/move_right/mr1.png","megaman/move_right/mr2.png",
                         "megaman/move_right/mr3.png", "megaman/move_right/mr4.png",
                         "megaman/move_right/mr5.png", "megaman/move_right/mr6.png",
                         "megaman/move_right/mr7.png", "megaman/move_right/mr8.png",
                         "megaman/move_right/mr9.png","megaman/move_right/mr10.png",
                         "megaman/move_right/mr11.png","megaman/move_right/mr12.png",
                         "megaman/move_right/mr13.png","megaman/move_right/mr14.png",
                         "megaman/move_right/mr15.png","megaman/move_right/mr16.png"]

        self.standLeft = ["megaman/stand/sl1.png","megaman/stand/sl2.png","megaman/stand/sl3.png"]
        self.standRight = ["megaman/stand/sr1.png","megaman/stand/sr2.png","megaman/stand/sr3.png"]

        self.standFrame = 0
        self.jumpFrame = 0
        self.lastJumpFrame = time.time()
        self.lastStandFrame = time.time()
        self.direction = "right"
        self.rect.topleft = [x, y]
        self.frame = 0

    def update(self, up, down, left, right, shooting, shootUp, world,  speed = HORIZ_MOV_INCR, shootTime = SHOOTING_FREQUENCY):
        #Check for key presses
        self.isFlying = False
        self.flyDown = False
        if up:
            if self.canFly:
                self.isFlying = True
            if self.contact:
                if self.direction == "right":
                    self.image = pygame.image.load(self.jump_right[self.jumpFrame]).convert()
                    self.image.set_colorkey((255,255,255))
                    if time.time() - self.lastJumpFrame > JUMP_FRAMES_TIME:
                        self.jumpFrame = (self.jumpFrame + 1) % JUMP_FRAMES
                        self.lastJumpFrame = time.time()
                if not self.canFly:
                    self.jump = True
                else:
                    self.isFlying = True
                self.contact = False
        if down:
            if self.contact and self.direction == "right":
                self.image = pygame.image.load('actions/down_right.png').convert_alpha()
            if self.contact and self.direction == "left":
                self.image = pygame.image.load('actions/down_left.png').convert_alpha()
            if self.canFly and not self.contact:
                self.flyDown = True

        if not down and self.direction == "right":
            self.image = pygame.image.load(self.standRight[self.standFrame]).convert()
            self.image.set_colorkey((255,255,255))
            if time.time() - self.lastStandFrame > STAND_FRAMES_TIME:
                self.standFrame = ( self.standFrame + 1 ) % 3
                self.lastStandFrame = time.time()

        if not down and self.direction == "left":
            self.image = pygame.image.load(self.standLeft[self.standFrame]).convert()
            self.image.set_colorkey((255,255,255))
            if time.time() - self.lastStandFrame > STAND_FRAMES_TIME:
                self.standFrame = ( self.standFrame + 1 ) % 3
                self.lastStandFrame = time.time()

        if left:
            self.direction = "left"
            self.movx = -speed
            if self.contact:
                self.frame = (self.frame + 1) % RUN_FRAMES
                self.image = pygame.image.load(self.run_left[self.frame]).convert()
                self.image.set_colorkey((255,255,255))
            else:
                self.image = pygame.image.load(self.jump_left[self.jumpFrame]).convert()
                self.image.set_colorkey((255,255,255))
                if time.time() - self.lastJumpFrame > JUMP_FRAMES_TIME:
                    self.jumpFrame = (self.jumpFrame + 1) % JUMP_FRAMES
                    self.lastJumpFrame = time.time()

        if right:
            self.direction = "right"
            self.movx = +speed
            if self.contact:
                self.frame = (self.frame + 1) % RUN_FRAMES
                self.image = pygame.image.load(self.run_right[self.frame]).convert()
                self.image.set_colorkey((255,255,255))
            else:
                self.image = pygame.image.load(self.jump_right[self.jumpFrame]).convert()
                self.image.set_colorkey((255,255,255))
                if time.time() - self.lastJumpFrame > JUMP_FRAMES_TIME:
                    self.jumpFrame = (self.jumpFrame + 1) % JUMP_FRAMES
                    self.lastJumpFrame = time.time()

        if shooting and time.time() - self.lastShotTime > shootTime:
            if not shootUp:
                if self.direction == "right":
                    projectile = Rect(self.rect.right,self.rect.top,self.rect.w,self.rect.h // 10)
                else:
                    projectile = Rect(self.rect.left - self.rect.w // 2,self.rect.top,self.rect.w,self.rect.h // 10)
                info = {'projectile':projectile,'direction':self.direction}
            else:
                projectile = Rect(self.rect.left,self.rect.top,self.rect.h // 10,self.rect.w)
                info = {'projectile':projectile,'direction':"top"}
            self.projectiles.append(info)
            self.lastShotTime = time.time()

        #Update player position
        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, world)

        if not self.contact and not self.jump and not self.canFly:
            self.movy += 1
            self.fallSpeed += 1
            if self.fallSpeed > MIN_VERTICAL_SPEED:
                self.fallSpeed = MIN_VERTICAL_SPEED
            self.rect.top += self.fallSpeed

        if self.jump:
            self.movy -= 1
            self.rect.top -= self.jumpSpeed
            self.maxJumpHeight -= self.jumpSpeed
            self.jumpSpeed -= 1
            if self.jumpSpeed <= MIN_VERTICAL_SPEED:
                self.jumpSpeed = MIN_VERTICAL_SPEED
            if self.maxJumpHeight <= 0:
                self.maxJumpHeight = self.rect.height * 2
                self.jump = False

        if self.isFlying:
            self.movy -= 1
            self.rect.top -= speed

        if self.flyDown:
            self.movy += 1
            self.rect.top += speed

        self.collide(0, self.movy, world)
        self.movx = 0
        self.movy = 0

        #Update projectiles
        for p in self.projectiles:
            if p.get('direction') == "right":
                p.get('projectile').left += 2 * HORIZ_MOV_INCR
            elif p.get('direction') == "left":
                p.get('projectile').left -= 2 * HORIZ_MOV_INCR
            elif p.get('direction') == "top":
                p.get('projectile').top -= 2 * HORIZ_MOV_INCR


        #now check for projectile collisions
        self.collideProjectiles(self.projectiles,world)

    def collide(self, movx, movy, world):
        self.contact = False
        for o in world:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contact = True
                    self.fallSpeed = 0
                    self.jumpSpeed = VERTICAL_MOV_INCR
                    self.jump = False
                    self.maxJumpHeight = self.rect.height * 2
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                    self.jumpSpeed = VERTICAL_MOV_INCR
                    self.jump = False
                    self.maxJumpHeight = self.rect.height * 2

    #Checks for collided projectiles
    def collideProjectiles(self,projectiles,world):
        for o in world:
            for p in projectiles[:]:
                if p.get('projectile').colliderect(o):
                    projectiles.remove(p)

    #checks for collisions with enemies
    def collideEnemies(self,enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and time.time() - self.lastTimeDamaged > DAMAGE_DELAY:
                #TODO:Remove hardcoded reduction
                self.health -= 10
                self.lastTimeDamaged = time.time()
                if self.health < 0:
                    self.health = 0

    #initialize player position
    def initPosition(self,world):
        for o in world:
            if self.rect.colliderect(o):
                self.rect.bottom = o.rect.top
