from pygame import mixer
from pygame import time


class Settings:
    # store settings

    def __init__(self):
        # initialize game settings
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # alien settings
        self.fleet_drop_speed = 5

        # how quick game speeds up
        self.speedup_scale = 1.1

        # how quick alien points increase
        self.score_scale = 1.5

        # sound
        self.audio_channels = 5
        self.ship_channel = mixer.Channel(0)
        self.alien_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)
        self.ufo_channel = mixer.Channel(3)

        self.norm_alien_spd = 2
        self.alien_speed_limit = None
        self.alien_base_limit = None
        self.alien_speed_factor = None
        self.UFO_spd = None
        self.last_UFO = None
        self.UFO_min_intv = 10000
        self.fleet_drop_spd = 10
        self.fleet_direction = None
        self.alien_pts = None
        self.UFO_pts = [50, 100, 150]

        self.initialize_dynamic_settings()
        # self.initialize_audio_settings()

    # def initialize_audio_settings(self):
        # mixer.init()
        # mixer.set_num_channels(self.audio_channels)
        # self.music_channel.set_volume(0.7)

    def initialize_dynamic_settings(self):
        # initialize settings
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet direction, 1 = right, -1 = left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

    def increase_speed(self):
        # increase speed settings and alien points
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

