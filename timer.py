import pygame


class Timer:

    def __init__(self, ai_settings):
        self.imglist = list()
        self.wait = 1000
        self.index = 0
        self.index = self.index + 1 % len(self.imglist)
        self.last = pygame.time.get_ticks()

