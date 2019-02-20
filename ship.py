import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        # initialize ship and start position
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the ship image
        self.image = pygame.image.load('images/ship.png')
        self.ship_img = self.image
        self.laser_frames = [pygame.image.load('images/ship1.png'),
                             pygame.image.load('images/ship2.png')]
        self.death_frames = [pygame.image.load('images/deaths/deadship.png'),
                             pygame.image.load('images/deaths/deadship1.png'),
                             pygame.image.load('images/deaths/deadship2.png'),
                             pygame.image.load('images/deaths/deadship3.png'),
                             pygame.image.load('images/deaths/deadship4.png'),
                             pygame.image.load('images/deaths/deadship5.png')]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.death_index = None
        self.laser_index = None
        self.last_frame = None

        self.dead_ship_sound = pygame.mixer.Sound('sound/ship_death.wav')
        self.ship_laser = pygame.mixer.Sound('sound/ship_laser.wav')
        self.dead_ship_sound.set_volume(0.4)
        self.ship_laser.set_volume(0.4)
        self.channel = ai_settings.ship_channel

        # start at bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store decimal value for ships center
        self.center = float(self.rect.centerx)

        # movement flag
        self.moving_right = False
        self.moving_left = False
        self.dead = False
        self.fire = False

    def update(self):
        # update ship position
        if not self.dead:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_spd_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_spd_factor

        # update rect object from self.center
            self.rect.centerx = self.center
        else:
            time = pygame.time.get_ticks()
            if abs(time - self.last_frame) > 250:
                self.death_index += 1
                if self.death_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_index]
                    self.last_frame = time
                else:
                    self.dead = False
                    self.image = self.ship_img

    def fire_laser(self):
        self.channel.play(self.ship_laser)
        """if not self.fire:
            self.image = self.laser_frames[self.laser_index]
            self.channel.play(self.ship_laser)
        else:
            self.image = self.ship_img"""

    def death(self):
        self.dead = True
        self.death_index = 0
        self.image = self.death_frames[self.death_index]
        self.last_frame = pygame.time.get_ticks()
        self.channel.play(self.dead_ship_sound)

    def blitme(self):
        # draw ship at current position
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # center ship
        self.center = self.screen_rect.centerx

