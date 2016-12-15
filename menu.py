import pygame
from pygame.locals import *
import sys
import sqlite3
from databaseUtils import *

FPS = 30
DATABASE = 'random.db'
MAX_HEALTH = 100
MAX_ENERGY = 100

def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps

#Function to display screen for proceeding to next level
def showNextLevelScreen(screen):
    screenRect = screen.get_rect()
    font = pygame.font.Font(None,screenRect.h // 10)

    #text to display
    gzText = font.render("CONGRATULATIONS",1,(255,255,255))
    nextLevelText = font.render("YOU PROCEED TO THE NEXT LEVEL",1,(255,255,255))
    anyKeyText = font.render("PRESS ANY KEY TO CONTINUE",1,(255,255,255))

    #Rectangles of text
    gzPos = gzText.get_rect()
    nextLevelPos = nextLevelText.get_rect()
    anyKeyPos = anyKeyText.get_rect()

    gzPos.centerx = nextLevelPos.centerx = anyKeyPos.centerx = screenRect.centerx

    gzPos.bottom = screenRect.h // 3
    nextLevelPos.top = gzPos.bottom + 10
    anyKeyPos.bottom = 2 * (screenRect.h // 3 )
    leaveLoop = False

    while not leaveLoop:
        #Check for any key press
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                leaveLoop = True

        screen.fill((0,0,0))
        screen.blit(gzText,gzPos)
        screen.blit(nextLevelText,nextLevelPos)
        screen.blit(anyKeyText,anyKeyPos)
        pygame.display.flip()

#Function to display on screen message when player is dead
def showPlayerDeadScreen(screen):
    screenRect = screen.get_rect()
    font = pygame.font.Font(None,screenRect.h // 5)

    #Text to display
    deadText = font.render("YOU DIED",1,(255,255,255))
    deadTextPos = deadText.get_rect()
    deadTextPos.center = screenRect.center

    screen.blit(deadText,deadTextPos)

#Function to show player info while playing
#Temporarily shows hard coded values
def showPlayerInfo(screen,player):
    screenRect = screen.get_rect()
    font = pygame.font.Font(None,screenRect.h // 20)
    infoRect = Rect(0,0,screenRect.w,screenRect.h // 20)

    #fill background of bar with black color
    pygame.draw.rect(screen,(0,0,0),infoRect)

    #Generate text
    healthText = font.render("HEALTH : ",1,(255,255,255))
    energyText = font.render("ENERGY : ",1,(255,255,255))
    coinsText = font.render("COINS : " + str(player.coins),1,(255,255,255))

    #get rectangles of text
    healthPos = healthText.get_rect()
    energyPos = energyText.get_rect()
    coinsPos = coinsText.get_rect()

    #generate healthbar and energybar and place them after texts
    healthPos.left = 0
    healthPos.top = 0
    healthBar = Rect(healthPos.right + 10,0,screenRect.w // 4,healthPos.h)
    currentHealthWidth = int((healthBar.w - 2)* (player.health / MAX_HEALTH))
    remainingHealth = Rect(healthBar.left+1,healthBar.top+1,currentHealthWidth,healthBar.h - 2)
    energyPos.top = 0
    energyPos.left = healthBar.right + 10
    energyBar = Rect(energyPos.right + 10,0,screenRect.w // 4,energyPos.h)
    currentEnergyWidth = int((energyBar.w - 2 ) * (player.energy / MAX_ENERGY))
    remainingEnergy = Rect(energyBar.left+1,energyBar.top+1,currentEnergyWidth,energyBar.h - 2)
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

    if player.hasKey != None:
        keyRect = Rect(coinsPos.right + 10,0,50,screenRect.h // 20)
        screen.blit(player.hasKey.image,keyRect)


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

                    #Change volume based on progress
                    pygame.mixer.music.set_volume(volumeProgress.width / volumeBar.width )

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
                return False,-1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for r in slots:
                    if r.collidepoint(pygame.mouse.get_pos()):
                        return True,slots.index(r)
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
    moveLeftText = font.render("Move left",1,(255,255,255))
    moveRightText = font.render("Move right",1,(255,255,255))
    moveUpText = font.render("Move up (Flying)",1,(255,255,255))
    moveDownText = font.render("Move down (Flying)",1,(255,255,255))
    jumpText = font.render("Jump",1,(255,255,255))
    shootText = font.render("Shoot",1,(255,255,255))
    comboText = font.render("Shoot (Combo)",1,(255,255,255))

    #Render texts from database
    controls = getControls(0)
    controlsTextList = []
    controlsPosList = []

    #Create list of fonts
    for c in controls:
        controlsTextList.append(font.render(c,1,(255,255,255)))

    #Create rectangles of fonts
    for c in controlsTextList:
        controlsPosList.append(c.get_rect())

    #get rectangles of texts
    volumePos = volumeText.get_rect()
    controlsPos = controlsText.get_rect()
    moveLeftPos = moveLeftText.get_rect()
    moveRightPos = moveRightText.get_rect()
    moveUpPos = moveUpText.get_rect()
    moveDownPos = moveDownText.get_rect()
    jumpPos = jumpText.get_rect()
    shootPos = shootText.get_rect()
    comboPos = comboText.get_rect()

    #position them
    controlsPos.centerx = screenRect.centerx
    controlsPos.top = screenRect.top
    moveLeftPos.left = moveRightPos.left = moveUpPos.left = moveDownPos.left =  200
    jumpPos.left = shootPos.left = comboPos.left = 200
    moveLeftPos.top = controlsPos.bottom + 70
    moveRightPos.top = moveLeftPos.bottom + 20
    moveUpPos.top = moveRightPos.bottom + 20
    moveDownPos.top = moveUpPos.bottom + 20
    jumpPos.top = moveDownPos.bottom + 20
    shootPos.top = jumpPos.bottom + 20
    comboPos.top = shootPos.bottom + 20

    #Add them to list
    moveExplainList = [moveLeftPos,moveRightPos,moveUpPos,moveDownPos,jumpPos,shootPos,comboPos]

    #Position rectangles of texts from database
    for i in range(0,7):
        controlsPosList[i].top = moveExplainList[i].top
        controlsPosList[i].right = screenRect.w -200

    #create volume bar and progress
    volumeBar = Rect(0,0,screenRect.width // 2, screenRect.height // 12)
    volumeBar.centerx = screenRect.centerx
    volumeBar.bottom = screenRect.bottom - 10

    #adjust volume text position
    volumePos.right = volumeBar.left - 10
    volumePos.bottom = volumeBar.bottom

    volumeProgress = Rect(0,0,volumeBar.width // 2,volumeBar.height)
    volumeProgress.topleft = volumeBar.topleft

    #now create a rectangle for the button on the progress bar
    volumeButton = Rect(0,0,volumeBar.width // 20, int(volumeBar.height * 1.2))
    volumeButton.centerx = volumeProgress.right
    volumeButton.centery = volumeProgress.centery
    leaveLoop = False

    #Create a rectangle for active control
    activeControlRect = Rect(0,0,controlsPosList[0].w,controlsPosList[0].h)
    activeControlRect.center = controlsPosList[0].center

    while not leaveLoop:
        for event in pygame.event.get():
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE:
                    leaveLoop = True
                else:
                    name = pygame.key.name(event.key)
                    #Change controls
                    for i in range(0,7):
                        if controlsPosList[i].top == activeControlRect.top:
                            controls.pop(i)
                            print(len(controls))
                            controls.insert(i,name)
                            print(len(controls))
                            controlsTextList[i] = font.render(name,1,(255,255,255))
                            oldRect = controlsPosList[i]
                            controlsPosList[i] = controlsTextList[i].get_rect()
                            controlsPosList[i].center = oldRect.center
                            controlsPosList[i].right = screenRect.w - 200
                            activeControlRect = Rect(0,0,controlsPosList[i].w,controlsPosList[i].h)
                            activeControlRect.center = controlsPosList[i].center
                            changeControls(0,controls)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if volumeBar.collidepoint(pygame.mouse.get_pos()):
                    volumeProgress.width = pygame.mouse.get_pos()[0] - volumeBar.left
                    volumeProgress.topleft = volumeBar.topleft
                    volumeButton.centerx = volumeProgress.right

                    #Change volume based on progress
                    pygame.mixer.music.set_volume(volumeProgress.width / volumeBar.width )

                #Now check if user wants to change a control
                for r in controlsPosList:
                    if r.collidepoint(pygame.mouse.get_pos()):
                        activeControlRect = Rect(0,0,r.w,r.h)
                        activeControlRect.center = r.center

        screen.fill((0,0,0))
        screen.blit(volumeText,volumePos)
        screen.blit(controlsText,controlsPos)
        screen.blit(moveLeftText,moveLeftPos)
        screen.blit(moveRightText,moveRightPos)
        screen.blit(moveUpText,moveUpPos)
        screen.blit(moveDownText,moveDownPos)
        screen.blit(jumpText,jumpPos)
        screen.blit(shootText,shootPos)
        screen.blit(comboText,comboPos)

        #Rect around active move
        pygame.draw.rect(screen,(0,255,0),activeControlRect,2)

        #Moves
        for i in range(0,7):
            screen.blit(controlsTextList[i],controlsPosList[i])

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
                        return False,None
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

    #Playback music
    pygame.mixer.init()
    pygame.mixer.music.load("soundtracks/menu.ogg")
    pygame.mixer.music.play(-1,0)
    pygame.mixer.music.set_volume(0.5)

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
            startGame,playerId = showLoadingScreen(screen,font)
            if startGame:
                leaveLoop = True
            else:
                isStartMenuVisible = True
                areOptionsVisible = False
                isLoadingVisible = False
                isNewGameVisible = False

        pygame.display.flip()
        time_spent = tps(clock, FPS)
    pygame.mixer.music.stop()
    return playerId
