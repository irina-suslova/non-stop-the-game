"""
Смерть персонажа
"""
import pygame
from constants import width, black
from text import Text


class Scull:
    """
    Класс черепа
    """
    def __init__(self):
        self.image = pygame.image.load('static/menu/scull.png')
        self.image = pygame.transform.scale(self.image, (350, 275))
        self.rect = self.image.get_rect()
        self.rect_width, self.rect_height = self.rect.size
        self.rect.x = (width - self.rect_width) // 2
        self.rect.y = 25
        self.text = Text(300, 320, 'Game Over', 'Cenwtury Gothic', 180, black, False)

    def draw(self, screen):
        """
        Отрисовка черепа
        """
        screen.blit(self.image, self.rect)
        self.text.draw(screen)
