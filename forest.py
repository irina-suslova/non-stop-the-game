"""
Описание полосы леса
"""
from random import randint
import pygame
from PIL import Image, ImageFile
from powerups import Boost, Shield, DoubleCoins, TimeAdd
from abstract_line import Line
from constants import cell_width
ImageFile.LOAD_TRUNCATED_IMAGES = True

class Forest(Line):
    """
    Класс линии леса
    """
    def __init__(self, number, trees, type_forest, index=0):
        """
        Инициализация
        :param number: вид (цвет) полосы леса
        :param trees: список с логическими координатами деревьев на полосе
        :param type_forest: вид леса - 'fir' (хвойный лес) или 'tree' (лиственный лес)
        :param index: уникальный номер для каждого шаблона полосы, используется для картинки полосы
        """
        super().__init__('forest', trees)
        self.type_forest = type_forest
        self.number = number
        self.boosts = []
        self.shields = []
        self.x2 = []
        self.time_add = []
        self.line_name = 'static/field/' + str(index) + '.png'
        self.image = pygame.image
        self.image_without_powerups = pygame.image
        self.is_power_upped = False
        self.trees_images_names = [
            'static/templates/' + type_forest + '_1.png',
            'static/templates/' + type_forest + '_2.png',
            'static/templates/' + type_forest + '_3.png'
        ]

    def copy_line(self, line):
        """
        Конструктор копирования
        :param line: полоса, с которой происходит копирование self
        :return:
        """
        self.number = line.number
        self.trees = line.trees
        self.image = line.image
        self.image_without_powerups = line.image_without_powerups
        self.boosts = line.boosts
        self.shields = line.shields
        self.x2 = line.x2
        self.time_add = line.time_add

    def remove_powerups(self):
        """
        С персонажа исчезает изображение бонуса
        Выход из режим паверапа
        :return:
        """
        self.image = self.image_without_powerups
        self.time_add = []

    def power_up_adding(self, mode):
        """
        Генерация паверапов на линии поля
        :return:
        """
        chance = randint(0, 100)
        if mode == "time":
            kind_of_powerup = randint(1, 4)
        else:
            kind_of_powerup = randint(1, 3)
        probability = 100
        line_im = Image.open(self.line_name)
        if chance <= probability and not self.is_power_upped:
            map_of_free_places = [1, 1, 1, 1, 1, 1, 1]
            for i in range(0, len(self.trees)):
                map_of_free_places[self.trees[i]] = 0
            for i in range(len(map_of_free_places) - 1, 0, -1):
                if map_of_free_places[i] == 1:
                    if kind_of_powerup == 1:
                        self.shields.append(i)
                        shield = Shield()
                        line_im.paste(shield.image, (i * cell_width, 0), shield.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break
                    if kind_of_powerup == 2:
                        self.boosts.append(i)
                        boost = Boost()
                        line_im.paste(boost.image, (i * cell_width, 0), boost.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break
                    if kind_of_powerup == 3:
                        self.x2.append(i)
                        x2 = DoubleCoins()
                        line_im.paste(x2.image, (i * cell_width, 0), x2.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break
                    if kind_of_powerup == 4:
                        self.time_add.append(i)
                        time = TimeAdd()
                        line_im.paste(time.image, (i * cell_width, 0), time.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break

    def generate(self, mode):
        """
        Создание единой картинки полосы по координатам self.trees
        """
        coords_x, images = super().generate_coords(self.trees, self.trees_images_names)

        line_name = self.line_name
        background_name = 'static/templates/' + str(self.number) + '.png'
        line = Image.open(line_name)
        background_line = Image.open(background_name)
        line.paste(background_line, (0, 0))

        for i in range(len(coords_x)):
            name_image = Image.open(images[i])
            line.paste(name_image, (coords_x[i], 0), name_image)
        line.save(line_name)
        self.image_without_powerups = pygame.image.load(line_name)
        self.power_up_adding(mode)
        self.image = pygame.image.load(line_name)

    def draw(self, screen):
        """
        Отрисовка полосы (вызов отрисовки родительского класса)
        """
        super().draw(screen, self.image, self.rect)
