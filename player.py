import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time

HORIZ_MOV_INCR = 10 #speed of movement
VERTICAL_MOV_INCR = 20
MIN_VERTICAL_SPEED = 15
SHOOTING_FREQUENCY = 0.2
DAMAGE_DELAY = 2
DAMAGE = 10
STAND_FRAMES = 3
STAND_FRAMES_TIME = 0.2
RUN_FRAMES = 16
JUMP_FRAMES = 9
JUMP_FRAMES_TIME = 0.4
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
SHOOT_FRAMES = 8
WALK_SHOOT_FRAMES = 15
JUMP_SHOOT_FRAMES = 9

class Player(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lastShotTime = 0
        self.symbol = "P"
        self.projectileImage = pygame.image.load("megaman/fires/fr1.png").convert()
        self.projectileImage.set_colorkey((255,255,255))
        self.projectiles = []
        self.coins = 0
        self.canFly = False
        self.isFlying = False
        self.flyDown = False
        self.health = 100
        self.energy = 100
        self.damage = DAMAGE
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.fallSpeed = 0
        self.jumpSpeed = VERTICAL_MOV_INCR
        self.contact = False
        self.jump = False
        self.image = pygame.image.load("megaman/stand/sr1.png").convert()
        self.image = pygame.transform.scale(self.image,(50,80))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.maxJumpHeight = self.rect.height * 1.5
        self.lastTimeDamaged = time.time() - DAMAGE_DELAY
        self.isInvincible = False
        self.invincibilityTime = 20 #TODO:Change time
        self.startInvincibility = 0

        self.jump_left = ["megaman/jump_left/jl1.png","megaman/jump_left/jl2.png",
                         "megaman/jump_left/jl3.png","megaman/jump_left/jl4.png",
                         "megaman/jump_left/jl5.png","megaman/jump_left/jl6.png",
                         "megaman/jump_left/jl7.png","megaman/jump_left/jl8.png","megaman/jump_left/jl9.png"]

        self.jump_right = ["megaman/jump_right/jr1.png","megaman/jump_right/jr2.png",
                         "megaman/jump_right/jr3.png","megaman/jump_right/jr4.png",
                         "megaman/jump_right/jr5.png","megaman/jump_right/jr6.png",
                         "megaman/jump_right/jr7.png","megaman/jump_right/jr8.png","megaman/jump_right/jr9.png"]

        self.run_left = ["megaman/move_left/ml1.png","megaman/move_left/ml2.png",
                         "megaman/move_left/ml3.png", "megaman/move_left/ml4.png",
                         "megaman/move_left/ml5.png", "megaman/move_left/ml6.png",
                         "megaman/move_left/ml7.png", "megaman/move_left/ml8.png",
                         "megaman/move_left/ml9.png","megaman/move_left/ml10.png",
                         "megaman/move_left/ml11.png","megaman/move_left/ml12.png",
                         "megaman/move_left/ml13.png","megaman/move_left/ml14.png",
                         "megaman/move_left/ml15.png","megaman/move_left/ml16.png"]

        self.run_right = ["megaman/move_right/mr1.png","megaman/move_right/mr2.png",
                         "megaman/move_right/mr3.png", "megaman/move_right/mr4.png",
                         "megaman/move_right/mr5.png", "megaman/move_right/mr6.png",
                         "megaman/move_right/mr7.png", "megaman/move_right/mr8.png",
                         "megaman/move_right/mr9.png","megaman/move_right/mr10.png",
                         "megaman/move_right/mr11.png","megaman/move_right/mr12.png",
                         "megaman/move_right/mr13.png","megaman/move_right/mr14.png",
                         "megaman/move_right/mr15.png","megaman/move_right/mr16.png"]

        self.standLeft = ["megaman/stand/sl1.png","megaman/stand/sl2.png","megaman/stand/sl3.png"]
        self.standRight = ["megaman/stand/sr1.png","megaman/stand/sr2.png","megaman/stand/sr3.png"]

        self.shootLeft = ["megaman/shoot_left/shl1.png","megaman/shoot_left/shl2.png",
                          "megaman/shoot_left/shl3.png","megaman/shoot_left/shl4.png",
                          "megaman/shoot_left/shl5.png","megaman/shoot_left/shl6.png",
                          "megaman/shoot_left/shl7.png","megaman/shoot_left/shl8.png"]

        self.shootRight = ["megaman/shoot_right/shr1.png","megaman/shoot_right/shr2.png",
                          "megaman/shoot_right/shr3.png","megaman/shoot_right/shr4.png",
                          "megaman/shoot_right/shr5.png","megaman/shoot_right/shr6.png",
                          "megaman/shoot_right/shr7.png","megaman/shoot_right/shr8.png"]

        self.shootRightWalk = ["megaman/shoot_walk_right/swr1.png","megaman/shoot_walk_right/swr2.png",
                               "megaman/shoot_walk_right/swr3.png","megaman/shoot_walk_right/swr4.png",
                               "megaman/shoot_walk_right/swr5.png","megaman/shoot_walk_right/swr6.png",
                               "megaman/shoot_walk_right/swr7.png","megaman/shoot_walk_right/swr8.png",
                               "megaman/shoot_walk_right/swr9.png","megaman/shoot_walk_right/swr10.png",
                               "megaman/shoot_walk_right/swr11.png","megaman/shoot_walk_right/swr12.png",
                               "megaman/shoot_walk_right/swr13.png","megaman/shoot_walk_right/swr14.png","megaman/shoot_walk_right/swr15.png"]

        self.shootLeftWalk = ["megaman/shoot_walk_left/swl1.png","megaman/shoot_walk_left/swl2.png",
                               "megaman/shoot_walk_left/swl3.png","megaman/shoot_walk_left/swl4.png",
                               "megaman/shoot_walk_left/swl5.png","megaman/shoot_walk_left/swl6.png",
                               "megaman/shoot_walk_left/swl7.png","megaman/shoot_walk_left/swl8.png",
                               "megaman/shoot_walk_left/swl9.png","megaman/shoot_walk_left/swl10.png",
                               "megaman/shoot_walk_left/swl11.png","megaman/shoot_walk_left/swl12.png",
                               "megaman/shoot_walk_left/swl13.png","megaman/shoot_walk_left/swl14.png","megaman/shoot_walk_left/swl15.png"]

        self.shootJumpRight = ["megaman/jump_shoot_right/jsr1.png","megaman/jump_shoot_right/jsr2.png",
                              "megaman/jump_shoot_right/jsr3.png","megaman/jump_shoot_right/jsr4.png",
                              "megaman/jump_shoot_right/jsr5.png","megaman/jump_shoot_right/jsr6.png",
                              "megaman/jump_shoot_right/jsr7.png","megaman/jump_shoot_right/jsr8.png","megaman/jump_shoot_right/jsr9.png"]

        self.shootJumpLeft = ["megaman/jump_shoot_left/jsl1.png","megaman/jump_shoot_left/jsl2.png",
                              "megaman/jump_shoot_left/jsl3.png","megaman/jump_shoot_left/jsl4.png",
                              "megaman/jump_shoot_left/jsl5.png","megaman/jump_shoot_left/jsl6.png",
                              "megaman/jump_shoot_left/jsl7.png","megaman/jump_shoot_left/jsl8.png","megaman/jump_shoot_left/jsl9.png"]

        self.standFrame = 0
        self.jumpFrame = 0
        self.shootFrame = 0
        self.shootWalkFrame = 0
        self.shootJumpFrame = 0
        self.lastJumpFrame = time.time()
        self.lastStandFrame = time.time()
        self.direction = "right"
        self.rect.topleft = [x, y]
        self.frame = 0
        self.isShooting = False

    def update(self, up, down, left, right, shooting, shootUp, world,  speed = HORIZ_MOV_INCR, shootTime = SHOOTING_FREQUENCY):
        #Check for key presses
        self.isFlying = False
        self.flyDown = False
        if up:
            if self.canFly:
                self.isFlying = True
            if self.contact:
                if self.direction == "right":
                    self.image = pygame.image.load(self.jump_right[self.jumpFrame]).convert()
                    if time.time() - self.lastJumpFrame > JUMP_FRAMES_TIME:
                        self.jumpFrame = (self.jumpFrame + 1) % JUMP_FRAMES
                        self.lastJumpFrame = time.time()
                if not self.canFly:
                    self.jump = True
                else:
                    self.isFlying = True
                self.contact = False
        if down:
            if self.canFly and not self.contact:
                self.flyDown = True

        if self.direction == "right":
            self.image = pygame.image.load(self.standRight[self.standFrame]).convert()
            if time.time() - self.lastStandFrame > STAND_FRAMES_TIME:
                self.standFrame = ( self.standFrame + 1 ) % 3
                self.lastStandFrame = time.time()

        if self.direction == "left":
            self.image = pygame.image.load(self.standLeft[self.standFrame]).convert()
            if time.time() - self.lastStandFrame > STAND_FRAMES_TIME:
                self.standFrame = ( self.standFrame + 1 ) % 3
                self.lastStandFrame = time.time()

        if left:
            self.direction = "left"
            self.movx = -speed
            if self.contact:
                self.frame = (self.frame + 1) % RUN_FRAMES
                self.image = pygame.image.load(self.run_left[self.frame]).convert()
            else:
                self.image = pygame.image.load(self.jump_left[self.jumpFrame]).convert()
                if time.time() - self.lastJumpFrame > JUMP_FRAMES_TIME:
                    self.jumpFrame = (self.jumpFrame + 1) % JUMP_FRAMES
                    self.lastJumpFrame = time.time()

        if right:
            self.direction = "right"
            self.movx = +speed
            if self.contact:
                self.frame = (self.frame + 1) % RUN_FRAMES
                self.image = pygame.image.load(self.run_right[self.frame]).convert()
            else:
                self.image = pygame.image.load(self.jump_right[self.jumpFrame]).convert()
                if time.time() - self.lastJumpFrame > JUMP_FRAMES_TIME:
                    self.jumpFrame = (self.jumpFrame + 1) % JUMP_FRAMES
                    self.lastJumpFrame = time.time()

        if shooting and time.time() - self.lastShotTime > shootTime:
            self.isShooting = True
            if not shootUp:
                if self.direction == "right":
                    projectile = Rect(self.rect.right,self.rect.top + self.rect.h // 4,self.rect.w,self.rect.h // 10)
                    image = pygame.image.load("megaman/fires/fr1.png")
                    image.set_colorkey((255,255,255))

                else:
                    projectile = Rect(self.rect.left - self.rect.w // 2,self.rect.top + self.rect.h // 4,self.rect.w,self.rect.h // 10)
                    image = pygame.image.load("megaman/fires/fl1.png")
                    image.set_colorkey((255,255,255))

                info = {'projectile':projectile,'direction':self.direction,'image': image}
            else:
                projectile = Rect(self.rect.left,self.rect.top,self.rect.h // 10,self.rect.w)
                image = pygame.image.load("megaman/fires/fr1.png")
                image = pygame.transform.rotate(image,90)
                image.set_colorkey((255,255,255))
                info = {'projectile':projectile,'direction':"top",'image': image}
            self.projectiles.append(info)
            self.lastShotTime = time.time()

        #Update player position
        if not (left or right):
            self.movx = 0
        self.rect.right += self.movx

        self.collide(self.movx, 0, world)

        if not self.contact and not self.jump and not self.canFly:
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

        if self.flyDown:
            self.movy += 1
            self.rect.top += speed

        self.collide(0, self.movy, world)
        self.movx = 0
        self.movy = 0

        #If player is in shooting animation change image
        if self.isShooting:
            if self.contact and not left and not right:
                if self.direction == "right":
                    self.image = pygame.image.load(self.shootRight[self.shootFrame])
                else:
                    self.image = pygame.image.load(self.shootLeft[self.shootFrame])
                self.shootFrame = (self.shootFrame + 1) % SHOOT_FRAMES
                if self.shootFrame == 0:
                    self.isShooting = False
            elif self.contact:
                if self.direction == "left":
                    self.image = pygame.image.load(self.shootLeftWalk[self.shootWalkFrame])
                else:
                    self.image = pygame.image.load(self.shootRightWalk[self.shootWalkFrame])
                self.shootWalkFrame = (self.shootWalkFrame + 1) % WALK_SHOOT_FRAMES
                if self.shootWalkFrame == 0:
                    self.isShooting = False
            elif not self.contact:
                if self.direction == "left":
                    self.image = pygame.image.load(self.shootJumpLeft[self.shootJumpFrame])
                else:
                    self.image = pygame.image.load(self.shootJumpRight[self.shootJumpFrame])
                self.shootJumpFrame = (self.shootJumpFrame + 1) % JUMP_SHOOT_FRAMES
                if self.shootJumpFrame == 0:
                    self.isShooting = False

        #Transform image
        self.image = pygame.transform.scale(self.image,(PLAYER_WIDTH,PLAYER_HEIGHT))
        self.image.set_colorkey((255,255,255))

        #Check if invincibility must be disabled
        if self.startInvincibility != 0:
            if time.time() - self.startInvincibility > self.invincibilityTime:
                self.isInvincible = False
                self.startInvincibility = 0

        #Update projectiles
        for p in self.projectiles:
            if p.get('direction') == "right":
                p.get('projectile').left += 2 * HORIZ_MOV_INCR
            elif p.get('direction') == "left":
                p.get('projectile').left -= 2 * HORIZ_MOV_INCR
            elif p.get('direction') == "top":
                p.get('projectile').top -= 2 * HORIZ_MOV_INCR

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
                    self.jumpSpeed = VERTICAL_MOV_INCR
                    self.jump = False
                    self.maxJumpHeight = self.rect.height * 2
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                    self.jumpSpeed = VERTICAL_MOV_INCR
                    self.jump = False
                    self.maxJumpHeight = self.rect.height * 2

    #Checks for collided projectiles
    def collideProjectiles(self,projectiles,world,all_sprite,breakBlocks):

        if self.symbol == "P":
            for b in breakBlocks:
                for p in projectiles[:]:
                    if p.get('projectile').colliderect(b):
                        projectiles.remove(p)
                        world.remove(b)
                        breakBlocks.remove(b)
                        all_sprite.remove(b)

        for o in world:
            for p in projectiles[:]:
                if p.get('projectile').colliderect(o):
                    projectiles.remove(p)

    #checks for collisions with enemies
    def collideEnemies(self,enemies):
        #No need if player is invincible
        if self.isInvincible:
            return

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and time.time() - self.lastTimeDamaged > DAMAGE_DELAY:
                #TODO:Remove hardcoded reduction
                self.health -= 10
                self.lastTimeDamaged = time.time()
                if self.health < 0:
                    self.health = 0

    #initialize player position
    def initPosition(self,world):
        for o in world:
            if self.rect.colliderect(o):
                self.rect.bottom = o.rect.top

    #Makes player invincible for a while
    def setInvincible(self):
        self.isInvincible = True
        self.startInvincibility = time.time()

    #Add a coin to player stats
    def addCoin(self):
        self.coins += 1
