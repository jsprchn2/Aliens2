from pygame.sysfont import SysFont
from pygame import display, time, image


class Button:
    # button text
    def __init__(self, settings, screen, msg, y_factor=0.65):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.button_color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.alt_color = (0, 0, 255)
        self.font = SysFont(None, 48)
        self.y_factor = y_factor

        # Prep button message
        self.msg = msg
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(self.text_color)

    def check_button(self, mouse_x, mouse_y):
        # check for button input
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def change_text_color(self, mouse_x, mouse_y):
        # change button color
        if self.check_button(mouse_x, mouse_y):
            self.prep_msg(self.alt_color)
        else:
            self.prep_msg(self.text_color)

    def prep_msg(self, color):
        # prep msg image
        self.msg_image = self.font.render(self.msg, True, color, self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = (self.settings.screen_width // 2)
        self.msg_image_rect.centery = int(self.settings.screen_height * self.y_factor)

    def draw_button(self):
        # draw the button
        self.screen.blit(self.msg_image, self.msg_image_rect)


class AlienDisplay:
    # display enemies and pts
    def __init__(self, ai_settings, screen, y_start):
        self.screen = screen
        self.settings = ai_settings
        self.aliens = []
        images = [
            image.load('images/simple.png'),
            image.load('images/rotate.png'),
            image.load('images/expand.png'),
            image.load('images/face.png')
        ]
        for img in images:
            self.aliens.append((img, img.get_rect()))
        self.example_scores = [
            Subtext(ai_settings.bg_color, self.screen, ' = ' + str(ai_settings.alien_points['1']),
                     text_color=(0, 0, 0)),
            Subtext(ai_settings.bg_color, self.screen, ' = ' + str(ai_settings.alien_points['2']),
                     text_color=(0, 0, 0)),
            Subtext(ai_settings.bg_color, self.screen, ' = ' + str(ai_settings.alien_points['3']),
                     text_color=(0, 0, 0)),
            Subtext(ai_settings.bg_color, self.screen, ' = ???', text_color=(0, 0, 0))
        ]
        self.score_images = []
        self.y_start = y_start
        self.prep_images()

    def prep_images(self):
        # prep all images
        y_offset = self.y_start
        for a, ex in zip(self.aliens, self.example_scores):
            a[1].centery = y_offset
            a[1].centerx = (self.settings.screen_width // 2) - a[1].width
            ex.prep_image()
            ex.image_rect.centery = y_offset
            ex.image_rect.centerx = (self.settings.screen_width // 2) + a[1].width
            y_offset += int(a[1].height * 1.5)

    def show_aliens(self):
        # show the aliens first frame with pts
        for a in self.aliens:
            self.screen.blit(a[0], a[1])
        for ex in self.example_scores:
            ex.blitme()


class Titletext:
    # Text
    def __init__(self, bg_color, screen, text, text_size=56, text_color=(0, 0, 0)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont(None, text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):

        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):

        self.screen.blit(self.image, self.image_rect)


class Subtext:

    def __init__(self, bg_color, screen, text, text_size=48, text_color=(0, 0, 0)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont(None, text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):

        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)


class Menu:
    # info for menu
    def __init__(self, settings, game_stats, screen):
        # settings, screen, and game stats
        self.settings = settings
        self.game_stats = game_stats
        self.screen = screen

        # text/image info
        self.titletext = Titletext(settings.bg_color, self.screen, 'Space', text_size=72)
        self.subtext = Subtext(settings.bg_color, self.screen, 'Invaders', text_size=62)
        self.alien_display = AlienDisplay(settings, self.screen, self.settings.screen_height // 3)
        self.prep_image()

    def prep_image(self):
        # render menu
        self.titletext.prep_image()
        self.titletext.image_rect.centerx = (self.settings.screen_width // 2)
        self.titletext.image_rect.centery = (self.settings.screen_height // 5) - self.titletext.image_rect.height
        self.subtext.prep_image()
        self.subtext.image_rect.centerx = (self.settings.screen_width // 2)
        self.subtext.image_rect.centery = (self.settings.screen_height // 5) + (self.titletext.image_rect.height // 3)

    def show_menu(self):
        # draw the menu
        self.titletext.blitme()
        self.subtext.blitme()
        self.alien_display.show_aliens()


def show_level(ai_settings, screen, stats):
    # show current level
    if stats.game_active:
        level_text = Titletext(ai_settings.bg_color, screen, 'Level: ' + str(stats.level))
        level_text.prep_image()
        level_text.image_rect.centerx = (ai_settings.screen_width // 2)
        level_text.image_rect.centery = (ai_settings.screen_height // 2) - level_text.image_rect.height
        start_time = time.get_ticks()
        while abs(start_time - time.get_ticks()) <= 1500:
            screen.fill(ai_settings.bg_color)
            level_text.blitme()
            display.flip()
