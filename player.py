import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time

HORIZ_MOV_INCR = 10 #speed of movement
JUMP_SPEEDS = 10 #number of different speeds for jumping
MIN_VERTICAL_SPEED = HORIZ_MOV_INCR
SHOOTING_FREQUENCY = 0.5
DAMAGE_DELAY = 2

class Player(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lastShotTime = 0
        self.symbol = "P"
        self.projectileImage = pygame.image.load("world/obstacle.png").convert()
        self.projectiles = []
        self.canFly = False
        self.isFlying = False
        self.health = 50
        self.energy = 75
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.fallSpeed = 0
        self.jumpSpeed = HORIZ_MOV_INCR
        self.contact = False
        self.jump = False
        self.image = pygame.image.load('actions/idle_right.png').convert()
        self.rect = self.image.get_rect()
        self.maxJumpHeight = self.rect.height * 2
        self.lastTimeDamaged = time.time()
        self.run_left = ["actions/run_left000.png","actions/run_left001.png",
                         "actions/run_left002.png", "actions/run_left003.png",
                         "actions/run_left004.png", "actions/run_left005.png",
                         "actions/run_left006.png", "actions/run_left007.png"]
        self.run_right = ["actions/run_right000.png","actions/run_right001.png",
                         "actions/run_right002.png", "actions/run_right003.png",
                         "actions/run_right004.png", "actions/run_right005.png",
                         "actions/run_right006.png", "actions/run_right007.png"]

        self.direction = "right"
        self.rect.topleft = [x, y]
        self.frame = 0

    def update(self, up, down, left, right, shooting, world, speed = HORIZ_MOV_INCR):
        #Check for key presses
        self.isFlying = False
        if up:
            if self.canFly:
                self.isFlying = True
            if self.contact:
                if self.direction == "right":
                    self.image = pygame.image.load("actions/jump_right.png")
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

        if not down and self.direction == "right":
                self.image = pygame.image.load('actions/idle_right.png').convert_alpha()

        if not down and self.direction == "left":
            self.image = pygame.image.load('actions/idle_left.png').convert_alpha()

        if left:
            self.direction = "left"
            self.movx = -speed
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_left[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = pygame.image.load("actions/jump_left.png").convert_alpha()

        if right:
            self.direction = "right"
            self.movx = +speed
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_right[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = pygame.image.load("actions/jump_right.png").convert_alpha()

        if shooting and time.time() - self.lastShotTime > SHOOTING_FREQUENCY:
            if self.direction == "right":
                projectile = Rect(self.rect.right,self.rect.top,self.rect.w,self.rect.h // 10)
            else:
                projectile = Rect(self.rect.left - self.rect.w // 2,self.rect.top,self.rect.w,self.rect.h // 10)
            info = {'projectile':projectile,'direction':self.direction}
            self.projectiles.append(info)
            self.lastShotTime = time.time()

        #Update player position
        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, world)

        if not self.contact and not self.jump and not self.isFlying:
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

        self.collide(0, self.movy, world)
        self.movx = 0
        self.movy = 0

        #Update projectiles
        for p in self.projectiles:
            if p.get('direction') == "right":
                p.get('projectile').left += 2 * HORIZ_MOV_INCR
            else:
                p.get('projectile').left -= 2 * HORIZ_MOV_INCR

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
                    self.jumpSpeed = HORIZ_MOV_INCR
                    self.jump = False
                    self.maxJumpHeight = self.rect.height * 2
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                    self.jumpSpeed = HORIZ_MOV_INCR
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
