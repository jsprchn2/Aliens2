import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # class to represent an alien

    def __init__(self, ai_settings, screen, type=3):
        # initialize alien
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.type = type

        # alien attributes
        self.images = None
        self.image = None
        self.image_index = None
        self.death_index = None
        self.last_frame = None
        self.death_frames = None
        self.rect = None
        self.init_images()

        # alien sounds
        self.death_sound = pygame.mixer.Sound('sound/alien_death.wav')
        self.bullet_sound = pygame.mixer.Sound('sound/alien_laser.wav')
        self.death_sound.set_volume(0.2)
        self.bullet_sound.set_volume(0.2)
        self.channel = ai_settings.alien_channel

        # start each new alien near the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the aliens position
        self.x = float(self.rect.x)

        # death flag
        self.dead = False

    def check_edges(self):
        # return true if alien is at edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # move alien right and left
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        # draw the alien at current position
        self.screen.blit(self.image, self.rect)

