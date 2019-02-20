import pygame


class Laser(pygame.sprite.Sprite):

    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/alien_laser.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)
        self.spd_factor = ai_settings.laser_spd_factor

    def update(self):
        # update laser
        self.y += self.spd_factor
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

