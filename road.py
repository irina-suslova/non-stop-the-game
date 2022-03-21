"""
Описание полосы дороги с толпой
"""
import random
from random import randint, choice
import pygame
from constants import width
from abstract_line import Line


class Road(Line):
    """
    Класс дороги
    """
    crowd_images = [
        [
            pygame.image.load('static/templates/crowd_1.png'),
            pygame.image.load('static/templates/crowd_2.png')
        ],
        [
            pygame.image.load('static/templates/crowd_3.png'),
            pygame.image.load('static/templates/crowd_4.png')
        ],
    ]
    crowd_test_rect = crowd_images[0][0].get_rect()

    def __init__(self):
        """
        Инициализация
        self.time - для изменения картинки отображения толпы раз в 0.2 секунды
        """
        super().__init__('road')
        self.time = 0           # Для изменения картинки отображения толпы раз в 0.2 секунды
        self.image_step = True
        self.number = random.randint(1, 3)
        self.rects = []
        self.x_shift = randint(3, 10) * choice([-1, 1])
        self.generate()

    def generate(self):
        """
        Расстановка толпы на полосе дороги
        """
        for i in range(self.number):
            rect = pygame.Rect(i * (width // self.number), 0, Road.crowd_test_rect.width,
                               Road.crowd_test_rect.height)
            self.rects.append(rect)

    def set_y(self):
        """
        Функция, делающая равными координаты y
        """
        for rect in self.rects:
            rect.y = self.rect.y

    def draw(self, screen):
        """
        Отрисовка полосы + вызов функции движения
        """
        self.time += 10
        if self.x_shift < 0:
            array = 0
        else:
            array = 1
        for rect in self.rects:
            screen.blit(Road.crowd_images[array][self.image_step], rect)
        if self.time % 200 == 0:
            self.image_step = not self.image_step
        self.move()

    def to_sprite(self):
        """
        Получение pygame.Sprite каждого прямоугольника толпы для коллизий с персонажем
        :return:
        """
        sprites = []
        for rect in self.rects:
            sprite = pygame.sprite.Sprite()
            sprite.image = Road.crowd_images[0][0]
            sprite.rect = rect
            sprites.append(sprite)
        return sprites

    def move(self):
        """
        Движение толпы
        """
        super().move()
        for rect in self.rects:
            rect.y += self.y_shift
            rect.x += self.x_shift
            if rect.x >= width or rect.x <= 0 - rect.width:
                if self.x_shift > 0:
                    rect.x = 0 - rect.width
                else:
                    rect.x = width
