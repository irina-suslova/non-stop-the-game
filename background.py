"""
Фон в меню
"""
import pygame

from constants import width


class Background:
    """
    Класс для создания фона
    """

    def __init__(self):
        self.picture = 'static/menu/background.png'
        self.image = pygame.image.load('static/menu/background.png')
        self.rect_1 = self.image.get_rect()
        self.rect_1_width, self.rect_1_height = self.rect_1.size
        self.rect_1.x = 0
        self.rect_1.y = 0

        self.rect_2 = self.image.get_rect()
        self.rect_2_width, self.rect_2_height = self.rect_2.size
        self.rect_2.x = width
        self.rect_2.y = 0

        self.x_shift = -1

    def draw(self, screen):
        """
        Отрисовка фона + его движение

        :param screen: параметры экрана
        :return:
        """

        screen.blit(self.image, self.rect_1)
        screen.blit(self.image, self.rect_2)
        self.move()

    def move(self):
        """
        Движение фона

        :return:
        """
        self.rect_1.x += self.x_shift
        self.rect_2.x += self.x_shift
        if self.rect_1.x < -width:
            self.rect_1.x = width
        if self.rect_2.x < -width:
            self.rect_2.x = width
