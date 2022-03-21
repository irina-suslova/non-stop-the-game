"""
Создание линий (леса) с препятствиями для поля
"""
from random import randint
from forest import Forest


def get_lines(count, field_type, mode):
    """
    Генерация списка, в котором нахоятся все объекты Line, используемые в игре (список шаблонов)
    :param count: показывает сколько линий нужно создать
    :param field_type: показывает тип леса в игре (лес из ёлок или лиственных деревьев)
    :return: возвращает готовый список
    """
    lines = []
    for i in range(count):
        if field_type == 'tree':
            number = randint(1, 4)
        elif field_type == 'fir':
            number = randint(5, 6)
        trees = []
        for j in range(randint(0, 2)):
            rand = randint(1, 5)
            if len(trees) != 0:
                while rand in trees:
                    rand = randint(1, 5)
            trees.append(rand)
        lines.append(Forest(number, trees + [0, 6], field_type, i))
        lines[len(lines) - 1].generate(mode)
    return lines
