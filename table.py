"""
Таблица рекордов
"""
import sys
import os
import pygame
from constants import size, width, height, white


try:
    if os.environ['CI_BUILD_STAGE'] == 'test':
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
except KeyError:
    pass

screen = pygame.display.set_mode((size), pygame.RESIZABLE)




class Button():
    """
    Кнопка выхода
    """
    def __init__(self, picture_1, picture_2):
        self.picture_1 = picture_1
        self.picture_2 = picture_2
        self.image_1 = pygame.image.load(picture_1)
        self.image_2 = pygame.image.load(picture_2)
        self.rect = self.image_1.get_rect()
        self.rect_width, self.rect_height = self.rect.size
        self.rect.x = (width - self.rect_width) // 2
        self.rect.x = 430
        self.rect.y = 0
        self.set_x_y()

    def draw_click(self, screen):
        """
        Отрисовка нажатия (фона)
        """
        screen.blit(self.image_2, self.rect)
        pygame.display.flip()
        pygame.time.wait(50)

    def set_x_y(self):
        """
        Размещение таблицы и кнопки выхода
        """
        if self.picture_1 == 'static/menu/back_1.png':
            self.rect.x = (width - self.rect_width) // 2
            self.rect.y = height - 20 - self.rect_height
        elif self.picture_1 == 'static/menu/highscores_1.png':
            self.rect.x = 520
        elif self.picture_1 == 'static/menu/right_1.png':
            self.rect.x = 980
            self.rect.y = 300
        elif self.picture_1 == 'static/menu/left_1.png':
            self.rect.x = 100
            self.rect.y = 300

    def check_click(self, back, mouse_x, mouse_y, background, screen, mode):
        """
        Проверка нажатия на кнопку
        """
        if self.rect.x <= mouse_x <= self.rect.x + self.rect_width \
                and self.rect.y <= mouse_y <= self.rect.y + self.rect_height:
            if self.picture_1 == 'static/menu/right_1.png':
                self.draw_click(screen)
                if mode == 'normal':
                    mode = 'reverse'
                elif mode == 'reverse':
                    mode = 'time'
                else:
                    mode = 'normal'
                scoreboard(background, mode)
                return True
            if self.picture_1 == 'static/menu/left_1.png':
                self.draw_click(screen)
                if mode == 'normal':
                    mode = 'time'
                elif mode == 'reverse':
                    mode = 'normal'
                else:
                    mode = 'reverse'
                scoreboard(background, mode)
                return True
            if self.picture_1 == 'static/menu//back_1.png':
                self.draw_click(screen)
            return True

    def draw(self):
        """
        Отрисовка
        """
        screen.blit(self.image_1, self.rect)


def read_from_file(mode):
    """
    Получение данных из таблицы рекордов
    """
    if mode == 'normal':
        file = open('highscores.txt', 'r')
    elif mode == 'reverse':
        file = open('highscores_inversed.txt', 'r')
    else:
        file = open('highscores_on_time.txt', 'r')
    nicks = []
    scores = []
    for line in file:
        nick, score = map(str, line.split())
        score = int(score)
        nicks.append(nick)
        scores.append(score)
    file.close()

    highscores = [nicks, scores]
    return highscores


def scoreboard(background, mode):
    """
    Запуск таблицы рекордов
    Кнопка выхода
    Отрисовка таблицы
    Проверка нажатий
    """
    pygame.font.init()
    pygame.init()
    data = read_from_file(mode)

    back = Button('static/menu/back_1.png', 'static/menu/back_2.png')
    left = Button('static/menu/left_1.png', 'static/menu/left_2.png')
    right = Button('static/menu/right_1.png', 'static/menu/right_2.png')
    text = pygame.font.SysFont('Comic Sans MS', 70, False)
    gameover = False

    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    gameover = right.check_click(back, mouse_x, mouse_y, background,
                                                 screen, mode) or \
                               left.check_click(back, mouse_x, mouse_y, background,
                                                screen, mode) or \
                               back.check_click(back, mouse_x, mouse_y, background,
                                                screen, mode)
                    if gameover:
                        return

        background.draw(screen)

        if mode == 'normal':
            background_table_name = 'static/menu/table_cl.png'
        elif mode == 'reverse':
            background_table_name = 'static/menu/table_inv.png'
        else:
            background_table_name = 'static/menu/table_time.png'
        background_table = pygame.image.load(background_table_name)
        background_table_rect = background_table.get_rect()
        screen.blit(background_table, ((width - background_table_rect.width) // 2, 20))

        t = 0
        for i in range(len(data[0])):
            text1 = text.render(str(i + 1) + ") " + data[0][i] + " " + str(data[1][i]), 0, white)
            screen.blit(text1, (520, 114 + t))
            t += 42

        back.draw()
        left.draw()
        right.draw()

        pygame.display.flip()
        pygame.time.wait(10)

    if gameover:
        sys.exit()
