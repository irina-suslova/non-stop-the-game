"""
Костюмы персонажа/разные персонажи
"""
# import sys
import pygame
# from background import Background
from constants import size, width, height


class Outfit():
    """
    Класс костюма персонажа
    """
    class ButtonLR():
        """
        Класс кнопок для пролистывания
        """
        def __init__(self, picture_1, picture_2):
            # type: (object, object) -> object
            self.picture_1 = picture_1
            self.picture_2 = picture_2
            self.image_1 = pygame.image.load(picture_1)
            self.image_2 = pygame.image.load(picture_2)
            self.rect = self.image_1.get_rect()
            self.rect_width, self.rect_height = self.rect.size
            self.rect.x = (width - self.rect_width) // 2
            self.rect.y = 0

        def set_y(self):
            """
            Размещение кнопок перелистывания и кнопки выбора
            """
            if self.picture_1 == 'static/menu/right_1.png':
                self.rect.x = 780
                self.rect.y = 300
            elif self.picture_1 == 'static/menu/left_1.png':
                self.rect.x = 300
                self.rect.y = 300
            elif self.picture_1 == 'static/menu/vib_1.png':
                self.rect.x = 366
                self.rect.y = 600

        def draw_click(self, background, screen):
            """
            Отриосвка нажатия
            """
            screen.blit(self.image_2, self.rect)
            pygame.display.flip()
            pygame.time.wait(50)

        def check_click(self, outfit, mouse_x, mouse_y, background, screen):
            """
            Проверка нажатия
            """
            if self.rect.x <= mouse_x <= self.rect.x + self.rect_width \
                    and self.rect.y <= mouse_y <= self.rect.y + self.rect_height:
                if self.picture_1 == 'static/menu/right_1.png':
                    self.draw_click(background, screen)
                    up_pers(outfit)
                elif self.picture_1 == 'static/menu/left_1.png':
                    self.draw_click(background, screen)
                    down_pers(outfit)
                elif self.picture_1 == 'static/menu/vib_1.png':
                    self.draw_click(background, screen)
                    return True

        def draw(self, screen):
            """
            Отриосвка
            """
            screen.blit(self.image_1, self.rect)

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = self.width = width
        self.height = height
        self.font = pygame.font.SysFont("monospace", 15)
        self.pers = 0
        self.num_pers = 5
        self.persy = [pygame.image.load('static/persons/person_0/front_big.png'),
                      pygame.image.load('static/persons/person_1/front_big.png'),
                      pygame.image.load('static/persons/person_2/front_big.png'),
                      pygame.image.load('static/persons/person_3/front_big.png'),
                      pygame.image.load('static/persons/person_4/front_big.png')]


    def draw(self, screen):
        """
        Отрисовка кнопок
        """
        screen.blit((self.persy[self.pers]), (450, 230))
        screen.blit(pygame.image.load('static/menu/right_1.png'), (780, 300))
        screen.blit(pygame.image.load('static/menu/left_1.png'), (300, 300))
        screen.blit(pygame.image.load('static/menu/vib_1.png'), (366, 600))


def outfit_prepare():
    """
    Подготовка к выбору костюма
    Правая и левая кнопка и текущий костюм на выбор
    """
    outfit = Outfit((size[0] - 500) // 2, (size[1] - 40) // 2, 500, 40)
    left = outfit.ButtonLR('static/menu/left_1.png', 'static/menu/left_2.png')
    right = outfit.ButtonLR('static/menu/right_1.png', 'static/menu/right_2.png')
    vib = outfit.ButtonLR('static/menu/vib_1.png', 'static/menu/vib_2.png')
    left.set_y()
    right.set_y()
    vib.set_y()
    gameover = False
    return outfit, gameover, left, right, vib


def outfit_loop(outfit, gameover, left, right, vib, background, screen):
    """
    Запуск процессов для выбора костюма
    Функция отрисовки
    """
    while not gameover:
        gameover = process_events(outfit, left, right, vib, gameover, background, screen)
        process_draw(outfit, background, screen)
        pygame.time.wait(10)
    return outfit.pers


def up_pers(outfit):
    """
    Следующий костюм
    """
    outfit.pers = (outfit.pers + 1) % outfit.num_pers


def down_pers(outfit):
    """
    Предыдущий костюм
    """
    outfit.pers = (outfit.pers - 1 + outfit.num_pers) % outfit.num_pers


def fun_vib():
    """
    Выбор
    """
    return


def process_draw(outfit, background, screen):
    """
    Отрисовка фона и костюмов
    """
    background.draw(screen)
    outfit.draw(screen)
    pygame.display.flip()


def process_events(outfit, left, right, vib, gameover, background, screen):
    """
    Проверка нажатия
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                gameover = right.check_click(outfit, mouse_x, mouse_y, background, screen) or \
                           left.check_click(outfit, mouse_x, mouse_y, background, screen) or \
                           vib.check_click(outfit, mouse_x, mouse_y, background, screen)
    return gameover
