"""
Меню смерти
"""
import sys
import pygame
from classes import Scull
from background import Background
from constants import size, width, white
from table import scoreboard
from nick import add_nick


def death(screen, score, mode):
    """
    Смерть персонажа
    Вызов черепа
    Конец игры для данных набранных очков
    """

    scull = Scull()
    scull.draw(screen)
    pygame.display.flip()
    pygame.time.wait(1000)
    end = End(score, mode)
    end.main_loop()


class End:
    """
    Класс конца игры
    """
    def __init__(self, score, mode):
        self.screen = pygame.display.set_mode((size), pygame.RESIZABLE)
        self.gameover = False
        self.background = Background()
        self.picture = pygame.image.load('static/menu/nickname.png')
        self.rect = self.picture.get_rect()
        self.rect.x = (width - self.rect.width) // 2
        self.rect.y = 20
        self.nick = ''
        self.elapsed_time = 0
        self.text = pygame.font.SysFont('Century Gothic', 180, False)
        self.score = score
        self.mode = mode
        self.finish = False

    def process_logic(self):
        """
        Ввод ника игрока
        """
        nick1 = self.nick
        cnt = -1
        max_len = 12
        while len(nick1) > 0:
            if len(nick1) > max_len:
                text1 = self.text.render(nick1[0:max_len], 0, white)
                nick1 = nick1[max_len:]
            else:
                text1 = self.text.render(nick1, 0, white)
                nick1 = ''
            cnt += 1
            self.screen.blit(text1, (250, 200 + 125 * cnt))
        self.elapsed_time += 10

    def process_events(self):
        """
        Сохранение ника и очков игрока
        Вывод таблицы рекордов
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    if len(self.nick) == 0:
                        self.nick = 'undefined_nick'
                    self.finish = True
                    add_nick(self.nick, self.score, self.mode)
                    scoreboard(self.background, self.mode)
                    return
                if event.key == 8:
                    if len(self.nick) >= 1:
                        self.nick = self.nick[:len(self.nick) - 1]
                else:
                    self.nick += str(event.unicode)

    def process_draw(self):
        """
        Отрисовка фона
        """
        self.background.draw(self.screen)
        self.screen.blit(self.picture, self.rect)

    def main_loop(self):
        """
        Вызов функции отрисовки
        Вызов функций ввода и сохранения данных игрока
        """
        pygame.init()
        pygame.font.init()
        while not self.gameover:
            self.process_events()
            if self.finish:
                return
            self.process_draw()
            self.process_logic()
            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()
