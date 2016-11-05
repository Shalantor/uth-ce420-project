import pygame
from pygame.locals import *
import sys
import sqlite3
from databaseUtils import *

FPS = 30
DATABASE = 'random.db'

def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps

#Function to show player info while playing
#Temporarily shows hard coded values
def showPlayerInfo(screen):
    screenRect = screen.get_rect()
    font = pygame.font.Font(None,screenRect.h // 20)
    infoRect = Rect(0,0,screenRect.w,screenRect.h // 20)

    #fill background of bar with black color
    pygame.draw.rect(screen,(0,0,0),infoRect)

    #Generate text
    healthText = font.render("HEALTH : ",1,(255,255,255))
    energyText = font.render("ENERGY : ",1,(255,255,255))
    coinsText = font.render("COINS : ",1,(255,255,255))

    #get rectangles of text
    healthPos = healthText.get_rect()
    energyPos = energyText.get_rect()
    coinsPos = coinsText.get_rect()

    #generate healthbar and energybar and place them after texts
    healthPos.left = 0
    healthPos.top = 0
    healthBar = Rect(healthPos.right + 10,0,screenRect.w // 4,healthPos.h)
    remainingHealth = Rect(healthBar.left+1,healthBar.top+1,healthBar.w - 2,healthBar.h - 2)
    energyPos.top = 0
    energyPos.left = healthBar.right + 10
    energyBar = Rect(energyPos.right + 10,0,screenRect.w // 4,energyPos.h)
    remainingEnergy = Rect(energyBar.left+1,energyBar.top+1,energyBar.w - 2,energyBar.h - 2)
    coinsPos.top = 0
    coinsPos.left = energyBar.right + 10

    #Now draw on screen
    screen.blit(healthText,healthPos)
    screen.blit(energyText,energyPos)
    screen.blit(coinsText,coinsPos)
    pygame.draw.rect(screen,(255,255,255),healthBar,1)
    pygame.draw.rect(screen,(255,0,0),remainingHealth)
    pygame.draw.rect(screen,(255,255,255),energyBar,1)
    pygame.draw.rect(screen,(0,0,255),remainingEnergy)


#Function to show pause screen from game
#Returns true for leaving game and false for just continuing
def showPauseScreen(screen,playerId):
    width,height = screen.get_size()
    font = pygame.font.Font(None,height // 10)
    screenRect = screen.get_rect()
    pygame.mouse.set_visible(1)
    activeDifficulty = getDifficulty(playerId)

    #render texts
    difficultyText = font.render("DIFFICULTY",1,(255,255,255))
    easyText = font.render("EASY",1,(255,255,255))
    mediumText = font.render("MEDIUM",1,(255,255,255))
    hardText = font.render("HARD",1,(255,255,255))
    volumeText = font.render("VOLUME",1,(255,255,255))
    exitText = font.render("EXIT",1,(255,255,255))

    #get rectangles
    difficultyPos = difficultyText.get_rect()
    easyPos = easyText.get_rect()
    mediumPos = mediumText.get_rect()
    hardPos = hardText.get_rect()
    volumePos = volumeText.get_rect()
    exitPos = exitText.get_rect()

    #position them
    difficultyPos.centerx = screenRect.centerx
    difficultyPos.top = 5
    easyPos.centerx = screenRect.centerx - (screenRect.width // 3)
    mediumPos.centerx = screenRect.centerx
    hardPos.centerx = screenRect.centerx + (screenRect.width // 3)
    easyPos.top = difficultyPos.bottom + 50
    mediumPos.top = difficultyPos.bottom + 50
    hardPos.top = difficultyPos.bottom + 50
    exitPos.centerx = screenRect.centerx
    exitPos.bottom = screenRect.bottom - 100
    diffList = [easyPos,mediumPos,hardPos]

    #Volume bar setup
    volumeBar = Rect(0,0,screenRect.width // 2, screenRect.height // 12)
    volumeBar.centerx = screenRect.centerx
    volumeBar.centery = screenRect.centery

    #adjust volume text position
    volumePos.right = volumeBar.left - 10
    volumePos.bottom = volumeBar.bottom

    #TODO:set progress according to current volume
    volumeProgress = Rect(0,0,volumeBar.width // 2,volumeBar.height)
    volumeProgress.topleft = volumeBar.topleft

    #now create a rectangle for the button on the progress bar
    volumeButton = Rect(0,0,volumeBar.width // 20, int(volumeBar.height * 1.2))
    volumeButton.centerx = volumeProgress.right
    volumeButton.centery = volumeProgress.centery

    #draw on screen
    screen.fill((0,0,0))
    screen.blit(difficultyText,difficultyPos)
    screen.blit(easyText,easyPos)
    screen.blit(mediumText,mediumPos)
    screen.blit(hardText,hardPos)
    screen.blit(volumeText,volumePos)
    screen.blit(exitText,exitPos)
    pygame.draw.rect(screen,(255,255,255),volumeBar,1)
    pygame.draw.rect(screen,(0,255,0),volumeProgress)
    pygame.draw.rect(screen,(0,0,255),volumeButton)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if volumeBar.collidepoint(pygame.mouse.get_pos()):
                    volumeProgress.width = pygame.mouse.get_pos()[0] - volumeBar.left
                    volumeProgress.topleft = volumeBar.topleft
                    volumeButton.centerx = volumeProgress.right
                if exitPos.collidepoint(pygame.mouse.get_pos()):
                    return True
                for rect in diffList:
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        activeDifficulty = diffList.index(rect)
                        changeDifficulty(playerId,activeDifficulty)

        #draw on screen
        screen.fill((0,0,0))
        screen.blit(difficultyText,difficultyPos)
        pygame.draw.rect(screen,(0,255,0),diffList[activeDifficulty])
        screen.blit(easyText,easyPos)
        screen.blit(mediumText,mediumPos)
        screen.blit(hardText,hardPos)
        screen.blit(volumeText,volumePos)
        screen.blit(exitText,exitPos)
        pygame.draw.rect(screen,(255,255,255),volumeBar,1)
        pygame.draw.rect(screen,(0,255,0),volumeProgress)
        pygame.draw.rect(screen,(0,0,255),volumeButton)
        pygame.display.flip()


def showLoadingScreen(screen,font):

    screenRect = screen.get_rect()
    chooseText = font.render("CHOOSE A SAVE",1,(255,255,255))
    choosePos = chooseText.get_rect()
    choosePos.centerx = screenRect.centerx
    choosePos.top = 5

    #get user data
    profiles = getProfiles()
    profileTexts = []
    for p in profiles:
        profileTexts.append(font.render(p,1,(255,255,255)))

    profilePos = Rect(0,0,choosePos.width // 2,choosePos.height)

    #rectangles for slots
    slotRect1 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slotRect2 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slotRect3 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slotRect4 = Rect(0,0,screenRect.width // 5, screenRect.height // 5)
    slots = [slotRect1,slotRect2,slotRect3,slotRect4]

    #positioning them on screen
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
    screen.blit(chooseText,choosePos)
    for r in slots:
        pygame.draw.rect(screen,(255,255,255),r,1)
    pygame.display.flip()
    leaveLoop = False

    while not leaveLoop:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                leaveLoop = True
            screen.fill((0,0,0))
            screen.blit(chooseText,choosePos)
            for i in range(0,4):
                pygame.draw.rect(screen,(255,255,255),slots[i],1)
                profilePos.center = slots[i].center
                screen.blit(profileTexts[i],profilePos)
            pygame.display.flip()


def showOptions(screen,font):

    screenRect = screen.get_rect()

    #render texts
    volumeText = font.render("VOLUME",1,(255,255,255))
    controlsText = font.render("CONTROLS",1,(255,255,255))

    #get rectangles of texts
    volumePos = volumeText.get_rect()
    controlsPos = controlsText.get_rect()

    #position them
    controlsPos.centerx = screenRect.centerx
    controlsPos.top = screenRect.top

    #create volume bar and progress
    volumeBar = Rect(0,0,screenRect.width // 2, screenRect.height // 12)
    volumeBar.centerx = screenRect.centerx
    volumeBar.bottom = screenRect.bottom - 10

    #adjust volume text position
    volumePos.right = volumeBar.left - 10
    volumePos.bottom = volumeBar.bottom

    #TODO:set progress according to current volume
    volumeProgress = Rect(0,0,volumeBar.width // 2,volumeBar.height)
    volumeProgress.topleft = volumeBar.topleft

    #now create a rectangle for the button on the progress bar
    volumeButton = Rect(0,0,volumeBar.width // 20, int(volumeBar.height * 1.2))
    volumeButton.centerx = volumeProgress.right
    volumeButton.centery = volumeProgress.centery

    #draw on screen
    screen.fill((0,0,0))
    screen.blit(volumeText,volumePos)
    screen.blit(controlsText,controlsPos)
    pygame.draw.rect(screen,(255,255,255),volumeBar,1)
    pygame.draw.rect(screen,(0,255,0),volumeProgress)
    pygame.draw.rect(screen,(0,0,255),volumeButton)
    pygame.display.flip()
    leaveLoop = False

    while not leaveLoop:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                leaveLoop = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if volumeBar.collidepoint(pygame.mouse.get_pos()):
                    volumeProgress.width = pygame.mouse.get_pos()[0] - volumeBar.left
                    volumeProgress.topleft = volumeBar.topleft
                    volumeButton.centerx = volumeProgress.right
        screen.fill((0,0,0))
        screen.blit(volumeText,volumePos)
        screen.blit(controlsText,controlsPos)
        pygame.draw.rect(screen,(255,255,255),volumeBar,1)
        pygame.draw.rect(screen,(0,255,0),volumeProgress)
        pygame.draw.rect(screen,(0,0,255),volumeButton)
        pygame.display.flip()



def showNameBox(screen,font):
    joinString = ""
    currentList = []

    #difficulties: 0 for easy, 1 for medium, 2 for hard, default is easy
    activeDifficulty = 0

    #get user data
    profiles = getProfiles()
    profileTexts = []
    for p in profiles:
        profileTexts.append(font.render(p,1,(255,255,255)))

    #render texts
    namePrompt = font.render("ENTER YOUR NAME",1,(255,255,255))
    okText = font.render("OK",1,(255,255,255))
    slotText = font.render("CHOOSE A SLOT",1,(255,255,255))
    difficultyText = font.render("CHOOSE DIFFICULTY",1,(255,255,255))
    easyText = font.render("EASY",1,(255,255,255))
    mediumText = font.render("MEDIUM",1,(255,255,255))
    hardText = font.render("HARD",1,(255,255,255))

    #get rectangles of texts
    namePos = namePrompt.get_rect()
    okPos = okText.get_rect()
    slotPos = slotText.get_rect()
    difficultyPos = difficultyText.get_rect()
    easyPos = easyText.get_rect()
    mediumPos = mediumText.get_rect()
    hardPos = hardText.get_rect()
    profilePos = Rect(0,0,slotPos.width // 2,slotPos.height)

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
    okPos.bottom = screenRect.bottom - 170
    inputRect.centerx = screenRect.centerx
    inputRect.bottom = okPos.top - 50
    namePos.bottom = inputRect.top - 50
    slotPos.centerx = screenRect.centerx
    slotPos.top = 5
    difficultyPos.centerx = screenRect.centerx
    difficultyPos.top = 5
    easyPos.centerx = screenRect.centerx - (screenRect.width // 3)
    mediumPos.centerx = screenRect.centerx
    hardPos.centerx = screenRect.centerx + (screenRect.width // 3)
    easyPos.top = difficultyPos.bottom + 50
    mediumPos.top = difficultyPos.bottom + 50
    hardPos.top = difficultyPos.bottom + 50

    #list for easier rendering of active difficulty
    diffList = [easyPos,mediumPos,hardPos]

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
    leaveFunctionLoop = False

    #the slot that is chosen
    chosenSlot = 0

    while not leaveFunctionLoop:
        leaveSlotsLoop = False
        leaveNamePromptLoop = False

        while not leaveSlotsLoop:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for r in slots:
                        if r.collidepoint(pygame.mouse.get_pos()):
                            chosenSlot = slots.index(r)
                            leaveSlotsLoop = True


            screen.fill((0,0,0))
            screen.blit(slotText,slotPos)
            for i in range(0,4):
                pygame.draw.rect(screen,(255,255,255),slots[i],1)
                profilePos.center = slots[i].center
                screen.blit(profileTexts[i],profilePos)
            pygame.display.flip()

        #draw on screen
        screen.fill((0,0,0))
        screen.blit(namePrompt,namePos)
        screen.blit(okText,okPos)
        pygame.draw.rect(screen,(255,255,255),inputRect,1)
        pygame.display.flip()

        while not leaveNamePromptLoop:
            inKey = -1
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if okPos.collidepoint(pygame.mouse.get_pos()) and len(currentList) >= 1:
                        enterProfile(chosenSlot,"".join(currentList),activeDifficulty)
                        return True,chosenSlot
                    for pos in diffList:
                        if pos.collidepoint(pygame.mouse.get_pos()):
                            activeDifficulty = diffList.index(pos)
                if event.type == KEYDOWN:
                    inKey = event.key

            if inKey > 0:
                if inKey == K_BACKSPACE:
                    currentList = currentList[0:-1]
                elif inKey == K_ESCAPE:
                    leaveNamePromptLoop = True
                elif inKey == K_MINUS and len(currentList) <= 7:
                    currentList.append("_")
                elif inKey <= 127 and len(currentList) <= 7:
                    currentList.append(chr(inKey))

            screen.fill((0,0,0))
            pygame.draw.rect(screen,(0,255,0),diffList[activeDifficulty])
            screen.blit(namePrompt,namePos)
            screen.blit(okText,okPos)
            screen.blit(difficultyText,difficultyPos)
            screen.blit(easyText,easyPos)
            screen.blit(mediumText,mediumPos)
            screen.blit(hardText,hardPos)
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
                elif isStartMenuVisible and optionsPos.collidepoint(pygame.mouse.get_pos()):
                    isStartMenuVisible = False
                    areOptionsVisible = True
                    isLoadingVisible = False
                    isNewGameVisible = False
                elif isStartMenuVisible and loadPos.collidepoint(pygame.mouse.get_pos()):
                    isStartMenuVisible = False
                    areOptionsVisible = False
                    isLoadingVisible = True
                    isNewGameVisible = False

        if isStartMenuVisible:
            screen.blit(startBackground,(0,0))
        elif isNewGameVisible:
            startGame,playerId = showNameBox(screen,font)
            if startGame:
                leaveLoop = True
            else:
                isStartMenuVisible = True
                areOptionsVisible = False
                isLoadingVisible = False
                isNewGameVisible = False
        elif areOptionsVisible:
            showOptions(screen,font)
            isStartMenuVisible = True
            areOptionsVisible = False
            isLoadingVisible = False
            isNewGameVisible = False
        elif isLoadingVisible:
            playerId = showLoadingScreen(screen,font)
            isStartMenuVisible = True
            areOptionsVisible = False
            isLoadingVisible = False
            isNewGameVisible = False

        pygame.display.flip()
        time_spent = tps(clock, FPS)
    return playerId
