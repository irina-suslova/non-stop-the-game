"""
Описание полосы с водой
"""
import random
import pygame
from PIL import Image
from abstract_line import Line


class Water(Line):
    """
    Класс водной полосы
    """
    water_name = 'static/templates/water.png'
    flower_names = [
        'static/templates/kuvsh_1.png',
        'static/templates/kuvsh_2.png',
    ]
    number = 0

    def __init__(self):
        """
        Инициализация
        """
        super().__init__('water')
        self.flowers = []
        self.image = pygame.image
        self.generate()

    def generate_flowers(self):
        """
        Рандомная расстановка цветов на полосе воды
        """
        for i in range(7):
            if random.randint(1, 3) in [1, 2]:
                self.flowers.append(i)

    def generate(self):
        """
        Создание единой полосы (картиники) с водой
        """
        self.generate_flowers()
        coords_x, images = super().generate_coords(self.flowers, self.flower_names)

        line_name = 'static/field/water_' + str(Water.number) + '.png'
        background_name = Water.water_name
        Water.number = (Water.number + 1) % 7
        line = Image.open(line_name)
        background_line = Image.open(background_name)
        line.paste(background_line, (0, 0))

        for i in range(len(coords_x)):
            name_image = Image.open(images[i])
            line.paste(name_image, (coords_x[i], 0), name_image)
        line.save(line_name)
        self.image = pygame.image.load(line_name)

    def draw(self, screen):
        """
        Отрисовка
        """
        super().draw(screen, self.image, self.rect)
