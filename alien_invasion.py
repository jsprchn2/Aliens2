import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from menu import Menu
import game_functions as gf


def run_game():
    # initialize game, create screen
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    menu = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    # make play button
    play_button = Button(ai_settings, screen, "Play")
    high_score = Button(ai_settings, screen, "High Scores")

    # create an instance to store stats and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    start = Menu(ai_settings, menu)

    # set background
    # bg_color = (230, 230, 230)

    # make ship, group to store bullets and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # make alien fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # start main loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, high_score, ship,
                        aliens, bullets, start)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button, high_score, start)


run_game()
