"""
Изменение громкости звука
"""
import pygame
import sys

from constants import size, height, width
from game_menu import Button


class Slider:
    """
    Класс для регулирования громкости
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = self.width = width
        self.height = height
        self.field = pygame.Rect(x, y, width, height)  # Сам ползунок
        self.occupancy = pygame.Rect(x, y, width // 2, height)
        # Заполненность ползунка, изначально на середине
        self.picture = pygame.image.load('static/menu/volume.png')
        self.rect = self.picture.get_rect()
        self.rect.x = (1280 - self.rect.width) // 2
        self.rect.y = (600 - self.rect.height) // 3

    def logic(self):
        """
        Возвращает процент нужной громкости от максимальной
        :return:
        """
        return int((self.occupancy.width / self.field.width) * 100)

    def check_click(self, mouse_x, mouse_y):
        """ Отладка

        print(self.x)
        print(self.y)
        print(mouse_x)
        print(mouse_y)
        """
        if self.x <= mouse_x <= self.x + self.width \
                and self.y <= mouse_y + 120 <= self.y + self.height:
            self.occupancy.width = mouse_x - self.x
            # Ползунок следует за курсором
            return False

    def draw(self, screen):
        """
        Отрисовка
        """
        pygame.draw.rect(screen, pygame.Color(238, 232, 170), self.field)
        if self.logic() > 0:
            pygame.draw.rect(screen, pygame.Color(255, 165, 0), self.occupancy)
        screen.blit(self.picture, self.rect)

    def check_scroll(self, mouse_x, mouse_y, up_direction):
        """
        Проверка на возможность и само скольжение
        :param mouse_x:
        :param mouse_y:
        :param up_direction:
        :return:
        """
        if self.x <= mouse_x <= self.x + self.width \
                and self.y <= mouse_y + 120 <= self.y + self.height \
                and up_direction:
            self.occupancy.width += 5
            # Ползунок увеличивает значение равномерно с прокруткой
            if self.occupancy.width > self.field.width:
                self.occupancy.width = self.field.width
            return False
        if self.x <= mouse_x <= self.x + self.width \
                and self.y <= mouse_y + 120 <= self.y + self.height \
                and not up_direction:
            self.occupancy.width -= 5
            if self.occupancy.width < 0:
                self.occupancy.width = 0
            return False


def options_prepare():
    """
    Slider creation
    :return:
    """
    slider = Slider((size[0] - 500) // 2, (size[1] - 40) // 2, 500, 40)
    back_button = Button("static/menu/back_1.png", "static/menu/back_2.png")
    back_button.rect.y = 600
    mute_button = Button("static/menu/mute_1.png", "static/menu/mute_2.png")  # Надо, чтоб эффект тоже был
    mute_button.rect.y = (height - mute_button.rect.height) // 2
    mute_button.rect.x = (width - slider.field.width - mute_button.rect.width) // 2 - 90  # Ухх, magic numbers!1 <3
    gameover = False
    return slider, gameover, back_button, mute_button


def options_main_loop(slider, gameover, background, screen, back_button, mute_button):
    """
    Main actions
    :param slider:
    :param gameover:
    :param background:
    :param screen:
    :return:
    """
    while not gameover:
        gameover = process_events(slider, gameover, back_button, screen, mute_button)
        process_draw(slider, background, screen, back_button, mute_button)
        pygame.time.wait(10)
    return slider.logic()


def process_draw(slider, background, screen, back_button, mute_button):
    """
    Отрисовка
    :param slider:
    :param background:
    :param screen:
    :return:
    """
    background.draw(screen)
    slider.draw(screen)
    back_button.draw(screen)
    mute_button.draw(screen)
    pygame.display.flip()


def process_events(slider, gameover, back_button, screen, mute_button):
    """
    Проверка состояния кнопок
    :param slider:
    :param gameover:
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if back_button.rect.x <= mouse_x <= back_button.rect.x + back_button.rect_width \
                        and back_button.rect.y <= mouse_y <= back_button.rect.y + back_button.rect_height:
                    back_button.draw_click(screen)
                    gameover = True
                elif mute_button.rect.x <= mouse_x <= mute_button.rect.x + mute_button.rect_width \
                        and mute_button.rect.y <= mouse_y <= mute_button.rect.y + mute_button.rect_height:
                    mute_button.draw_click(screen)
                    slider.occupancy.width = 0
                else:
                    gameover = slider.check_click(mouse_x, mouse_y)
            elif event.button == 4:
                mouse_x, mouse_y = event.pos
                gameover = slider.check_scroll(mouse_x, mouse_y, True)
            elif event.button == 5:
                mouse_x, mouse_y = event.pos
                gameover = slider.check_scroll(mouse_x, mouse_y, False)
    return gameover
