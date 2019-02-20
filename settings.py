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

        self.bunker_size = 10
        self.bunker_color = (0, 0, 255)

        self.laser_spd_factor = None
        self.lasers_allowed = 1

        # alien settings
        self.fleet_drop_spd = 5

        # how quick game spds up
        self.spdup_scale = 1.1

        # how quick alien points increase
        self.score_scale = 1.5

        # sound
        self.audio_channels = 5
        self.ship_channel = mixer.Channel(0)
        self.alien_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)
        self.ufo_channel = mixer.Channel(3)
        self.music_channel = mixer.Channel(4)
        self.normal_music_interval = 725
        self.music_interval = self.normal_music_interval
        self.music_spdup = 25
        self.bgm = [
            mixer.Sound('sound/bgm1.wav'),
            mixer.Sound('sound/bgm2.wav'),
            mixer.Sound('sound/bgm3.wav')
        ]
        self.bgm_index = None
        self.last_beat = None

        self.norm_alien_spd = 2
        self.alien_spd_limit = None
        self.alien_base_limit = None
        self.alien_spd_factor = None
        self.UFO_spd = None
        self.last_UFO = None
        self.UFO_min_interval = 10000
        self.fleet_drop_spd = 10
        self.fleet_direction = None
        self.alien_pts = None
        self.UFO_pts = [50, 100, 150]
        self.laser_stamp = None
        self.laser_time = 1000

        self.initialize_dynamic_settings()
        # self.initialize_audio_settings()

    """def initialize_audio_settings(self):
        mixer.init()
        mixer.set_num_channels(self.audio_channels)
        self.music_channel.set_volume(0.7)"""

    def initialize_dynamic_settings(self):
        # initialize settings
        self.ship_spd_factor = 5
        self.bullet_spd_factor = 3
        self.laser_spd_factor = 2
        self.alien_spd_factor = self.norm_alien_spd
        self.alien_spd_limit = self.alien_spd_factor * 5
        self.alien_base_limit = self.alien_spd_limit / 2
        self.ufo_spd = self.alien_spd_factor * 2

        # fleet direction, 1 = right, -1 = left
        self.fleet_direction = 1

        # scoring
        self.alien_points = {'1': 10, '2': 20, '3': 40}

    def increase_spd(self):
        # increase spd settings and alien points
        self.ship_spd_factor *= self.spdup_scale
        self.bullet_spd_factor *= self.spdup_scale
        self.alien_spd_factor *= self.spdup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

    def increase_alien_spd(self):
        self.alien_spd_factor *= self.spdup_scale
        self.music_interval -= self.music_spdup

    def reset_alien_spd(self):
        self.alien_spd_factor = self.norm_alien_spd
        self.music_interval = self.normal_music_interval

    def increase_base_spd(self):
        if self.norm_alien_spd < self.alien_base_limit:
            self.norm_alien_spd *= self.spdup_scale
            self.normal_music_interval -= self.music_spdup

    def continue_bgm(self):
        if not self.last_beat:
            self.bgm_index = 0
            self.music_channel.play(self.bgm[self.bgm_index])
            self.last_beat = time.get_ticks()
        elif abs(self.last_beat - time.get_ticks()) > self.music_interval and not self.music_channel.get_busy():
            self.bgm_index = (self.bgm_index + 1) % len(self.bgm)
            self.music_channel.play(self.bgm[self.bgm_index])
            self.last_beat = time.get_ticks()

    def stop_bgm(self):
        self.music_channel.stop()
        self.last_beat = None
        self.bgm_index = None

