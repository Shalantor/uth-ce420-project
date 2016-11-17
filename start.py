import pygame
from pygame.locals import *
import sys
from level import *
from player import *
from camera import *
from menu import *
from databaseUtils import *

SCREEN_SIZE = (1280, 720) #resolution of the game
FPS = 30

"""SETUP DATABASE"""
setupDatabase()

"""HERE THE MAIN PROGRAM STARTS"""

pygame.init()

#Show menu for login
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
clock = pygame.time.Clock()

"""GAME LOOP"""
while True:
    #playerId = showMenu(screen,clock)
    pygame.mouse.set_visible(0)
    screen_rect = screen.get_rect()
    background = pygame.image.load("world/background2.jpg").convert_alpha()
    background_rect = background.get_rect()
    level = Level("level/level2.txt")
    level.create_level(0,0)
    world = level.world
    player = level.player
    enemies = level.enemies
    enemies2 = level.enemies2
    platformsVertical = level.platformsVertical
    platformsHorizontal = level.platformsHorizontal

    camera = Camera(screen, player.rect, level.get_size()[0], level.get_size()[1])
    all_sprite = level.all_sprite
    up = down = left = right = shooting = shootUp = False
    x, y = 0, 0
    leaveLoop = False

    #Correct positions of player and enemies
    player.initPosition(world)
    for e in enemies:
        e.initPosition(world)
    for e in enemies2:
        e.initPosition(world)

    while not leaveLoop:

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                leaveLoop = showPauseScreen(screen,playerId)
                pygame.mouse.set_visible(0)

            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_DOWN:
                down = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYDOWN and event.key == K_SPACE:
                shooting = True
            if event.type == KEYDOWN and event.key == K_w:
                shootUp = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_DOWN:
                down = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_SPACE:
                shooting = False
            if event.type == KEYUP and event.key == K_w:
                shootUp = False

        asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)

        for x in range(0, asize[0], background_rect.w):
            for y in range(0, asize[1], background_rect.h):
                screen.blit(background, (x, y))

        time_spent = tps(clock, FPS)
        camera.draw_sprites(screen, all_sprite)
        showPlayerInfo(screen,player)

        #Update player
        player.update(up, down, left, right, shooting, shootUp, world)

        #Check for enemy collisions with player
        player.collideEnemies(enemies)

        #Update enemies
        for enemy in enemies:
            enemy.update(player,world)

        for enemy in enemies2:
            enemy.update(player,world)

        #Update vertical platforms
        for platV in platformsVertical:
            platV.move(player)

        #Update horizontal platforms
        for platH in platformsHorizontal:
            platH.move(player)

        #Check if player projectiles hit enemies 1
        for p in player.projectiles[:]:
            for e in enemies[:]:
                if p.get('projectile').colliderect(e):
                    e.health -= player.damage
                    player.projectiles.remove(p)
                    if e.health <= 0:
                        enemies.remove(e)
                        level.all_sprite.remove(e)
                    break

        #Do same for enemies 2
        for p in player.projectiles[:]:
            for e in enemies2[:]:
                if p.get('projectile').colliderect(e):
                    e.health -= player.damage
                    player.projectiles.remove(p)
                    if e.health <= 0:
                        enemies2.remove(e)
                        level.all_sprite.remove(e)
                    break


        #Check if enemy projectiles hit player
        for e in enemies2:
            for p in e.projectiles[:]:
                if p.get('projectile').colliderect(player.rect):
                    player.health -= e.damage
                    e.projectiles.remove(p)

        camera.update()
        pygame.display.flip()
