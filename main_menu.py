"""
Отображение главного меню.
Фон + кнопки
"""
import sys
import pygame
from background import Background
from constants import size
from button import Button
from game_name import GameName


def main_loop(exit, gameover, highscores, name, screen, start_game,
              settings, outfits, background):
    """
    Запуск всех процессов
    Отрисовка
    """
    while not gameover:
        gameover = process_events(exit, gameover, highscores, start_game,
                                  settings, outfits, background, screen)
        process_draw(exit, highscores, name, screen, start_game,
                     settings, outfits, background)
        pygame.time.wait(10)
    if gameover:
        sys.exit()


def prepare():
    """
    Экран меню
    """
    screen = pygame.display.set_mode((size), pygame.RESIZABLE)  # Установка размеров окна
    gameover = False
    name = GameName()
    start_game = Button('static/menu/play_1.png', 'static/menu/play_2.png')
    highscores = Button('static/menu/highscores_1.png', 'static/menu/highscores_2.png')
    exit = Button('static/menu/exit_1.png', 'static/menu/exit_2.png')
    settings = Button('static/menu/settings_1.png', 'static/menu/settings_2.png')
    outfits = Button('static/menu/outfits_1.png', 'static/menu/outfits_2.png')
    background = Background()
    return exit, gameover, highscores, name, screen, start_game \
        , settings, outfits, background


def process_draw(exit, highscores, name, screen,
                 start_game, settings, outfits, background):
    """
    Отриосвка фона, заголовка и кнопок главного меню
    """
    background.draw(screen)
    name.draw(screen)
    start_game.draw(screen)
    highscores.draw(screen)
    exit.draw(screen)
    settings.draw(screen)
    outfits.draw(screen)
    pygame.display.flip()


def process_events(exit, gameover, highscores, start_game, settings,
                   outfits, background, screen):
    """
    Проверка нажатий
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                gameover = highscores.check_click(mouse_x, mouse_y, background, screen) or \
                           start_game.check_click(mouse_x, mouse_y, background, screen) \
                               or exit.check_click(mouse_x, mouse_y, background, screen) or \
                           settings.check_click(mouse_x, mouse_y, background, screen) \
                               or outfits.check_click(mouse_x, mouse_y, background, screen)
    return gameover
