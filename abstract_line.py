"""
Описание одной линии поля
"""
from random import choice
import pygame
from constants import Lines_speed, cell_width, width


class Line:
    """
    Класс линии поля
    """
    def __init__(self, type, trees=[]):
        """
        Инициализация
        :param type: вид полосы
        :param trees: список с логическими координатами деревьев на полосе
        """
        self.type = type
        self.trees = trees
        self.rect = pygame.Rect(0, 0, width, cell_width)
        self.y_shift = Lines_speed.lines_speed  # Скорость движения полос

    def generate_coords(self, items, all_images):
        """
        Перевод логических координат массива items в координаты поля
        и присваивание этим кооринатам изображения
        :param items: логические координаты
        :param all_images: картинки, из которых происходит выбор
        :return: возвращает список координат поля и список изображений
        """
        coords_x = []
        images = []
        for item in items:
            coords_x.append(item * cell_width)
            images.append(choice(all_images))
        return coords_x, images

    def draw(self, screen, image, rect):
        """
        Отрисвока изборажения полосы (только для воды и леса!) + вызов движения
        """
        screen.blit(image, rect)
        self.move()

    def move(self):
        """
        Движение полосы (только для воды и леса!)
        """
        self.rect.y += self.y_shift
