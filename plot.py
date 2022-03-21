import pygame
import sys


class Picture:
    images = [
        pygame.image.load('static/menu/first.png'),
        pygame.image.load('static/menu/second.png'),
        pygame.image.load('static/menu/third.png'),
        pygame.image.load('static/menu/fourth.png'),
    ]
    rect = pygame.Rect((0, 0), (1280, 800))

    def __init__(self):
        self.number = 0
        self.clicked = False

    def main_loop(self, screen):
        self.process_draw(screen)
        self.number += 1
        while not self.clicked:
            self.proces_events()
        self.clicked = False
        return

    def process_draw(self, screen):
        screen.blit(Picture.images[self.number], Picture.rect)
        pygame.display.flip()

    def proces_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.clicked = True
