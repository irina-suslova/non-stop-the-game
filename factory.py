"""
Файл с созданием класса Фабрики (паттерн проектирования)
"""
from forest import Forest
from water import Water
from road import Road


class AbstractFactory:
    """
    Абстрактная фабрика, от которой наследуюся все остальные
    """
    def create_forest(self, **kwargs):
        """
        Создание леса
        :param kwargs:
        :return:
        """

    def create_water(self, **kwargs):
        """
        Создание воды
        :param kwargs:
        :return:
        """

    def create_road(self, **kwargs):
        """
        Создание дороги
        :param kwargs:
        :return:
        """


class Factory(AbstractFactory):
    """
    Фабрика, создающая необходимые линии для поля
    """
    def create_forest(self, number=0, trees=[], type_forest='', index=-1):
        """
        Создание полосы леса
        :param number: вид (цвет) полосы леса
        :param trees: список с логическими координатами деревьев на полосе
        :param type_forest: вид леса - 'fir' (хвойный лес) или 'tree' (лиственный лес)
        :param index: уникальный номер для каждого шаблона полосы, используется для картинки полосы
        :return: возвращает готовый объект лесной полосы
        """
        return Forest(number, trees, type_forest, index)

    def create_water(self):
        """
        Создание полосы воды
        :return: возвращает готовый объект полосы с водой
        """
        return Water()

    def create_road(self):
        """
        Создание полосы, по которой ходит толпа
        :return: возвращает готовый объект полосы с толпой
        """
        return Road()
