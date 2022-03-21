"""
Заголовок игры
"""
import pygame
from constants import width


class GameName:
    """
    Класс заголовка игры
    """
    def __init__(self):
        self.image = pygame.image.load('static/menu/name.png')
        self.rect = self.image.get_rect()
        self.rect_width, self.rect_height = self.rect.size
        self.rect.x = (width - self.rect_width) // 2
        self.rect.y = 120

    def draw(self, screen):
        """
        Отрисовка заголовка
        """
        screen.blit(self.image, self.rect)
