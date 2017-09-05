import pygame
from pygame.locals import *
import sys

CAMERA_DISTANCE = 25

class Camera(object):
    '''Class for center screen on the player'''
    def __init__(self, screenInfo, player, level_width, level_height):
        self.player = player
        self.rect = Rect(0,0,screenInfo.current_w,screenInfo.current_h)
        self.rect.center = self.player.center
        self.world_rect = Rect(0, 0, level_width, level_height)

    #Follow player
    def update(self):
      if self.player.centerx > self.rect.centerx + CAMERA_DISTANCE:
          self.rect.centerx = self.player.centerx - CAMERA_DISTANCE
      if self.player.centerx < self.rect.centerx - CAMERA_DISTANCE:
          self.rect.centerx = self.player.centerx + CAMERA_DISTANCE
      if self.player.centery > self.rect.centery + CAMERA_DISTANCE:
          self.rect.centery = self.player.centery - CAMERA_DISTANCE
      if self.player.centery < self.rect.centery - CAMERA_DISTANCE:
          self.rect.centery = self.player.centery + CAMERA_DISTANCE
      self.rect.clamp_ip(self.world_rect)

    #Draw sprites on screen
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                if s.symbol == "P" and not s.isDead:
                    surf.blit(s.image, self.RelRect(s, self))
                else:
                    surf.blit(s.image, self.RelRect(s, self))
                #Check if it is the player
                if s.symbol == "P" or s.symbol == "e2" or s.symbol == "e3":
                    for p in s.projectiles:
                        pRect = p.get('projectile')
                        if pRect.colliderect(self.rect):
                            image = p.get('image')
                            image = pygame.transform.scale(image,(pRect.w,pRect.h))
                            surf.blit(image,self.RelRectProject(p.get('projectile'),self))

    #Measure displacement of camera to show the player
    def RelRect(self,actor, camera):
        return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

    #Measure displacement of camera for projectile
    def RelRectProject(self,projectile,camera):
        return pygame.Rect(projectile.x-camera.rect.x, projectile.y-camera.rect.y, projectile.w, projectile.h)

    #Get visible objects on screen
    def getVisibleObjects(self,world,sprites):
        visibleObjects = []
        visibleSprites = []
        for o in world:
            if o.rect.colliderect(self.rect):
                visibleObjects.append(o)
        for s in sprites:
            if s.rect.colliderect(self.rect):
                visibleSprites.append(s)
        return visibleObjects,visibleSprites
