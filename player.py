import pygame
from pygame.locals import *
import sys
from level import *
from camera import *
import time

class Player(pygame.sprite.Sprite):
    '''class for player and collision'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #Player specific constants
        self.horiz_mov_incr = 10
        self.vertical_mov_incr = 20
        self.min_vertical_speed = 15
        self.shooting_frequency = 0.2
        self.damage_delay = 2
        self.damage = 20
        self.stand_frames = 3
        self.stand_frames_time = 0.2
        self.run_frames = 16
        self.jump_frames = 9
        self.jump_frames_time = 0.4
        self.player_width = 45
        self.player_height = 70
        self.shoot_frames = 8
        self.walk_shoot_frames = 15
        self.jump_shoot_frames = 9
        self.fly_frames = 6
        self.combo_frames = 8

        #Other player variables
        self.isDead = False
        self.isDeadStartTime = 0
        self.lastShotTime = 0
        self.symbol = "P"
        self.projectileImage = pygame.image.load("megaman/fires/fr1.png").convert()
        self.comboImage = pygame.image.load("megaman/fires/combo.png").convert()
        self.projectileImage.set_colorkey((255,255,255))
        self.projectiles = []
        self.coins = 0
        self.canFly = False
        self.isFlying = False
        self.flyDown = False
        self.health = 100
        self.energy = 100
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.fallSpeed = 0
        self.jumpSpeed = self.vertical_mov_incr
        self.contact = False
        self.jump = False
        self.image = pygame.image.load("megaman/stand/sr1.png").convert()
        self.image = pygame.transform.scale(self.image,(40,60))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.startJumpHeight = self.rect.height * 2
        self.maxJumpHeight = self.startJumpHeight
        self.lastTimeDamaged = time.time() - self.damage_delay
        self.isInvincible = False
        self.invincibilityTime = 5
        self.startInvincibility = 0
        self.hasWings = False
        self.hasKey = None
        self.flyFrameFrequency = 0.1

        #Variables for sound
        self.jumpSound = pygame.mixer.Sound('Sounds/Jump.ogg')
        self.damageSound = pygame.mixer.Sound('Sounds/Punch.ogg')
        self.shootSound = pygame.mixer.Sound('Sounds/Laser.ogg')
        self.pickupHealthSound = pygame.mixer.Sound('Sounds/Life_Pickup.ogg')
        self.coinSound = pygame.mixer.Sound('Sounds/Cash.ogg')
        self.breakSound = pygame.mixer.Sound('Sounds/breakables.ogg')
        self.comboSound = pygame.mixer.Sound('Sounds/Laser_Blast.ogg')
        self.dyingSound = pygame.mixer.Sound('Sounds/Dying.ogg')
        self.invincibleSound = pygame.mixer.Sound('Sounds/Shield.ogg')

        #Variables for graphics
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

        self.flyRight = ["megaman/fly_right/rfly1.png","megaman/fly_right/rfly2.png",
                         "megaman/fly_right/rfly3.png","megaman/fly_right/rfly4.png",
                         "megaman/fly_right/rfly5.png","megaman/fly_right/rfly6.png"]

        self.flyLeft = ["megaman/fly_left/lfly1.png","megaman/fly_left/lfly2.png",
                         "megaman/fly_left/lfly3.png","megaman/fly_left/lfly4.png",
                         "megaman/fly_left/lfly5.png","megaman/fly_left/lfly6.png"]

        self.comboShootRight = ["megaman/combo_right/1.png","megaman/combo_right/2.png",
                                "megaman/combo_right/3.png","megaman/combo_right/4.png",
                                "megaman/combo_right/5.png","megaman/combo_right/6.png",
                                "megaman/combo_right/7.png","megaman/combo_right/8.png"]

        self.comboShootLeft = ["megaman/combo_left/1.png","megaman/combo_left/2.png",
                                "megaman/combo_left/3.png","megaman/combo_left/4.png",
                                "megaman/combo_left/5.png","megaman/combo_left/6.png",
                                "megaman/combo_left/7.png","megaman/combo_left/8.png"]

        self.flyRightImage = pygame.image.load("megaman/jump_right/jr6.png")
        self.flyLeftImage =  pygame.image.load("megaman/jump_left/jl6.png")

        self.comboFrame = 0
        self.standFrame = 0
        self.flyFrame = 0
        self.jumpFrame = 0
        self.shootFrame = 0
        self.shootWalkFrame = 0
        self.shootJumpFrame = 0
        self.lastComboTime = time.time()
        self.comboFrequency = 1
        self.lastFlyFrame = time.time()
        self.lastJumpFrame = time.time()
        self.lastStandFrame = time.time()
        self.direction = "right"
        self.rect.topleft = [x, y]
        self.frame = 0
        self.isShooting = False
        self.isComboing = False
        self.comboFrameFrequency = 0.01
        self.lastComboFrameChange = time.time()

    def update(self, up, down, left, right, shooting, shootUp, combo, world):
        #Check for key presses
        self.isFlying = False
        self.flyDown = False
        if up:
            if self.canFly:
                self.isFlying = True
                self.contact = False

                """TODO:Add sound for flying"""

            if self.contact:
                if self.direction == "right":
                    self.image = pygame.image.load(self.jump_right[self.jumpFrame]).convert()
                    if time.time() - self.lastJumpFrame > self.jump_frames_time:
                        self.jumpFrame = (self.jumpFrame + 1) % self.jump_frames
                        self.lastJumpFrame = time.time()
                if not self.canFly:

                    """---JUMP SOUND---"""
                    if self.symbol == "P":
                        self.jumpSound.play()

                    self.jump = True
                else:
                    self.isFlying = True
                self.contact = False
        if down:
            if self.canFly and not self.contact:
                self.flyDown = True

        if self.direction == "right":
            self.image = pygame.image.load(self.standRight[self.standFrame]).convert()
            if time.time() - self.lastStandFrame > self.stand_frames_time:
                self.standFrame = ( self.standFrame + 1 ) % self.stand_frames
                self.lastStandFrame = time.time()

        if self.direction == "left":
            self.image = pygame.image.load(self.standLeft[self.standFrame]).convert()
            if time.time() - self.lastStandFrame > self.stand_frames_time:
                self.standFrame = ( self.standFrame + 1 ) % self.stand_frames
                self.lastStandFrame = time.time()

        if left:
            self.direction = "left"
            self.movx = - self.horiz_mov_incr
            if self.contact:
                self.frame = (self.frame + 1) % self.run_frames
                self.image = pygame.image.load(self.run_left[self.frame]).convert()
            elif self.canFly:
                if not self.flyFrame == self.fly_frames - 1 and time.time() - self.lastFlyFrame > self.flyFrameFrequency:
                    self.flyFrame = self.flyFrame + 1
                    self.lastFlyFrame = time.time()
                self.image = pygame.image.load(self.flyLeft[self.flyFrame]).convert()
            else:
                self.image = pygame.image.load(self.jump_left[self.jumpFrame]).convert()
                if time.time() - self.lastJumpFrame > self.jump_frames_time:
                    self.jumpFrame = (self.jumpFrame + 1) % self.jump_frames
                    self.lastJumpFrame = time.time()

        if right:
            self.direction = "right"
            self.movx = + self.horiz_mov_incr
            if self.contact:
                self.frame = (self.frame + 1) % self.run_frames
                self.image = pygame.image.load(self.run_right[self.frame]).convert()
            elif self.canFly:
                if not self.flyFrame == self.fly_frames - 1 and time.time() - self.lastFlyFrame > self.flyFrameFrequency:
                    self.flyFrame = self.flyFrame + 1
                    self.lastFlyFrame = time.time()
                self.image = pygame.image.load(self.flyRight[self.flyFrame]).convert()
            else:
                self.image = pygame.image.load(self.jump_right[self.jumpFrame]).convert()
                if time.time() - self.lastJumpFrame > self.jump_frames_time:
                    self.jumpFrame = (self.jumpFrame + 1) % self.jump_frames
                    self.lastJumpFrame = time.time()

        #Reset fly frames
        if not left and not right:
            self.flyFrame = 0

        #Check for combo
        if combo and time.time() - self.lastComboTime > self.comboFrequency and not (left or right) and self.contact:
            self.comboSound.play()
            self.lastComboTime = time.time()
            if self.direction == "right":
                projectile = Rect(self.rect.right,self.rect.top,self.rect.w * 3,self.rect.h)
                image = self.comboImage
            else:
                projectile = Rect(self.rect.left,self.rect.top,self.rect.w * 3,self.rect.h)
                projectile.right = self.rect.left
                image = self.comboImage
                image = pygame.transform.rotate(image,180)
            image.set_colorkey((255,255,255))
            info = {'projectile':projectile,'direction':self.direction,'image': image,'normal':False, 'damage':self.damage * 3}
            self.projectiles.append(info)
            self.isComboing = True

        #Check for shooting
        if shooting and time.time() - self.lastShotTime > self.shooting_frequency and not self.isComboing:

            """---SHOOT SOUND---"""
            if self.symbol == "P":
                self.shootSound.play()

            self.isShooting = True
            if not shootUp:
                if self.direction == "right":
                    projectile = Rect(self.rect.right,self.rect.top + self.rect.h // 4,self.rect.w,self.rect.h // 10)
                    image = self.projectileImage
                else:
                    projectile = Rect(self.rect.left - self.rect.w // 2,self.rect.top + self.rect.h // 4,self.rect.w,self.rect.h // 10)
                    image = self.projectileImage
                    image = pygame.transform.rotate(image,180)
                image.set_colorkey((255,255,255))

                info = {'projectile':projectile,'direction':self.direction,'image': image,'normal':True, 'damage':self.damage}
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
            if self.fallSpeed > self.min_vertical_speed:
                self.fallSpeed = self.min_vertical_speed
            self.rect.top += self.fallSpeed

        if self.jump:
            self.movy -= 1
            self.rect.top -= self.jumpSpeed
            self.maxJumpHeight -= self.jumpSpeed
            self.jumpSpeed -= 1
            if self.jumpSpeed <= self.min_vertical_speed:
                self.jumpSpeed = self.min_vertical_speed
            if self.maxJumpHeight <= 0:
                self.maxJumpHeight = self.startJumpHeight
                self.jump = False

        if self.isFlying:
            self.movy -= 1
            self.rect.top -= self.horiz_mov_incr
            self.image = pygame.image.load(self.flyRight[self.fly_frames - 1])
            self.image = pygame.transform.rotate(self.image,90)

        if self.flyDown:
            self.movy += 1
            self.rect.top += self.horiz_mov_incr
            self.image = pygame.image.load(self.flyRight[self.fly_frames - 1])
            self.image = pygame.transform.rotate(self.image,-90)

        self.collide(0, self.movy, world)
        self.movx = 0
        self.movy = 0

        if self.canFly and left or right and self.flyFrame == self.fly_frames - 1:
            self.image = pygame.transform.scale(self.image,(self.player_height,self.player_width + 20))
        elif self.flyDown or self.isFlying:
            self.image = pygame.transform.scale(self.image,(self.player_width + 20,self.player_height))
        else:
            self.image = pygame.transform.scale(self.image,(self.player_width,self.player_height))

        #Reduce energy level if in air
        if not self.contact and self.canFly and self.symbol == "P":
            self.energy -= 0.3
            if self.energy <= 0:
                self.canFly = False

        #If player can fly change his idle flying animation
        if self.canFly and not (left or right):
            if self.direction == "right":
                self.image = self.flyRightImage
            else:
                self.image = self.flyLeftImage
            self.image = pygame.transform.scale(self.image,(self.player_width,self.player_height))

        #If player is in shooting animation change image
        if self.isShooting and not ((left or right) and self.canFly) and not self.isComboing:
            if self.contact and not left and not right:
                if self.direction == "right":
                    self.image = pygame.image.load(self.shootRight[self.shootFrame])
                elif self.direction == "left":
                    self.image = pygame.image.load(self.shootLeft[self.shootFrame])
                self.shootFrame = (self.shootFrame + 1) % self.shoot_frames
                if self.shootFrame == 0:
                    self.isShooting = False
            elif self.contact:
                if self.direction == "left":
                    self.image = pygame.image.load(self.shootLeftWalk[self.shootWalkFrame])
                elif self.direction == "right":
                    self.image = pygame.image.load(self.shootRightWalk[self.shootWalkFrame])
                self.shootWalkFrame = (self.shootWalkFrame + 1) % self.walk_shoot_frames
                if self.shootWalkFrame == 0:
                    self.isShooting = False
            elif not self.contact:
                if self.direction == "left":
                    self.image = pygame.image.load(self.shootJumpLeft[self.shootJumpFrame])
                elif self.direction == "right":
                    self.image = pygame.image.load(self.shootJumpRight[self.shootJumpFrame])
                self.shootJumpFrame = (self.shootJumpFrame + 1) % self.jump_shoot_frames
                if self.shootJumpFrame == 0:
                    self.isShooting = False
            self.image = pygame.transform.scale(self.image,(self.player_width + (self.rect.w // 3),self.player_height))
        elif self.isComboing:
            if time.time() - self.lastComboFrameChange > self.comboFrameFrequency:
                self.lastComboFrameChange = time.time()
                if self.direction == "right":
                    self.image = pygame.image.load(self.comboShootRight[self.comboFrame])
                elif self.direction == "left":
                    self.image = pygame.image.load(self.comboShootLeft[self.comboFrame])
                self.comboFrame = (self.comboFrame + 1 ) % self.combo_frames
                if self.comboFrame == 0:
                    self.isComboing = False
            self.image = pygame.transform.scale(self.image,(self.rect.w + 10,self.rect.h))


        #Transform image
        if self.symbol == "P":
            self.image.set_colorkey((255,255,255))

        #Check if invincibility must be disabled
        if self.startInvincibility != 0:
            if time.time() - self.startInvincibility > self.invincibilityTime:
                self.invincibleSound.stop()
                self.isInvincible = False
                self.startInvincibility = 0

        #Update projectiles
        for p in self.projectiles:
            if p.get('direction') == "right":
                p.get('projectile').left += 2 * self.horiz_mov_incr
            elif p.get('direction') == "left":
                p.get('projectile').left -= 2 * self.horiz_mov_incr
            elif p.get('direction') == "top":
                p.get('projectile').top -= 2 * self.horiz_mov_incr

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
                    self.jumpSpeed = self.vertical_mov_incr
                    self.jump = False
                    self.maxJumpHeight = self.startJumpHeight
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                    self.jumpSpeed = self.vertical_mov_incr
                    self.jump = False
                    self.maxJumpHeight = self.startJumpHeight

    #Checks for collided projectiles
    def collideProjectiles(self,projectiles,world,all_sprite,breakBlocks):

        if self.symbol == "P":
            for b in breakBlocks:
                for p in projectiles[:]:
                    if p.get('projectile').colliderect(b):
                        self.breakSound.play()
                        projectiles.remove(p)
                        world.remove(b)
                        breakBlocks.remove(b)
                        all_sprite.remove(b)

        for o in world:
            for p in projectiles[:]:
                if p.get('projectile').colliderect(o):
                    projectiles.remove(p)

    #checks for collisions with enemies
    def collideEnemies(self,enemies,visibleObjects):
        #No need if player is invincible
        if self.isInvincible:
            return

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and time.time() - self.lastTimeDamaged > self.damage_delay:

                """---TAKE DAMAGE SOUND---"""
                if self.symbol == "P":
                    self.damageSound.play()

                self.health -= enemy.damage
                self.lastTimeDamaged = time.time()
                if self.health <= 0:
                    self.health = 100
                    if self.symbol == "P":
                        self.dyingSound.play(-1)
                        pygame.mixer.music.stop()
                        self.isDead = True
                        self.isDeadStartTime = time.time()

    #initialize player position
    def initPosition(self,world):
        for o in world:
            if self.rect.colliderect(o):
                self.rect.bottom = o.rect.top

    #Makes player invincible for a while
    def setInvincible(self):
        self.isInvincible = True
        self.startInvincibility = time.time()
        """---SOUND FOR INVINCIBILITY---"""
        self.invincibleSound.play(-1,0)

    #Add a coin to player stats
    def addCoin(self):
        self.coins += 1
        """---COIN SOUND---"""
        if self.symbol == "P":
            self.coinSound.play()


    #Replenish health
    def replenishHealth(self,heart):
        if self.health == 100:
            return False

        """---HEALTH SOUND---"""
        if self.symbol == "P":
            self.pickupHealthSound.play()

        self.health += heart.healthValue
        if self.health > 100:
            self.health = 100
        return True
