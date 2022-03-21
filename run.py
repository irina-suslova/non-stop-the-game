"""
Запуск игры
"""
# from game import Game
import sys
import os
import pygame
from main_menu import prepare, main_loop


def main():
    """
    Запуск всей игры
    :return:
    """
    pygame.init()  # Инициализация библиотеки
    pygame.font.init()
    exit, gameover, highscores, name, screen, start_game, \
    settings, outfits, background = prepare()
    main_loop(exit, gameover, highscores, name, screen,
              start_game, settings, outfits, background)
    sys.exit()


if __name__ == "__main__":
    os.environ['PYGAME_RUN_TESTS'] = '0'
    main()
