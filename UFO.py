import pygame
from pygame.sysfont import SysFont
from random import choice


class Ufo(pygame.sprite.Sprite):

    def __init__(self, ai_settings, screen, sound=True):
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings
        self.possible_scores = ai_settings.UFO_pts
        self.score = None

        self.image = pygame.image.load('images/face.png')
        self.rect = self.image.get_rect()
        self.score_image = None
        self.font = SysFont(None, 32, bold=True)
        self.prep_score()

        self.death_frames = [pygame.image.load('images/deaths/deadface.png'),
                             pygame.image.load('images/deaths/deadface1.png'),
                             pygame.image.load('images/deaths/deadface2.png'),
                             pygame.image.load('images/deaths/deadface3.png'),
                             pygame.image.load('images/deaths/deadface4.png'),
                             pygame.image.load('images/deaths/deadface5.png')]
        self.death_index = None
        # self.death_frames.append(pygame.image.load('images/deaths/deadface.png'))
        self.death_frames.append(self.score_image)
        self.last_frame = None
        self.wait_interval = 500

        self.entrance_sound = pygame.mixer.Sound('sound/UFO_entrance.wav')
        self.death_sound = pygame.mixer.Sound('sound/UFO_death.wav')
        self.entrance_sound.set_volume(0.6)
        self.channel = ai_settings.ufo_channel

        self.speed = ai_settings.ufo_spd * (choice([-1, 1]))
        self.rect.x = 0 if self.speed > 0 else ai_settings.screen_width
        self.rect.y = ai_settings.screen_height * 0.1

        self.dead = False

        if sound:
            self.channel.play(self.entrance_sound, loops=-1)

    def kill(self):
        self.channel.stop()
        super().kill()

    def death_begins(self):
        self.channel.stop()
        self.channel.play(self.death_sound)
        self.dead = True
        self.death_index = 0
        self.image = self.death_frames[self.death_index]
        self.last_frame = pygame.time.get_ticks()

    def score(self):
        self.score = choice(self.possible_scores)
        return self.score

    def prep_score(self):
        score_str = str(self.get_score())
        self.score_image = self.font.render(score_str, True, (255, 0, 0), self.ai_settings.bg_color)

    def update(self):
        if not self.dead:
            self.rect.x += self.speed
            if self.speed > 0 and self.rect.left > self.ai_settings.screen_width:
                self.kill()
            elif self.rect.right < 0:
                self.kill()
        else:
            time = pygame.time.get_ticks()
            if abs(time - self.last_frame) > self.wait_interval:
                self.last_frame = time
                self.death_index += 1
                if self.death_index >= len(self.death_frames):
                    self.kill()
                else:
                    self.image = self.death_frames[self.death_index]
                    self.wait_interval += 500

    def get_score(self):
        # get random score of ufo pt value
        self.score = choice(self.possible_scores)
        return self.score

    def blitme(self):
        self.screen.blit(self.image, self.rect)

