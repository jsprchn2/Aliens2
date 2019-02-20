import sys
import pygame
import random

from alien import Alien
from bullet import Bullet
from laser import Laser
from hi_scores import HiScoreScreen
from button import Button, Menu, show_level
from UFO import Ufo


def check_events(ai_settings, screen, stats, ship, bullets):
    # handle key inputs and releases
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats.game_active, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def start_new_game(ai_settings, screen, stats, sb,
                   ship, aliens, lasers, bullets):
    # start new game when clicking play button
    # Hide mouse
    pygame.mouse.set_visible(False)
    # Reset settings
    ai_settings.initialize_dynamic_settings()
    # Reset game stats
    stats.reset_stats()
    stats.game_active = True
    # Reset scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # Remove all aliens and bullets
    aliens.empty()
    bullets.empty()
    lasers.empty()
    # Create new alien fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    stats.next_spdup = len(aliens) - (len(aliens) // 5)
    stats.aliens_left = len(aliens)
    ship.center_ship()


def check_keydown_events(event, ai_settings, screen, game_active, ship, bullets):
    # handle key input
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and game_active:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    # handle key release
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    # fire bullets
    for i in range(3):
        new_bullet = Bullet(ai_settings=ai_settings, screen=screen, ship=ship, yoffset=i * 0.5 * ship.rect.height)
        ship.fire_laser()
        bullets.add(new_bullet)
    bullets.update()


def fire_random_laser(ai_settings, screen, aliens, lasers):
    # random laser from random alien
    firing_alien = random.choice(aliens.sprites())
    if len(lasers) < ai_settings.lasers_allowed and \
            (ai_settings.laser_stamp is None or
             (abs(pygame.time.get_ticks() - ai_settings.laser_stamp) > ai_settings.beam_time)):
        new_laser = Laser(ai_settings, screen, firing_alien)
        firing_alien.fire_laser()
        lasers.add(new_laser)


def alien_collision_check(bullet, alien):
    if alien.dead:
        return False
    return pygame.sprite.collide_rect(bullet, alien)


def check_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    # check for any hit aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False, collided=alien_collision_check)
    if collisions:
        for aliens_hit in collisions.values():
            for a in aliens_hit:
                stats.score += ai_settings.alien_points[str(a.alien_type)]
                a.now_die()
            sb.prep_score()
        check_high_score(stats, sb)
    ufo_collide = pygame.sprite.groupcollide(bullets, ufo, True, False, collided=alien_collision_check)
    if ufo_collide:
        for ufo in ufo_collide.values():
            for u in ufo:
                stats.score += u.score
                u.death_begins()
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # remove all bullets, remake fleet, and spd up
        if ufo:
            for u in ufo.sprites():
                # kill ufo
                u.kill()
        lasers.empty()
        bullets.empty()
        stats.level += 1
        # display current level
        show_level(ai_settings, screen, stats)
        # increase the base speed, reset speed to base
        ai_settings.increase_base_spd()
        ai_settings.reset_alien_spd()
        sb.prep_level()     # setup scoreboard
        create_fleet(ai_settings, screen, ship, aliens)
        # get next speed up
        stats.next_spdup = len(aliens) - (len(aliens) // 5)
    stats.aliens_left = len(aliens)
    if stats.aliens_left <= stats.next_spdup and ai_settings.alien_spd_factor < ai_settings.alien_spd_limit:
        # if low aliens, and havent hit the limit then speed up
        ai_settings.increase_alien_spd()
        stats.next_spdup = stats.aliens_left - (stats.aliens_left // 5)


def check_ship_laser_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    # check for laser ship collisions
    collide = pygame.sprite.spritecollideany(ship, lasers)
    if collide:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)


def check_bunker_collisions(lasers, bullets, bunkers):
    # check for laser, bullet collision against bunker
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)
    for b_list in collisions.values():
        for block in b_list:
            block.damage(top=False)
    collisions = pygame.sprite.groupcollide(lasers, bunkers, True, False)
    for b_list in collisions.values():
        for block in b_list:
            block.damage(top=True)


def update_bullets_lasers(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    # update all bullets and lasers
    bullets.update()
    lasers.update()
    # Remove bullets out of screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for laser in lasers.copy():
        if laser.rect.bottom > ai_settings.screen_height:
            lasers.remove(laser)
    check_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
    check_ship_laser_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)


def check_high_score(stats, sb):
    # check for new hi score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, bunkers, ufo_group):
    # update screen
    if stats.game_active:
        ufo_event_check(ai_settings, screen, ufo_group)
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Redraw all lasers
    for laser in lasers.sprites():
        laser.blitme()
    if ufo_group:
        ufo_group.update()
        for ufo in ufo_group.sprites():
            ufo.blitme()
    aliens.draw(screen)
    check_bunker_collisions(lasers, bullets, bunkers)
    sb.show_score()
    ship.blitme()
    bunkers.update()
    pygame.display.flip()


def get_number_aliens(ai_settings, alien_width):
    # get number of aliens to fit in row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # get number of rows to fit aliens
    available_space_y = (ai_settings.screen_height - (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufo):
    # ship hit by alien laser
    if ufo:     # ufos play sound, so kill them first so the death sound is clear
        for u in ufo.sprites():
            u.kill()
    ship.death()
    ship.update()
    while ship.dead:
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        pygame.display.flip()
        ship.update()
    if stats.ships_left > 0:
        # reduce lives by 1
        stats.ships_left -= 1
        # Remove all aliens, lasers and bullets
        aliens.empty()
        bullets.empty()
        lasers.empty()
        # remake fleet and center ship
        ai_settings.reset_alien_spd()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.next_spdup = len(aliens) - (len(aliens) // 5)
        stats.aliens_left = len(aliens.sprites())
        ship.center_ship()
        # Update score
        sb.prep_ships()
    else:
        ai_settings.stop_bgm()
        pygame.mixer.music.load('sound/game_over_yea.wav')
        pygame.mixer.music.play()
        stats.game_active = False
        stats.save_high_score()
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    # check if any aliens reach bottom
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # same as when ship is hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    # check if any aliens reach edge and update
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
    # check if any aliens reach bottom
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo)
    if aliens.sprites():
        fire_random_laser(ai_settings, screen, aliens, lasers)


def create_alien(ai_settings, screen, aliens, alien_num, row_num):
    # make alien and place in row
    if row_num < 1:
        alien_type = 3
    elif row_num < 3:
        alien_type = 2
    else:
        alien_type = 1
    alien = Alien(ai_settings, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.25 * alien_width * alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.25 * alien.rect.height * row_num
    alien.rect.y += int(ai_settings.screen_height / 8)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # create alien fleet
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_num in range(number_rows):
        for alien_num in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_num, row_num)


def change_fleet_direction(ai_settings, aliens):
    # drop down fleet and go in other direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_spd
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    # check alien fleet edges
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def create_random_ufo(ai_settings, screen):
    # make random ufo
    ufo = None
    if random.randrange(0, 100) <= 25:
        ufo = Ufo(ai_settings, screen)
    time_stamp = pygame.time.get_ticks()
    return time_stamp, ufo


def ufo_event_check(ai_settings, screen, ufo_group):
    # check ufo
    if not ai_settings.last_UFO and not ufo_group:
        ai_settings.last_UFO, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)
    elif abs(pygame.time.get_ticks() - ai_settings.last_UFO) > ai_settings.UFO_min_interval and not ufo_group:
        ai_settings.last_UFO, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)


def high_score_screen(ai_settings, game_stats, screen):
    # show hi scores
    hs_screen = HiScoreScreen(ai_settings, screen, game_stats)
    back_button = Button(ai_settings, screen, 'Back To Menu', y_factor=0.85)

    while True:
        back_button.change_text_color(*pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_button(*pygame.mouse.get_pos()):
                    return True
        screen.fill(ai_settings.bg_color)
        hs_screen.show_scores()
        back_button.draw_button()
        pygame.display.flip()


def startup_screen(ai_settings, game_stats, screen):
    # show menu
    menu = Menu(ai_settings, game_stats, screen)
    play_button = Button(ai_settings, screen, 'Play Game', y_factor=0.85)
    hiscore_button = Button(ai_settings, screen, 'High Scores', y_factor=0.95)
    intro = True

    while intro:
        play_button.change_text_color(*pygame.mouse.get_pos())
        hiscore_button.change_text_color(*pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                game_stats.game_active = play_button.check_button(click_x, click_y)
                intro = not game_stats.game_active
                if hiscore_button.check_button(click_x, click_y):
                    ret_hs = high_score_screen(ai_settings, game_stats, screen)
                    if not ret_hs:
                        return False
        screen.fill(ai_settings.bg_color)
        menu.show_menu()
        hiscore_button.draw_button()
        play_button.draw_button()
        pygame.display.flip()

    return True


def play_bgm(ai_settings, stats):
    # play music if game is active
    if stats.game_active:
        ai_settings.continue_bgm()
