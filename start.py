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

def showMenu(screen,clock):
    pygame.mouse.set_visible(1)
    startBackground = pygame.Surface(screen.get_size()).convert()
    width,height = screen.get_size()
    font = pygame.font.Font(None,height // 10)

    #Variables to know what is visible and what isnt
    areOptionsVisible = False
    isLoadingVisible = False
    isStartMenuVisible = True
    isNewGameVisible = False

    #render texts
    playText = font.render("NEW GAME",1,(255,255,255))
    loadText = font.render("LOAD",1,(255,255,255))
    optionsText = font.render("OPTIONS",1,(255,255,255))
    exitText = font.render("EXIT",1,(255,255,255))

    #Get rectangles for text
    playPos = playText.get_rect()
    loadPos = loadText.get_rect()
    optionsPos = optionsText.get_rect()
    exitPos = exitText.get_rect()

    #Set position of texts
    playPos.centerx = startBackground.get_rect().centerx
    loadPos.centerx = startBackground.get_rect().centerx
    optionsPos.centerx = startBackground.get_rect().centerx
    exitPos.centerx = startBackground.get_rect().centerx

    playPos.centery = startBackground.get_rect().centery - 3 * playPos.height
    loadPos.centery = startBackground.get_rect().centery - 1 * loadPos.height
    optionsPos.centery = startBackground.get_rect().centery + 1 * optionsPos.height
    exitPos.centery = startBackground.get_rect().centery + 3 * exitPos.height

    #blit to background
    startBackground.blit(playText,playPos)
    startBackground.blit(loadText,loadPos)
    startBackground.blit(optionsText,optionsPos)
    startBackground.blit(exitText,exitPos)

    #blit to screen
    leaveLoop = False

    while not leaveLoop:
        for event in pygame.event.get():
            #Check for closing game or going back to previous menu
            if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                if isStartMenuVisible:
                    pygame.quit()
                    sys.exit()
                else:
                    isStartMenuVisible = True
                    areOptionsVisible = False
                    isLoadingVisible = False
                    isNewGameVisible = False

            #Check if new game has been clicked and then navigate to next menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if isStartMenuVisible and exitPos.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        if isStartMenuVisible:
            screen.blit(startBackground,(0,0))

        pygame.display.flip()
        time_spent = tps(clock, FPS)


pygame.init()

#Show menu for login
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
clock = pygame.time.Clock()

showMenu(screen,clock)

"""Now set variables for gameplay """
pygame.mouse.set_visible(0)
screen_rect = screen.get_rect()
background = pygame.image.load("world/background2.jpg").convert_alpha()
background_rect = background.get_rect()
level = Level("level/level.txt")
level.create_level(0,0)
world = level.world
player = level.player

camera = Camera(screen, player.rect, level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite
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

    for x in range(0, asize[0], background_rect.w):
        for y in range(0, asize[1], background_rect.h):
            screen.blit(background, (x, y))

    time_spent = tps(clock, FPS)
    camera.draw_sprites(screen, all_sprite)

    player.update(up, down, left, right, world)
    camera.update()
    pygame.display.flip()
