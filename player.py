import pygame
from pygame.locals import *
import sys
from level import *
from camera import *

HORIZ_MOV_INCR = 10 #speed of movement
JUMP_SPEEDS = 10 #number of different speeds for jumping
MIN_VERTICAL_SPEED = HORIZ_MOV_INCR

class Player(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
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

    def update(self, up, down, left, right, world):
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
            self.movx = -HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_left[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = pygame.image.load("actions/jump_left.png").convert_alpha()

        if right:
            self.direction = "right"
            self.movx = +HORIZ_MOV_INCR
            if self.contact:
                self.frame += 1
                self.image = pygame.image.load(self.run_right[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.image = pygame.image.load("actions/jump_right.png").convert_alpha()

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
            self.rect.top -= HORIZ_MOV_INCR

        self.collide(0, self.movy, world)
        self.movx = 0
        self.movy = 0

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
