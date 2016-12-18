import pygame
from pygame.locals import *
import sys
from level import *
from player import *
from camera import *
from menu import *
from databaseUtils import *

SCREEN_SIZE = (0,0) #resolution of the game
FPS = 30
TIME_DEAD = 3

"""SETUP DATABASE"""
setupDatabase()

"""HERE THE MAIN PROGRAM STARTS"""

pygame.init()

#Show menu for login
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
screenInfo = pygame.display.Info()
clock = pygame.time.Clock()

nextLevel = False

"""GAME LOOP"""
while True:
    if not nextLevel:
        playerId = showMenu(screen,clock)
    else:
        nextLevel = False
        showNextLevelScreen(screen)
    pygame.mouse.set_visible(0)
    screen_rect = screen.get_rect()
    background = pygame.image.load("world/background2.jpg").convert_alpha()
    background_rect = background.get_rect()

    #Get level of player
    playerLevel = getLevel(playerId)
    playerCoins = getCoins(playerId)

    level = Level("level/level" + str(playerLevel) +  ".txt")
    level.create_level(0,0,playerId,playerLevel)
    world = level.world
    player = level.player
    player.coins = playerCoins
    enemies = level.enemies
    enemies2 = level.enemies2
    enemies3 = level.enemies3
    platformsVertical = level.platformsVertical
    platformsHorizontal = level.platformsHorizontal
    breakBlocks = level.breakBlocks
    stars = level.stars
    coins = level.coins
    hearts = level.hearts
    spawnPoints = level.spawnPoints
    jumpBoosts = level.jumpBoosts
    wings = level.wings
    fountains = level.fountains
    keys = level.keys
    door = level.door

    camera = Camera(screenInfo, player.rect, level.get_size()[0], level.get_size()[1])
    all_sprite = level.all_sprite
    up = down = left = right = shooting = shootUp = combo = False
    x, y = 0, 0
    leaveLoop = False

    #Sound
    keySound = pygame.mixer.Sound('Sounds/Key_Pickup.ogg')
    damageSound = pygame.mixer.Sound('Sounds/Punch.ogg')

    #Start song
    pygame.mixer.init()
    pygame.mixer.music.load("soundtracks/song" + str(playerLevel) + ".ogg")
    pygame.mixer.music.play(-1,0)
    pygame.mixer.music.set_volume(0.5)

    #Correct positions of player and enemies
    player.initPosition(world)
    for e in enemies:
        e.initPosition(world)
    for e in enemies2:
        e.initPosition(world)
    for e in enemies3:
        e.initPosition(world)

    #Get player moves
    controls = getControls(0)

    while not leaveLoop:

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                leaveLoop = showPauseScreen(screen,playerId)
                pygame.mouse.set_visible(0)

            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[2]:
                up = True
            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[3]:
                down = True
            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[0]:
                left = True
            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[1]:
                right = True
            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[5]:
                shooting = True
            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[4]:
                shootUp = True
            if event.type == KEYDOWN and pygame.key.name(event.key) == controls[6]:
                combo = True

            if event.type == KEYUP and pygame.key.name(event.key) == controls[2]:
                up = False
            if event.type == KEYUP and pygame.key.name(event.key) == controls[3]:
                down = False
            if event.type == KEYUP and pygame.key.name(event.key) == controls[0]:
                left = False
            if event.type == KEYUP and pygame.key.name(event.key) == controls[1]:
                right = False
            if event.type == KEYUP and pygame.key.name(event.key) == controls[5]:
                shooting = False
            if event.type == KEYUP and pygame.key.name(event.key) == controls[4]:
                shootUp = False
            if event.type == KEYUP and pygame.key.name(event.key) == controls[6]:
                combo = False

        asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)

        for x in range(0, asize[0], background_rect.w):
            for y in range(0, asize[1], background_rect.h):
                screen.blit(background, (x, y))

        visibleObjects,visibleSprites = camera.getVisibleObjects(world,level.all_sprite)
        time_spent = tps(clock, FPS)
        camera.draw_sprites(screen, visibleSprites)

        if player.isDead:
            if player in level.all_sprite:
                level.all_sprite.remove(player)
            showPlayerDeadScreen(screen)

        showPlayerInfo(screen,player)

        if not player.isDead:
            #Update player
            player.update(up, down, left, right, shooting, shootUp, combo ,visibleObjects)

            #Update player projectiles collisions
            player.collideProjectiles(player.projectiles,world,level.all_sprite,breakBlocks)

            #Check for enemy collisions with player
            player.collideEnemies(enemies,visibleObjects)
            player.collideEnemies(enemies2,visibleObjects)
            player.collideEnemies(enemies3,visibleObjects)
        else:
            if time.time() - player.isDeadStartTime > TIME_DEAD:
                player.isDead = False
                player.rect.x = player.startX
                player.rect.y = player.startY
                player.x = player.startX
                player.y = player.startY
                player.initPosition(visibleObjects)
                level.all_sprite.add(player)

        #Update enemies
        for enemy in enemies:
            if enemy in visibleSprites:
                enemy.update(player,visibleObjects)
                enemy.collideProjectiles(enemy.projectiles,visibleObjects,all_sprite,breakBlocks)

        for enemy in enemies2:
            if enemy in visibleSprites:
                enemy.update(player,visibleObjects)
                enemy.collideProjectiles(enemy.projectiles,visibleObjects,all_sprite,breakBlocks)

        for enemy in enemies3:
            if enemy in visibleSprites:
                enemy.update(player,visibleObjects)
                enemy.collideProjectiles(enemy.projectiles,visibleObjects,all_sprite,breakBlocks)

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
                    e.health -= p.get('damage')
                    player.projectiles.remove(p)
                    if e.health <= 0:
                        enemies.remove(e)
                        level.all_sprite.remove(e)
                    break

        #Do same for enemies 2
        for p in player.projectiles[:]:
            for e in enemies2[:]:
                if p.get('projectile').colliderect(e):
                    e.health -= p.get('damage')
                    player.projectiles.remove(p)
                    if e.health <= 0:
                        enemies2.remove(e)
                        level.all_sprite.remove(e)
                    break

        #Same for enemies 3
        for p in player.projectiles[:]:
            for e in enemies3[:]:
                if p.get('projectile').colliderect(e):
                    e.health -= p.get('damage')
                    player.projectiles.remove(p)
                    if e.health <= 0:
                        enemies3.remove(e)
                        level.all_sprite.remove(e)
                    break

        #Check if enemy projectiles hit player
        for e in enemies2:
            for p in e.projectiles[:]:
                if p.get('projectile').colliderect(player.rect):
                    if not player.isInvincible and not player.isDead and time.time() - player.lastTimeDamaged >= player.damage_delay:
                        player.lastTimeDamaged = time.time()
                        player.health -= e.damage
                        """---DAMAGE SOUND---"""
                        damageSound.play()
                        if player.health <= 0:
                            player.health = 100
                            player.x = player.startX
                            player.y = player.startY
                            player.rect.left = player.startX
                            player.rect.right = player.startY
                            player.initPosition(visibleObjects)
                    e.projectiles.remove(p)

        #Do the same for enemies 3
        for e in enemies3:
            for p in e.projectiles[:]:
                if p.get('projectile').colliderect(player.rect):
                    if not player.isInvincible and not player.isDead and time.time() - player.lastTimeDamaged >= player.damage_delay:
                        player.lastTimeDamaged = time.time()
                        player.health -= e.damage
                        """---DAMAGE SOUND---"""
                        damageSound.play()
                        if player.health <= 0:
                            player.health = 100
                            player.x = player.startX
                            player.y = player.startY
                            player.rect.left = player.startX
                            player.rect.right = player.startY
                            player.initPosition(visibleObjects)
                    e.projectiles.remove(p)

        #Update spin of stars
        for s in stars[:]:
            s.update()
            if player.rect.colliderect(s):
                player.setInvincible()
                level.all_sprite.remove(s)
                stars.remove(s)

        #Check if player collided with coin
        for c in coins[:]:
            if player.rect.colliderect(c):
                player.addCoin()
                level.all_sprite.remove(c)
                coins.remove(c)

        #Check if player collide with heart:
        for h in hearts[:]:
            if player.rect.colliderect(h):
                if player.replenishHealth(h):
                    level.all_sprite.remove(h)
                    hearts.remove(h)

        #Check if player collided with spawnpoint
        for s in spawnPoints:
            if player.rect.colliderect(s.rect) and not player.isDead:
                player.startX = s.x
                player.startY = s.y

        #Check if player collided with wings
        for w in wings[:]:
            w.update()
            if player.rect.colliderect(w):
                """---GET WINGS SOUND---"""
                player.canFly = True
                player.hasWings = True
                wings.remove(w)
                level.all_sprite.remove(w)

        #Check if player collided with jump boost
        for j in jumpBoosts[:]:
            if player.rect.colliderect(j):
                """---GET JUMP BOOST SOUND---"""
                player.startJumpHeight += player.rect.height
                jumpBoosts.remove(j)
                level.all_sprite.remove(j)

        #Check if player collided with fountain
        for f in fountains:
            if player.rect.colliderect(f):
                player.energy += 10
                if player.hasWings:
                    player.canFly = True
                if player.energy >= 100:
                    player.energy = 100

        #Check if collided with keys
        for k in keys[:]:
            if player.rect.colliderect(k):
                """---GET KEY SOUND---"""
                keySound.play()
                keys.remove(k)
                player.hasKey = k
                level.all_sprite.remove(k)

        #Check for door
        if door != None and player.hasKey != None:
            if player.rect.colliderect(door):
                playerLevel += 1
                setStats(playerId,playerLevel,player.coins)
                leaveLoop = True
                nextLevel = True
                pygame.mixer.music.stop()

        camera.update()
        pygame.display.flip()
