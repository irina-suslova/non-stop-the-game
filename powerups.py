"""
Модуль с описанием паверапов
"""
import pygame
from PIL import Image


class PowerUp:
    """
    Базовый класс паверапа
    """

    def __init__(self, time_of_boost=100, way_to_image="static/powerups/powerup.png",
                 is_shown=True):
        self.image = Image.open(way_to_image)
        self.is_shown = is_shown
        self.time_of_boost = time_of_boost

    def draw(self, screen):
        """
        Делаем отрисовку модельки
        """
        if self.is_shown:
            screen.blit(self.image, self.rect)

    def hide(self):
        """
        Делаем модельку невидимой
        """
        self.is_shown = False

    def show(self):
        """
        Делаем модельку видимой
        """
        self.is_shown = True

    def to_sprite(self):
        """
        Превращаем моедльку в спрайт
        """
        sprite = pygame.sprite.Sprite()
        sprite.image = self.image
        sprite.rect = self.rect
        return sprite

    def time_check(self):
        """
        Функция проверки времени паверапа
        """
        if self.time_of_boost <= 0:
            self.hide()


class Boost(PowerUp):
    """
    Класс паверапа такого: Буст
    """

    def __init__(self, time_of_boost=100, way_to_image="static/powerups/boost.png",
                 is_shown=True):
        super().__init__(time_of_boost, way_to_image, is_shown)


class DoubleCoins(PowerUp):
    """
    Класс паверапа такого: Двойные очки
    """

    def __init__(self, x=0, y=0, time_of_boost=100, way_to_image="static/powerups/x2.png",
                 is_shown=True):
        super().__init__(time_of_boost, way_to_image, is_shown)


class Shield(PowerUp):
    """
    Класс паверапа такого: Щит
    """

    def __init__(self, time_of_boost=100, way_to_image="static/powerups/shield.png",
                 is_shown=True):
        super().__init__(time_of_boost, way_to_image, is_shown)

    def shield(self):
        """
        Функция создания щита вокруг шишки
        """
        raise NotImplementedError


class TimeAdd(PowerUp):
    """
    Класс паверапа: Дополнительное время
    """

    def __init__(self, time_of_boost=100, way_to_image="static/powerups/time_add.png",
                 is_shown=True):
        super().__init__(time_of_boost, way_to_image, is_shown)