import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # class to represent an alien or aliens

    def __init__(self, ai_settings, screen, alientype=3):
        # initialize alien
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.type = alientype

        # alien attributes
        self.images = None
        self.image = None
        self.image_index = None
        self.death_index = None
        self.last_frame = None
        self.death_frames = None
        self.rect = None
        self.init_aliens()

        # alien sounds
        self.death_sound = pygame.mixer.Sound('sound/alien_death.wav')
        self.laser_sound = pygame.mixer.Sound('sound/alien_laser.wav')
        self.death_sound.set_volume(0.2)
        self.laser_sound.set_volume(0.2)
        self.channel = ai_settings.alien_channel

        # start each new alien near the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the aliens position
        self.x = float(self.rect.x)

        # death flag
        self.dead = False

    def init_aliens(self):
        if self.type == 1:
            self.images = [pygame.image.load('images/simple.png'),
                           pygame.image.load('images/simple1.png')]
            self.death_frames = [pygame.image.load('images/deaths/deadsimple.png'),
                                 pygame.image.load('images/deaths/deadsimple1.png'),
                                 pygame.image.load('images/deaths/deadsimple2.png'),
                                 pygame.image.load('images/deaths/deadsimple3.png'),
                                 pygame.image.load('images/deaths/deadsimple4.png')]
        elif self.type == 2:
            self.images = [pygame.image.load('images/rotate.png'),
                           pygame.image.load('images/rotate1.png')]
            self.death_frames = [pygame.image.load('images/deaths/deadrotate.png'),
                                 pygame.image.load('images/deaths/deadrotate1.png'),
                                 pygame.image.load('images/deaths/deadrotate2.png'),
                                 pygame.image.load('images/deaths/deadrotate3.png'),
                                 pygame.image.load('images/deaths/deadrotate4.png')]
        else:
            self.images = [pygame.image.load('images/expand.png'),
                           pygame.image.load('images/expand1.png')]
            self.death_frames = [pygame.image.load('images/deaths/deadexpand.png'),
                                 pygame.image.load('images/deaths/deadexpand1.png'),
                                 pygame.image.load('images/deaths/deadexpand2.png'),
                                 pygame.image.load('images/deaths/deadexpand3.png'),
                                 pygame.image.load('images/deaths/deadexpand4.png')]

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.last_frame = pygame.time.get_ticks()

    def fire_laser(self):
        self.channel.play(self.laser_sound)

    def now_die(self):
        self.dead = True
        self.death_index = 0
        self.image = self.death_frames[self.death_index]
        self.last_frame = pygame.time.get_ticks()
        self.channel.play(self.death_sound)

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
        time = pygame.time.get_ticks()
        if not self.dead:
            if abs(self.last_frame - time) > 1000:
                self.last_frame = time
                self.image_index = (self.image_index + 1) % len(self.images)
                self.image = self.images[self.image_index]
        else:
            if abs(self.last_frame - time) > 20:
                self.last_frame = time
                self.death_index += 1
                if self.death_index >= len(self.death_frames):
                    self.kill()
                else:
                    self.image = self.death_frames[self.death_index]

    def blitme(self):
        # draw the alien at current position
        self.screen.blit(self.image, self.rect)

