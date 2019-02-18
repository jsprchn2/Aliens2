import pygame
from pygame import sprite, Surface, PixelArray
from random import randrange


class Bunker(sprite.Sprite):

    def __init__(self, ai_settings, screen, row, col):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/bunkerstill.png')
        # self.height = ai_settings.bunker_size
        # self.width = ai_settings.bunker_size
        # self.image = Surface((self.width, self.height))
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col
        self.dmg = False

    def update(self):
        self.screen.blit(self.image, self.rect)
