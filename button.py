"""
Описание кнопок в главном меню
"""
import pygame
from constants import width, height
from options_menu import options_main_loop, options_prepare
from game_menu import game_menu
from table import scoreboard
from outfit import outfit_loop, outfit_prepare


class Button:
    """
        Кнопка для меню
        """
    game_cost = 0
    def __init__(self, picture_1, picture_2):
        self.picture_1 = picture_1
        self.picture_2 = picture_2
        self.image_1 = pygame.image.load(picture_1)
        self.image_2 = pygame.image.load(picture_2)
        self.rect = self.image_1.get_rect()
        self.rect_width, self.rect_height = self.rect.size
        self.rect.x = (width - self.rect_width) // 2
        self.rect.y = 0
        self.set_y()

    def set_y(self):
        """
        Размещение картинки с кнопкой в зависимости от её вида
        """
        if self.picture_1 == 'static/menu/exit_1.png':
            self.rect.y = height - 4 * (self.rect_height + 5) + 40 + 2 * (self.rect_height + 20)
        elif self.picture_1 == 'static/menu/highscores_1.png':
            self.rect.y = height - 4 * (self.rect_height + 5) + 40 + self.rect_height + 20
        elif self.picture_1 == 'static/menu/play_1.png':
            self.rect.y = height - 4 * (self.rect_height + 5) + 40
        elif self.picture_1 == 'static/menu/settings_1.png':
            self.rect.y = height - self.rect_height - 20
            self.rect.x = width - self.rect_width - 20
        elif self.picture_1 == 'static/menu/outfits_1.png':
            self.rect.x = 20
            self.rect.y = height - self.rect_height - 20

    def draw_click(self, screen):
        """
        Отрисовка фона
        """
        screen.blit(self.image_2, self.rect)
        pygame.display.flip()
        pygame.time.wait(50)

    def check_click(self, mouse_x, mouse_y, background, screen):
        """
        Проверка нажатия на кнопку. Определяет какая именно кнопка нажата.
        Действия соответствующие кнопкам
        """
        if self.rect.x <= mouse_x <= self.rect.x + self.rect_width \
                and self.rect.y <= mouse_y <= self.rect.y + self.rect_height:
            if self.picture_1 == 'static/menu/exit_1.png':
                self.draw_click(screen)
                return True  # Завершить gameover
            elif self.picture_1 == 'static/menu/highscores_1.png':
                self.draw_click(screen)
                scoreboard(background, 'normal')
            elif self.picture_1 == 'static/menu/play_1.png':
                self.draw_click(screen)
                volume = open('volume.txt', 'r')
                v = int(volume.read()) / 100
                volume.close()
                game_menu(background, Button.game_cost, v)
            elif self.picture_1 == 'static/menu/settings_1.png':
                self.draw_click(screen)
                slider, gameover, back_button, mute_button = options_prepare()
                volume = open('volume.txt', 'w')
                v = options_main_loop(slider, gameover, background, screen, back_button, mute_button)
                volume.write(str(v))
                volume.close()
            elif self.picture_1 == 'static/menu/outfits_1.png':
                self.draw_click(screen)  # Выбор костюма
                outfit, gameover, left, right, vib = outfit_prepare()
                Button.game_cost = outfit_loop(outfit, gameover, left,
                                               right, vib, background, screen)
                # В переменную cost отдается номер выбранного костюма
            return False

    def draw(self, screen):
        """
        Отрисовка фона (продвижение картинки)
        """
        screen.blit(self.image_1, self.rect)
