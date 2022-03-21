"""
Просто текст
"""
from random import randint
import pygame
from constants import width, height, black


class Text:
    """
    Класс текста
    """
    def __init__(self, x, y, text='Hello, Pygame!',
                 font="Comic Sans MS", size=95, color=black, bold=True, italic=False):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic
        self.font_object = pygame.font.SysFont(self.font, self.size, self.bold, self.italic)
        self.text_surface = self.font_object.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.speed = [randint(0, 1) * 2 - 1, randint(0, 1) * 2 - 1]

    def shift(self):
        """
        Передвижение текста
        :return:
        """
        self.x += self.speed[0]
        self.y += self.speed[1]
        if self.x < 0 or self.x + self.rect.width > width:
            self.speed[0] *= -1
        if self.y < 0 or self.y + self.rect.height > height:
            self.speed[1] *= -1

    def draw(self, screen):
        """
        Отрисовка
        :param screen:
        :return:
        """
        screen.blit(self.text_surface, (int(self.x), int(self.y)))
