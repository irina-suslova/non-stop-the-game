"""
Описание одной линии поля
"""
from random import randint
import pygame
from PIL import Image, ImageFile
from constants import Lines_speed
from powerups import Boost, Shield, DoubleCoins
from PIL import ImageFile

from powerups import Boost, Shield, DoubleCoins

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Line:
    """
    Класс линии поля
    """
    test_line = pygame.image.load('static/templates/' + 'tree' + '_1.png')

    def __init__(self, number, trees, type_forest):
        """
        Инициализация
        :param number: число, показывающее цвет полосы, на которой будут расставлены деревья
        :param trees: список с логическими координатами деревьев на полосе
        :param type_forest: показывает тип леса в игре (лес из ёлок или лиственных деревьев)
        """
        self.type = type_forest
        self.number = number
        self.trees = trees
        self.boosts = []
        self.shields = []
        self.x2 = []
        self.line_name = 'static/field/' + str(self.number) + '.png'
        self.image = pygame.image
        self.image_without_powerups = pygame.image
        self.is_power_upped = False
        self.rect = pygame.Rect(0, 0, 1280, 182)
        self.trees_images_names = [
            'static/templates/' + type_forest + '_1.png',
            'static/templates/' + type_forest + '_2.png',
            'static/templates/' + type_forest + '_3.png'
        ]

        self.y_shift = Lines_speed.lines_speed  # Скорость движения полос

    def copy_line(self, line):
        """
        Конструктор копирования
        :param line: объект класса Line, с которого копируются свойства
        :return:
        """
        self.number = line.number
        self.trees = line.trees
        self.image = line.image
        self.image_without_powerups = line.image_without_powerups
        self.boosts = line.boosts
        self.shields = line.shields
        self.x2 = line.x2

    def remove_powerups(self):
        """
        This func removes all the powerup images from the line
        :return:
        """
        self.image = self.image_without_powerups

    def power_up_adding(self, mode):
        """
        This func adds powerups to the line
        :return:
        """
        chance = randint(0, 100)
        if mode == "time":
            kind_of_powerup = randint(1, 4)
        else:
            kind_of_powerup = randint(1, 3)
        probability = 70
        line_im = Image.open(self.line_name)
        if chance <= probability and not self.is_power_upped:
            map_of_free_places = [1, 1, 1, 1, 1, 1, 1]
            for i in range(0, len(self.trees)):
                map_of_free_places[self.trees[i]] = 0
            for i in range(0, len(map_of_free_places)):
                if map_of_free_places[i] == 1:
                    if kind_of_powerup == 1:
                        self.shields.append(i)
                        shield = Shield()
                        line_im.paste(shield.image, (i*182, 0), shield.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break
                    if kind_of_powerup == 2:
                        self.boosts.append(i)
                        boost = Boost()
                        line_im.paste(boost.image, (i * 182, 0), boost.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break
                    if kind_of_powerup == 3:
                        self.x2.append(i)
                        x2 = DoubleCoins()
                        line_im.paste(x2.image, (i * 182, 0), x2.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break
                    if kind_of_powerup == 4:
                        self.time.append(i)
                        time = Time()
                        line_im.paste(time.image, (i * 182, 0), time.image)
                        line_im.save(self.line_name)
                        self.is_power_upped = True
                        break

    def generate(self, mode):
        """
        Расстановка деревьев на полосе в порядке, заданном списком self.trees
        Создание целостной картинки полосы (для улучшения производительности)
        :return:
        """
        rects = []
        images = []
        rects.append(Line.test_line.get_rect())
        images.append(self.trees_images_names[2])
        rects.append(Line.test_line.get_rect())
        images.append(self.trees_images_names[2])
        rects[0].x = rects[0].y = rects[1].y = 0
        rects[1].x = 6 * rects[len(rects) - 1].width

        for tree in self.trees:
            rects.append(Line.test_line.get_rect())
            rects[len(rects) - 1].y = 0
            rects[len(rects) - 1].x = tree * rects[len(rects) - 1].width
            rand = randint(1, 3)
            if rand == 1:
                images.append(self.trees_images_names[0])
            elif rand == 2:
                images.append(self.trees_images_names[1])
            elif rand == 3:
                images.append(self.trees_images_names[2])
        self.trees.append(0)
        self.trees.append(6)

        line_name = self.line_name
        background_name = 'static/templates/' + str(self.number) + '.png'

        line = Image.open(line_name)

        background_line = Image.open(background_name)

        line.paste(background_line, (0, 0))

        for i in range(len(rects)):
            name_image = Image.open(images[i])
            line.paste(name_image, (rects[i].x, 0), name_image)
        line.save(line_name)
        self.image_without_powerups = pygame.image.load(line_name)
        self.power_up_adding(mode)
        self.image = pygame.image.load(line_name)

    def draw(self, screen):
        """
        Функция отрисовки полосу (+ вызов движения)
        :param screen:
        :return:
        """
        screen.blit(self.image, self.rect)
        self.move()

    def move(self):
        """
        Движение полосы
        :return:
        """
        self.rect.y += self.y_shift
