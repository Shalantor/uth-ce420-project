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

def showNameBox(screen,font):
    joinString = ""
    currentList = []

    #render texts
    namePrompt = font.render("ENTER YOUR NAME",1,(255,255,255))
    okText = font.render("OK",1,(255,255,255))
    slotText = font.render("CHOOSE A SLOT",1,(255,255,255))
    emptyText = font.render("EMPTY",1,(255,255,255))

    #get rectangles of texts
    namePos = namePrompt.get_rect()
    okPos = okText.get_rect()
    slotPos = slotText.get_rect()
    emptyPos = emptyText.get_rect()

    #rectangle for the typed text
    screenRect = screen.get_rect()
    inputRect = Rect(0,0,screenRect.width // 4,screenRect.height // 10)

    #rectangles for slots
    slotRect1 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slotRect2 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slotRect3 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slotRect4 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slots = [slotRect1,slotRect2,slotRect3,slotRect4]

    #position them
    namePos.centerx = screenRect.centerx
    okPos.centerx = screenRect.centerx
    namePos.top = 2 * namePos.height
    okPos.centery = screenRect.centery + 2 * okPos.height
    inputRect.centerx = screenRect.centerx
    inputRect.centery = screenRect.centery
    slotPos.centerx = screenRect.centerx
    slotPos.top = 5

    slotRect1.centerx = screenRect.width // 4
    slotRect2.centerx = screenRect.width // 4
    slotRect3.centerx = 3 * (screenRect.width // 4)
    slotRect4.centerx = 3 * (screenRect.width // 4)

    slotRect1.centery = screenRect.height // 4
    slotRect2.centery = 3 * (screenRect.height // 4)
    slotRect3.centery = screenRect.height // 4
    slotRect4.centery = 3 * (screenRect.height // 4)

    #now draw on screen
    screen.fill((0,0,0))
    screen.blit(slotText,slotPos)
    for r in slots:
        pygame.draw.rect(screen,(255,255,255),r,1)
    pygame.display.flip()
    leaveLoop = False

    while not leaveLoop:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for r in slots:
                    if r.collidepoint(pygame.mouse.get_pos()):
                        leaveLoop = True

        screen.fill((0,0,0))
        screen.blit(slotText,slotPos)
        for r in slots:
            pygame.draw.rect(screen,(255,255,255),r,1)
            emptyPos.centerx = r.centerx
            emptyPos.centery = r.centery
            screen.blit(emptyText,emptyPos)
        pygame.display.flip()

    #draw on screen
    screen.fill((0,0,0))
    screen.blit(namePrompt,namePos)
    screen.blit(okText,okPos)
    pygame.draw.rect(screen,(255,255,255),inputRect,1)
    pygame.display.flip()

    while True:
        inKey = -1
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if okPos.collidepoint(pygame.mouse.get_pos()):
                    return True
            if event.type == KEYDOWN:
                inKey = event.key

        if inKey > 0:
            if inKey == K_BACKSPACE:
                currentList = currentList[0:-1]
            elif inKey == K_ESCAPE:
                return False
            elif inKey == K_MINUS and len(currentList) <= 10:
                currentList.append("_")
            elif inKey <= 127 and len(currentList) <= 10:
                currentList.append(chr(inKey))

        screen.fill((0,0,0))
        screen.blit(namePrompt,namePos)
        screen.blit(okText,okPos)
        pygame.draw.rect(screen,(255,255,255),inputRect,1)

        if len(currentList) > 0:
            inputText = font.render(joinString.join(currentList),1,(255,255,255))
            inputTextPos = inputText.get_rect()
            inputTextPos.centerx = inputRect.centerx
            inputTextPos.centery = inputRect.centery
            screen.blit( inputText , inputTextPos)
        pygame.display.flip()

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

    #now first the screen with the available slots should be shown

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Check if exit has been clicked and if it was terminate program
                if isStartMenuVisible and exitPos.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                #check if new game is clicked and if it is navigate to next menu
                elif isStartMenuVisible and playPos.collidepoint(pygame.mouse.get_pos()):
                    isStartMenuVisible = False
                    areOptionsVisible = False
                    isLoadingVisible = False
                    isNewGameVisible = True

        if isStartMenuVisible:
            screen.blit(startBackground,(0,0))
        elif isNewGameVisible:
            startGame = showNameBox(screen,font)
            if startGame:
                leaveLoop = True
            else:
                isStartMenuVisible = True
                areOptionsVisible = False
                isLoadingVisible = False
                isNewGameVisible = False

        pygame.display.flip()
        time_spent = tps(clock, FPS)


"""HERE THE MAIN PROGRAM STARTS"""

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
