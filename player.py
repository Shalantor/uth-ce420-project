import pygame
from pygame.locals import *
import sys
from level import *
from camera import *

HORIZ_MOV_INCR = 10 #speed of movement
JUMP_SPEEDS = 10 #number of different speeds for jumping

class Player(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
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
        if up:
            if self.contact:
                if self.direction == "right":
                    self.image = pygame.image.load("actions/jump_right.png")
                self.jump = True
                self.movy -= 1
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

        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, world)


        if not self.contact:
            self.movy += 1
            self.fallSpeed += HORIZ_MOV_INCR / JUMP_SPEEDS
            if self.fallSpeed > HORIZ_MOV_INCR:
                self.fallSpeed = HORIZ_MOV_INCR
            self.rect.top += self.fallSpeed

        if self.jump:
            self.movy -= 1
            self.rect.top -= self.jumpSpeed
            self.jumpSpeed -= HORIZ_MOV_INCR / JUMP_SPEEDS
            if self.jumpSpeed <= 0 or self.contact:
                self.jump = False

        self.contact = False
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
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                    self.jumpSpeed = HORIZ_MOV_INCR
