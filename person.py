"""
Персонаж в игре
"""
import pygame
from constants import height, width, boost_time, shield_time, x2_time, Lines_speed
from forest import Forest


class Person:
    """
    Класс персонажа
    """
    def __init__(self, mode='normal', cost=2):
        """
        Класс персонажа
        """
        self.cost = cost

        self.images = [
            [
                pygame.image.load('static/persons/person_' + str(cost) + '/back_1.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/back_2.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/back_3.png')
            ],
            [
                pygame.image.load('static/persons/person_' + str(cost) + '/front_1.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/front_2.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/front_3.png')
            ],
            [
                pygame.image.load('static/persons/person_' + str(cost) + '/left_1.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/left_2.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/left_3.png')
            ],
            [
                pygame.image.load('static/persons/person_' + str(cost) + '/right_1.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/right_2.png'),
                pygame.image.load('static/persons/person_' + str(cost) + '/right_3.png')
            ],
            pygame.image.load('static/persons/person_' + str(cost) + '/right_3.png'),
        ]

        self.current_image = self.images[0][0]

        self.score = 0
        self.rect = self.images[0][0].get_rect()
        self.rect.x = self.rect.width * 3
        self.set_y(mode)
        self.rejim = {
            'boost' : False,
            'shield' : False,
            'x2' : False
        }
        self.boost_time = 5
        self.shield_time = 5
        self.x2_time = 5
        self.image_step = True
        self.last_direction = 1
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.images[0][0]
        self.sprite.rect = self.rect
        self.move_order = []
        self.speed = 14
        self.step_max_time = 182
        self.current_step_time = 0
        self.directions = [
            [0, -1],
            [0, 1],
            [-1, 0],
            [1, 0],
            [0, 0],
        ]
        self.current_line = 1
        self.dead = False

    def set_y(self, mode):
        """
        Задаётся координата по вертикали в зависимости
        от режима игры
        :param mode:
        :return:
        """
        if mode == "normal" or mode == "time":
            self.rect.y = height - self.rect.height * 2
        elif mode == "reverse":
            self.rect.y = self.rect.height

    def add_move_order(self, direction, lines, mode):
        """
        Добавление следующего шага персонажа
        """
        self.move_order.append(direction)
        if self.current_step_time == 0:
            if self.check_borders(direction) \
                    and (self.check_trees_collision(direction, lines, mode)
                         or self.rejim['shield']):
                self.current_step_time = self.step_max_time

    def move(self, lines, mode='normal'):
        """
        Движение первонажа на 1 шаг (равный self.speed)
        :param lines:
        :return:
        """
        gameover = False
        if self.current_step_time > 0:
            self.rect.x += self.directions[self.move_order[0]][0] * self.speed
            self.rect.y += self.directions[self.move_order[0]][1] * self.speed
            self.current_step_time -= self.speed
            gameover = self.check_road_collision(lines) \
                       and not self.rejim['shield'] and not self.rejim['boost']
        if self.current_step_time == 0:
            self.powerup_checker(lines)
            gameover = (self.check_road_collision(lines)
                        or self.check_water_collision(lines)) and not self.rejim['shield'] \
                       and not self.rejim['boost']
            if len(self.move_order) > 0:
                del self.move_order[0]
            if len(self.move_order) > 0:
                while len(self.move_order) > 0:
                    if self.check_borders(self.move_order[0]) \
                            and (self.check_trees_collision(self.move_order[0], lines, mode)
                                 or self.rejim['shield']):
                        self.current_step_time = self.step_max_time
                        break
                    else:
                        del self.move_order[0]
        self.rect.y += Lines_speed.lines_speed
        return gameover or not self.check_borders(4)

    def check_road_collision(self, lines):
        """
        Проверка столкновении персонажа и толпы
        :return:
        """
        if lines[self.current_line].type == 'road':
            self.sprite.rect = self.rect
            for crowd_sprite in lines[self.current_line].to_sprite():
                if pygame.sprite.collide_mask(self.sprite, crowd_sprite) is not None:
                    return True
        return False

    def check_water_collision(self, lines):
        """
        Проверка на коллизию с водой
        :param lines:
        :return:
        """
        if lines[self.current_line].type == 'water':
            x = self.rect.x
            x_cell = x // self.rect.width
            if not x_cell in lines[self.current_line].flowers:
                return True
        return False

    def check_borders(self, direction):
        """
        Проверка столкновения с бортиками
        :param direction:
        :return:
        """
        x = self.rect.x + self.directions[direction][0] * self.step_max_time
        y = self.rect.y + self.directions[direction][1] * self.step_max_time
        if 0 <= x and x + self.rect.width <= width and \
                -self.rect.height <= y <= height + self.rect.height:
            return True
        return False

    def check_trees_collision(self, direction, lines, mode):
        """
        Проверка столкновения персонажа с деревьями
        (через наличие логической координаты персонажа в списке
        деревьев на линии lines[self.current_line].trees
        :param direction: направление, куда собирается пойти персонаж
        :param lines: список линий, отображающихся сейчас на экране
        :param mode: режим игры
        :return:
        """
        x = self.rect.x + self.directions[direction][0] * self.step_max_time
        y = self.rect.y + self.directions[direction][1] * self.step_max_time
        x_cell = x // self.rect.width

        if mode == "reverse":
            if y != self.rect.y:
                if self.current_line - self.directions[direction][1] * (-1) >= len(lines) or \
                        (x_cell in lines[self.current_line -
                                         self.directions[direction][1] * (-1)].trees
                         and not self.rejim['shield']):
                    return False
            if self.current_line >= len(lines) or \
                    (x_cell in lines[self.current_line].trees and not self.rejim['shield']):
                return False
            self.current_line -= self.directions[direction][1] * (-1)
            return True

        if mode == "normal" or mode == "time":
            if y != self.rect.y:
                if self.current_line + \
                        self.directions[direction][1] * (-1) >= len(lines) or \
                        (x_cell in lines[self.current_line +
                                         self.directions[direction][1] * (-1)].trees
                         and not self.rejim['shield']):
                    return False
            elif self.current_line >= len(lines) or \
                    (x_cell in lines[self.current_line].trees and not self.rejim['shield']):
                return False
            self.current_line += self.directions[direction][1] * (-1)
            return True

    def powerup_checker(self, lines):
        """
        Проверка того, находится ли сейчас персонаж на клетке с паверапом
        :param lines: список линий, отображающихся сейчас на экране
        :return:
        """
        if type(lines[self.current_line]) == Forest:
            x_cell = self.rect.x // self.rect.width
            if x_cell in lines[self.current_line].boosts:
                self.boost_time = boost_time
                self.rejim['boost'] = True
            if x_cell in lines[self.current_line].shields:
                self.shield_time = shield_time
                self.rejim['shield'] = True
            if x_cell in lines[self.current_line].x2:
                self.x2_time = x2_time
                self.rejim['x2'] = True

    def draw(self, screen):
        """
        Отрисовка персонажа
        :param screen:
        :return:
        """
        if self.current_step_time > 0:
            self.current_image = self.images[self.move_order[0]][self.image_step + 1]
            screen.blit(self.current_image, self.rect)
            self.last_direction = self.move_order[0]
            if self.current_step_time % 56 == 0:  # число, кратное speed
                self.image_step = not self.image_step
        else:
            self.current_image = self.images[self.last_direction][0]
            screen.blit(self.current_image, self.rect)
