import pygame.ftfont


class Button():

    def __init__(self, ai_settings, screen, msg):
        # initialize button
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set the dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.top = 600

        self.rect2 = pygame.Rect(0, 0, self.width + 100, self.height)
        self.rect2.center = self.screen_rect.center
        self.rect2.top = 700

        # the button message needs to be prepped only once
        self.prep_msg(msg)
        self.prep_score_msg(msg)

    def prep_msg(self, msg):
        # turn msg into a rendered image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.msg_image_rect.top = 608

    def prep_score_msg(self, msg):
        self.msg_image2 = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect2 = self.msg_image2.get_rect()
        self.msg_image_rect2.center = self.rect2.center
        self.msg_image_rect2.top = 708

    def draw_button(self):
        # draw blank button then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_button2(self):
        self.screen.fill(self.button_color, self.rect2)
        self.screen.blit(self.msg_image2, self.msg_image_rect2)

    def check_button(self, mouse_x, mouse_y):
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    """def alter_text_color(self, mouse_x, mouse_y):
        if self.check_button(mouse_x, mouse_y):
            self.prep_msg(self.alt_color)
        else:
            self.prep_msg(self.text_color)"""

