"""
Меню режимов игры
"""
import sys
import pygame
from game import Game
from constants import size, width, height


class Button:
    """
    Класс кнопок меню
    """
    def __init__(self, picture_1, picture_2):
        self.picture_1 = picture_1
        self.picture_2 = picture_2
        self.image_1 = pygame.image.load(picture_1)
        self.image_2 = pygame.image.load(picture_2)
        self.rect = self.image_1.get_rect()
        self.rect_width, self.rect_height = self.rect.size
        self.rect.x = (width - self.rect_width) // 2
        self.rect.y = 0
        self.set_x_y()

    def set_x_y(self):
        """
        Размещение кнопок
        """
        if self.picture_1 == 'static/menu/classic_1.png':
            self.rect.y = (height - self.rect_height) // 4 * 1 - self.rect_height
        elif self.picture_1 == 'static/menu/inversed_1.png':
            self.rect.y = (height - self.rect_height) // 4 * 2 - self.rect_height
        elif self.picture_1 == 'static/menu/ontime_1.png':
            self.rect.y = (height - self.rect_height) // 4 * 3 - self.rect_height
        elif self.picture_1 == "static/menu/back_1.png":
            self.rect.y = 600

    def draw_click(self, screen):
        """
        Отрисовка нажатия
        """
        screen.blit(self.image_2, self.rect)
        pygame.display.flip()
        pygame.time.wait(50)

    def check_click(self, mouse_x, mouse_y, screen, background, cost, volume):
        """
        Проверка на наличие нажатия
        Отрисовка нажатия
        Начало игры в соответствующем режиме
        """
        if self.rect.x <= mouse_x <= self.rect.x + self.rect_width \
                and self.rect.y <= mouse_y <= self.rect.y + self.rect_height:
            if self.picture_1 == 'static/menu/classic_1.png':
                pygame.mixer.music.load('Tokyo_drift.mp3')
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.draw_click(screen)
                game = Game('normal', cost)
                game.main_loop()
                return True
            if self.picture_1 == 'static/menu/inversed_1.png':
                pygame.mixer.music.load('Tokyo_drift.mp3')
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.draw_click(screen)
                game = Game('reverse', cost)
                game.main_loop()
                return True
            if self.picture_1 == 'static/menu/ontime_1.png':
                pygame.mixer.music.load('Tokyo_drift.mp3')
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.draw_click(screen)
                game = Game('time', cost)
                game.main_loop()
                return True
            if self.picture_1 == 'static/menu/back_1.png':
                self.draw_click(screen)
                return True
            return False

    def draw(self, screen):
        """
        Отрисовка меню
        """
        screen.blit(self.image_1, self.rect)

def game_menu(background, cost, volume):
    """
    Запуск кнопок
    Проверка нажатия
    Отрисовка всего
    """
    pygame.font.init()
    pygame.init()
    gameover = False
    clicked = False
    screen = pygame.display.set_mode((size), pygame.RESIZABLE)
    play1 = Button('static/menu/classic_1.png', 'static/menu/classic_2.png')
    play2 = Button('static/menu/inversed_1.png', 'static/menu/inversed_2.png')
    play3 = Button('static/menu/ontime_1.png', 'static/menu/ontime_2.png')
    back_button = Button("static/menu/back_1.png", "static/menu/back_2.png")
    while not gameover:
        if clicked:
            return
        background.draw(screen)
        play1.draw(screen)
        play2.draw(screen)
        play3.draw(screen)
        back_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    clicked = play1.check_click(mouse_x, mouse_y, screen, background, cost, volume)
                    clicked = clicked or play2.check_click(mouse_x, mouse_y, screen,
                                                           background, cost, volume)
                    clicked = clicked or play3.check_click(mouse_x, mouse_y, screen,
                                                           background, cost, volume)
                    clicked = clicked or back_button.check_click(mouse_x, mouse_y, screen,
                                                           background, cost, volume)
        pygame.display.flip()
        pygame.time.wait(10)
    if gameover:
        sys.exit()
    return
