import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # class to manage bullets

    def __init__(self, ai_settings, screen, ship, yoffset=0):
        # bullet object at ships position
        super(Bullet, self).__init__()
        self.screen = screen

        # create a bullet rect at correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top - yoffset

        # store bullets position as decimal value
        self.y = float(self.rect.y - yoffset)

        self.color = ai_settings.bullet_color
        self.spd_factor = ai_settings.bullet_spd_factor

    def update(self):
        # move bullet up screen
        # update decimal position
        self.y -= self.spd_factor
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        # draw bullet
        pygame.draw.rect(self.screen, self.color, self.rect)

