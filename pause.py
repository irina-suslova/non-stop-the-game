"""
Пауза в игре и пасхалки
"""
import pygame
from text import Text


class Pause:
    """
    Класс паузы
    """
    pygame.font.init()
    pause_text = Text(435, 320, 'P A U S E', 'Cenwtury Gothic', 130, (147, 221, 234), False)
    pause_sign = Text(595, 430, '| |', 'Cenwtury Gothic', 130, (147, 221, 234), True)


class Egg:
    """
    Класс пасхалки
    """
    egg = pygame.image.load('static/menu/f.png')
    coords = (340, 100)


class Egg_2:
    """
    Класс пасхалки (2)
    """
    egg = pygame.image.load('static/menu/q.png')
    coords = (240, 50)