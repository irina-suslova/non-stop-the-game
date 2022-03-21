import pygame
from constants import black, white, timer_value, width, height
from time import time


class Timer:
    """
    The timer-class.
    """
    def __init__(self):
        """
        The timer-initialising function
        """
        self.value = timer_value
        self.field = pygame.Rect(0, 0, 75, 30)
        self.font = pygame.font.SysFont("monospace", 30)
        self.time = time()

    def draw(self, screen, person):
        """
        The timer drawing function
        """
        if self.not_dead_yet(person):
            pygame.draw.rect(screen, black, self.field, 0)
            pygame.draw.rect(screen, white, self.field, 1)
            if time() - self.time > 1:
                self.value -= int(time() - self.time)
                self.time = time()
            if self.value % 60 < 10:
                label = self.font.render(str(self.value // 60) + ':0' + str(self.value % 60), 1, (255, 255, 255))
            else:
                label = self.font.render(str(self.value // 60) + ':' + str(self.value % 60), 1, (255, 255, 255))
            screen.blit(label, self.field)
        else:
            person.dead = True



    def not_dead_yet(self, person):
        """
        Checks if the person is alive
        """
        if self.value > 0 and not person.dead:
            return True
        else:
            return False