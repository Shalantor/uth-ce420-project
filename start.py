import pygame
from pygame.locals import *
import sys
from level import *
from player import *
from camera import *

SCREEN_SIZE = (1280, 720) #resolution of the game
FPS = 30

def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
screen_rect = screen.get_rect()
background = pygame.image.load("world/background2.jpg").convert_alpha()
background_rect = background.get_rect()
level = Level("level/level.txt")
level.create_level(0,0)
world = level.world
player = level.player
pygame.mouse.set_visible(0)

camera = Camera(screen, player.rect, level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite

clock = pygame.time.Clock()

up = down = left = right = False
x, y = 0, 0
while True:

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_UP:
            up = True
        if event.type == KEYDOWN and event.key == K_DOWN:
            down = True
        if event.type == KEYDOWN and event.key == K_LEFT:
            left = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            right = True

        if event.type == KEYUP and event.key == K_UP:
            up = False
        if event.type == KEYUP and event.key == K_DOWN:
            down = False
        if event.type == KEYUP and event.key == K_LEFT:
            left = False
        if event.type == KEYUP and event.key == K_RIGHT:
            right = False

    asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)
    bg = pygame.Surface(asize)

    for x in range(0, asize[0], background_rect.w):
        for y in range(0, asize[1], background_rect.h):
            screen.blit(background, (x, y))

    time_spent = tps(clock, FPS)
    camera.draw_sprites(screen, all_sprite)

    player.update(up, down, left, right, world)
    camera.update()
    pygame.display.flip()
