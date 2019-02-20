import pygame

import game_functions as gf

from game_stats import GameStats
from scoreboard import Scoreboard
from bunker import create_bunker
from settings import Settings
from ship import Ship


def run_game():
    # setup pygame, settings, and display
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    # setup game stats and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # setup ship, bullets, beams, aliens and bunkers
    ship = Ship(ai_settings, screen)
    bullets = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    ufo = pygame.sprite.Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)
    bunkers = pygame.sprite.Group(create_bunker(ai_settings, screen, 0),
                                  create_bunker(ai_settings, screen, 1),
                                  create_bunker(ai_settings, screen, 2),
                                  create_bunker(ai_settings, screen, 3))

    while True:
        clock.tick(70)  # 70 fps
        if not stats.game_active:
            quit_game = not gf.startup_screen(ai_settings, stats, screen)
            if quit_game:
                pygame.quit()
                break
            gf.start_new_game(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets)
        gf.check_events(ai_settings, screen, stats, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets_lasers(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, bunkers, ufo)
        gf.play_bgm(ai_settings, stats)


run_game()
