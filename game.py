"""
Основные действия игры. Движение линий,бусты, персонаж на поле
"""
import time
import sys
from random import randint, choice
import pygame
from constants import size, road_color, height, Lines_speed, x2_time, shield_time
from person import Person
from lines import get_lines
from weather import weather
from factory import Factory
from pause import Pause, Egg, Egg_2
from death_menu import death
from timer import Timer
from plot import Picture


class Game:
    """
    This is class of the game. Main methods for running are here.
    """
    def __init__(self, mode='normal', cost=2):
        """
        All values initialization
        """
        # screen = pygame.display.set_mode((size), pygame.RESIZABLE)

        # Установка размеров окна
        self.gameover = False
        self.size = 10
        self.boost_rejim = False
        self.type = choice(["fir", "tree"])       # "tree" or "fir"
        self.factory = Factory()
        self.death = False
        self.mode = mode        # 'normal' or 'reverse' or 'time'
        self.all_lines = get_lines(self.size, self.type, self.mode)
        self.lines = []
        self.screen = pygame.display.set_mode((size), pygame.RESIZABLE)
        self.pers = Person(self.mode, cost)
        self.font = pygame.font.Font(None, 40)
        self.sec = time.time()
        self.point_per_sec = 1
        self.shield_params = {
            'way' : 'static/powerups/shield_char.png',
            'image' : pygame.image.load('static/powerups/shield_char.png'),
            'rect' : pygame.image.load('static/powerups/shield_char.png').get_rect()
        }
        self.flag_params = {
            'way': 'static/powerups/flag_char.png',
            'image': pygame.image.load('static/powerups/flag_char.png'),
            'rect': pygame.image.load('static/powerups/flag_char.png').get_rect()
        }
        self.pause = False
        self.egg = False
        self.egg_2 = False
        self.rain = True
        self.rain_pictures = [
            pygame.image.load('static/templates/rain_1.png'),
            pygame.image.load('static/templates/rain_2.png'),
            pygame.image.load('static/templates/rain_3.png'),
        ]
        self.time = 0
        self.timer = Timer()
        self.plot_pict_number = 0
        self.plot = Picture()

    def prepare(self):
        """
        Prepare for game. Initialization.
        :return:
        """

        if self.mode == "normal" or self.mode == "time":
            Lines_speed.lines_speed = abs(Lines_speed.lines_speed)

        elif self.mode == "reverse":
            Lines_speed.lines_speed = -abs(Lines_speed.lines_speed)

        rand = randint(0, self.size - 1)
        test_line = self.factory.create_forest()
        test_line.copy_line(self.all_lines[rand])
        self.lines.append(test_line)

        rand = randint(0, self.size - 1)
        while self.all_lines[rand].number == self.lines[len(self.lines) - 1].number:
            # Чтобы полосы не повторялись друг за другом
            rand = randint(0, self.size - 1)
        test_line = self.factory.create_forest()
        test_line.copy_line(self.all_lines[rand])
        self.lines.append(test_line)

        if self.mode == "normal" or self.mode == "time":
            self.lines[0].rect.y = height - self.lines[0].rect.height
            self.lines[len(self.lines) - 1].rect.y = \
                self.lines[len(self.lines) - 2].rect.y \
                - self.lines[len(self.lines) - 1].rect.height

        elif self.mode == "reverse":
            self.lines[0].rect.y = 0
            self.lines[len(self.lines) - 1].rect.y = \
                self.lines[len(self.lines) - 2].rect.y \
                + self.lines[len(self.lines) - 1].rect.height

        self.rain = weather()

    def main_loop(self):
        """
        All main methods. Game for running.
        :return:
        """
        self.prepare()
        while not self.gameover:  # Основной цикл
            self.process_events()
            self.process_logic()
            if self.death or self.pers.dead:
                return
            self.process_draw()
            self.check_plot_picture()
            pygame.display.flip()  # Double buffering
            pygame.time.wait(10)
        sys.exit()

    def process_events(self):
        """
        Проверка состояний процесса и кнопок
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover = True
            if event.type == pygame.KEYDOWN \
                    and not self.pers.rejim['boost']:
                if event.key == pygame.K_w:
                    self.pers.add_move_order(0, self.lines, self.mode)
                elif event.key == pygame.K_s:
                    self.pers.add_move_order(1, self.lines, self.mode)
                elif event.key == pygame.K_a:
                    self.pers.add_move_order(2, self.lines, self.mode)
                elif event.key == pygame.K_d:
                    self.pers.add_move_order(3, self.lines, self.mode)
                elif event.key == pygame.K_p:
                    self.pause = not self.pause
                elif event.key == pygame.K_f:
                    self.egg = not self.egg
                elif event.key == pygame.K_q:
                    self.egg_2 = not self.egg_2

    def process_logic(self):
        """
        Движение персонажа
        :return:
        """
        if not self.pause and not self.egg and not self.egg_2:
            if not self.pers.rejim['boost']:
                self.death = self.pers.move(self.lines, self.mode) or not self.timer.not_dead_yet(self.pers)

            if self.death or self.pers.dead:
                pygame.time.wait(700)
                death(self.screen, self.pers.score, self.mode)

    def check_plot_picture(self):
        if self.pers.score >= 0 and self.plot_pict_number == 0:
            self.plot_pict_number += 1
            self.plot.main_loop(self.screen)
        elif self.pers.score >= 20 and self.plot_pict_number == 1:
            self.plot_pict_number += 1
            self.plot.main_loop(self.screen)
        elif self.pers.score >= 100 and self.plot_pict_number == 2:
            self.plot_pict_number += 1
            self.plot.main_loop(self.screen)
        elif self.pers.score >= 200 and self.plot_pict_number == 3:
            self.plot_pict_number += 1
            self.plot.main_loop(self.screen)

    def boost_abuse(self):
        """
        Применение буста если он активирован
        :return:
        """
        if self.pers.boost_time == 0:
            self.pers.boost_time -= 1
            self.pers.rejim['boost'] = False
            self.boost_rejim = False
            for line in self.lines:
                line.y_shift = Lines_speed.lines_speed
            self.pers.rejim['shield'] = True
            self.pers.shield_time = shield_time
        if self.pers.rejim['boost']:
            self.pers.boost_time -= 1
            self.pers.score += 1

            self.flag_params['rect'].x = self.pers.rect.x
            self.flag_params['rect'].y = self.pers.rect.y
            if self.mode != 'reverse':
                self.pers.current_image = self.pers.images[0][0]
                self.screen.blit(self.pers.current_image, self.pers.rect)
                self.screen.blit(self.flag_params['image'], self.flag_params['rect'])
            else:
                self.pers.current_image = self.pers.images[1][0]
                self.screen.blit(self.flag_params['image'], self.flag_params['rect'])
                self.screen.blit(self.pers.current_image, self.pers.rect)
            if not self.boost_rejim:
                self.boost_rejim = True
                for line in self.lines:
                    if self.mode == 'normal' or self.mode == 'time':
                        line.y_shift = Lines_speed.boost_speed
                    else:
                        line.y_shift = -Lines_speed.boost_speed

    def shield_abuse(self):
        """
        Применение щита если он активирован
        :return:
        """
        if self.pers.shield_time <= 0:
            self.pers.rejim['shield'] = False
        if self.pers.rejim['shield']:
            self.pers.shield_time -= 1
            self.shield_params['rect'].x = self.pers.rect.x
            self.shield_params['rect'].y = self.pers.rect.y
            self.screen.blit(self.shield_params['image'], self.shield_params['rect'])

    def x2_abuse(self):
        """
        Применение удвоения очков если оно активировано
        :return:
        """
        if self.pers.x2_time <= 0:
            self.pers.rejim['x2'] = False
            self.point_per_sec = 1
        if self.pers.rejim['x2']:
            self.pers.x2_time -= 1
            self.point_per_sec = 2

    def powerup_abuse(self):
        """
        Общая функция применения всех паверапов на каждом шагу
        :return:
        """
        self.boost_abuse()
        self.shield_abuse()
        self.x2_abuse()

    def powerup_collision(self):
        """
        Проверка коллизии моделей паверапов и модели персонажа
        :return:
        """

        cur_line = self.lines[self.pers.current_line]
        if cur_line.type == 'forest':
            if len(cur_line.boosts) > 0:
                image = pygame.image.load('static/powerups/boost.png')
                rect = image.get_rect()
                rect.y = cur_line.rect.y
                rect.x = cur_line.boosts[0] * 182
                sprite1 = pygame.sprite.Sprite()
                sprite1.image = image
                sprite1.rect = rect
                if pygame.sprite.collide_mask(self.pers.sprite,
                                              sprite1) is not None:
                    cur_line.remove_powerups()

            if len(cur_line.shields) > 0:
                image = pygame.image.load('static/powerups/shield.png')
                rect = image.get_rect()
                rect.y = cur_line.rect.y
                rect.x = cur_line.shields[0] * 182
                sprite1 = pygame.sprite.Sprite()
                sprite1.image = image
                sprite1.rect = rect
                if pygame.sprite.collide_mask(self.pers.sprite,
                                              sprite1) is not None:
                    cur_line.remove_powerups()
                    self.pers.rejim['shield'] = True
                    self.pers.shield_time = shield_time
            if len(cur_line.x2) > 0:
                image = pygame.image.load('static/powerups/x2.png')
                rect = image.get_rect()
                rect.y = cur_line.rect.y
                rect.x = cur_line.x2[0] * 182
                sprite1 = pygame.sprite.Sprite()
                sprite1.image = image
                sprite1.rect = rect
                if pygame.sprite.collide_mask(self.pers.sprite,
                                              sprite1) is not None:
                    cur_line.remove_powerups()
                    self.pers.x2_time = x2_time
            if len(cur_line.time_add) > 0:
                image = pygame.image.load('static/powerups/time_add.png')
                rect = image.get_rect()
                rect.y = cur_line.rect.y
                rect.x = cur_line.time_add[0] * 182
                sprite1 = pygame.sprite.Sprite()
                sprite1.image = image
                sprite1.rect = rect
                if pygame.sprite.collide_mask(self.pers.sprite,
                                                sprite1) is not None:
                    cur_line.remove_powerups()
                    self.timer.value += 10

    def process_draw(self):

        """
        This func draw lines for background
        :return:
        """

        if self.pause:
            Pause.pause_text.draw(self.screen)
            Pause.pause_sign.draw(self.screen)
            pygame.display.flip()
            return

        if self.egg:
            self.screen.blit(Egg.egg, Egg.coords)
            pygame.display.flip()
            return

        if self.egg_2:
            self.screen.blit(Egg_2.egg, Egg_2.coords)
            pygame.display.flip()
            return

        self.screen.fill(road_color)
        for line in self.lines:
            line.draw(self.screen)

        if self.mode == "normal" or self.mode == "time":
            if self.lines[len(self.lines) - 1].rect.y >= 0:
                if randint(1, 3) == 2:
                    self.lines.append(self.factory.create_road())
                    if self.pers.rejim['boost']:
                        self.lines[len(self.lines) - 1].y_shift = Lines_speed.boost_speed
                    self.lines[len(self.lines) - 1].rect.y = \
                             self.lines[len(self.lines) - 2].rect.y \
                             - self.lines[len(self.lines) - 1].rect.height
                    self.lines[len(self.lines) - 1].set_y()
                else:
                    if randint(1, 3) == 2:
                        self.lines.append(self.factory.create_water())
                        if self.pers.rejim['boost']:
                            self.lines[len(self.lines) - 1].y_shift = Lines_speed.boost_speed
                        self.lines[len(self.lines) - 1].rect.y = \
                            self.lines[len(self.lines) - 2].rect.y - \
                            self.lines[len(self.lines) - 1].rect.height
                    else:
                        rand = randint(0, self.size - 1)
                        while self.all_lines[rand].number == \
                                self.lines[len(self.lines) - 1].number:  # Чтобы полосы не повторялись друго за другом
                            rand = randint(0, self.size - 1)

                        test_line = self.factory.create_forest()
                        test_line.copy_line(self.all_lines[rand])
                        if self.pers.rejim['boost']:
                            test_line.y_shift = Lines_speed.boost_speed
                        self.lines.append(test_line)
                        self.lines[len(self.lines) - 1].rect.y = \
                            self.lines[len(self.lines) - 2].rect.y - \
                            self.lines[len(self.lines) - 1].rect.height

            if self.lines[0].rect.y >= height:
                del self.lines[0]
                if not self.pers.rejim['boost']:
                    self.pers.current_line -= 1

        elif self.mode == "reverse":
            if self.lines[len(self.lines) - 1].rect.y <= height:
                if randint(1, 3) == 2:
                    self.lines.append(self.factory.create_road())
                    if self.pers.rejim['boost']:
                        self.lines[len(self.lines) - 1].y_shift = -Lines_speed.boost_speed
                    self.lines[len(self.lines) - 1].rect.y = \
                        self.lines[len(self.lines) - 2].rect.y + \
                        self.lines[len(self.lines) - 1].rect.height
                    self.lines[len(self.lines) - 1].set_y()
                else:
                    if randint(1, 3) == 2:
                        self.lines.append(self.factory.create_water())
                        if self.pers.rejim['boost']:
                            self.lines[len(self.lines) - 1].y_shift = -Lines_speed.boost_speed
                        self.lines[len(self.lines) - 1].rect.y = \
                            self.lines[len(self.lines) - 2].rect.y + \
                            self.lines[len(self.lines) - 1].rect.height
                    else:
                        rand = randint(0, self.size - 1)
                        while self.all_lines[rand].number == \
                                self.lines[len(self.lines) - 1].number:
                            # Чтобы полосы не повторялись друго за другом
                            rand = randint(0, self.size - 1)

                        test_line = self.factory.create_forest()
                        test_line.copy_line(self.all_lines[rand])
                        if self.pers.rejim['boost']:
                            test_line.y_shift = -Lines_speed.boost_speed
                        self.lines.append(test_line)
                        self.lines[len(self.lines) - 1].rect.y = \
                            self.lines[len(self.lines) - 2].rect.y + \
                            self.lines[len(self.lines) - 1].rect.height

            if self.lines[0].rect.y <= 0 - self.lines[0].rect.height:
                del self.lines[0]
                if not self.pers.rejim['boost']:
                    self.pers.current_line -= 1
        self.powerup_collision()
        if not self.pers.rejim['boost']:
            self.pers.draw(self.screen)
        self.powerup_abuse()
        if int(time.time() - self.sec) >= 1:
            self.pers.score += self.point_per_sec
            self.sec = time.time()

        if self.rain == True:
            self.time += 10
            if self.time > 20:
                self.time = 0
            self.screen.blit(self.rain_pictures[self.time // 10], pygame.Rect(0, 0, 1280, 800))
        text = self.font.render("Score: "
                                + str(self.pers.score), True, (0, 0, 0))
        self.screen.blit(text, [1100, 20])
        if self.mode == "time":
            self.timer.draw(self.screen, self.pers)
