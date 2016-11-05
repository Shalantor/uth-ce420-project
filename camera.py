import pygame
from pygame.locals import *
import sys

class Camera(object):
    '''Class for center screen on the player'''
    def __init__(self, screen, player, level_width, level_height):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.world_rect = Rect(0, 0, level_width, level_height)

    def update(self):
      if self.player.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.player.centerx - 25
      if self.player.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.player.centerx + 25
      if self.player.centery > self.rect.centery + 25:
          self.rect.centery = self.player.centery - 25
      if self.player.centery < self.rect.centery - 25:
          self.rect.centery = self.player.centery + 25
      self.rect.clamp_ip(self.world_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, self.RelRect(s, self))
                #Check if it is the player
                if s.symbol == "P":
                    for p in s.projectiles:
                        pRect = p.get('projectile')
                        if pRect.colliderect(self.rect):
                            image = s.projectileImage
                            image = pygame.transform.scale(image,(pRect.w,pRect.h))
                            surf.blit(image,self.RelRectProject(p.get('projectile'),self))

    def RelRect(self,actor, camera):
        return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

    def RelRectProject(self,projectile,camera):
        return pygame.Rect(projectile.x-camera.rect.x, projectile.y-camera.rect.y, projectile.w, projectile.h)
