import pygame


class Menu:

    def __init__(self, ai_settings, menu_screen):
        self.ai_settings = ai_settings
        self.menu_screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        self.menu_screen.fill(ai_settings.bg_color)

        self.screen = menu_screen
        self.screen_rect = menu_screen.get_rect()
        self.ai_settings = ai_settings

        # font
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 96)
        self.smaller_font = pygame.font.SysFont(None, 48)

        # space invaders string
        self.first_image = self.font.render("Space", True, self.text_color, self.ai_settings.bg_color)
        self.first_image_rect = self.first_image.get_rect()
        self.first_image_rect.centerx = self.screen_rect.centerx
        self.first_image_rect.top = 100
        self.second_image = self.font.render("Invaders", True, self.text_color, self.ai_settings.bg_color)
        self.second_image_rect = self.second_image.get_rect()
        self.second_image_rect.centerx = self.screen_rect.centerx
        self.second_image_rect.top = 175

        # points: 10, 20, 40, and ?? points
        self.third_image = self.smaller_font.render("= 10 Pts", True, self.text_color, self.ai_settings.bg_color)
        self.third_image_rect = self.second_image.get_rect()
        self.third_image_rect.centerx = self.screen_rect.centerx + 100
        self.third_image_rect.top = 310

        self.fourth_image = self.smaller_font.render("= 20 Pts", True, self.text_color, self.ai_settings.bg_color)
        self.fourth_image_rect = self.second_image.get_rect()
        self.fourth_image_rect.centerx = self.screen_rect.centerx + 100
        self.fourth_image_rect.top = 370

        self.fifth_image = self.smaller_font.render("= 40 Pts", True, self.text_color, self.ai_settings.bg_color)
        self.fifth_image_rect = self.second_image.get_rect()
        self.fifth_image_rect.centerx = self.screen_rect.centerx + 100
        self.fifth_image_rect.top = 430

        self.sixth_image = self.smaller_font.render("= ?? Pts", True, self.text_color, self.ai_settings.bg_color)
        self.sixth_image_rect = self.second_image.get_rect()
        self.sixth_image_rect.centerx = self.screen_rect.centerx + 100
        self.sixth_image_rect.top = 500

        # high scores
        self.hi_score_image = self.smaller_font.render("Invaders", True, (0, 0, 155), self.ai_settings.bg_color)
        self.hi_score_image_rect = self.second_image.get_rect()
        self.hi_score_image_rect.centerx = 1000
        self.hi_score_image_rect.top = 100

        self.alien1 = pygame.image.load('images/simple.png')
        self.alien1 = pygame.transform.scale(self.alien1, (64, 64))
        self.alien2 = pygame.image.load('images/rotate.png')
        self.alien2 = pygame.transform.scale(self.alien2, (64, 64))
        self.alien3 = pygame.image.load('images/expand.png')
        # self.alien3 = pygame.transform.scale(self.alien3, (64, 64))
        self.ufo = pygame.image.load('images/face.png')
        self.ufo = pygame.transform.scale(self.ufo, (64, 64))

    def show_menu(self):
        self.menu_screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        self.menu_screen.fill(self.ai_settings.bg_color)
        self.screen.blit(self.first_image, self.first_image_rect)
        self.screen.blit(self.second_image, self.second_image_rect)
        self.screen.blit(self.third_image, self.third_image_rect)
        self.screen.blit(self.fourth_image, self.fourth_image_rect)
        self.screen.blit(self.fifth_image, self.fifth_image_rect)
        self.screen.blit(self.sixth_image, self.sixth_image_rect)
        self.screen.blit(self.alien1, (500, 300))
        self.screen.blit(self.alien2, (500, 350))
        self.screen.blit(self.alien3, (500, 420))
        self.screen.blit(self.ufo, (500, 490))

    def show_hi_score(self):
        self.screen.blit(self.hi_score_image, self.hi_score_image_rect)

