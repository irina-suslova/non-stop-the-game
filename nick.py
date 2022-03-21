"""
Имя игрока
"""


def add_nick(nick, score, mode):
    """
    Добавление ника игрока и его очков
    """
    write_to_file(nick, score, mode)


def sorting(highscores):
    """
    Функция для сортировки словаря по значениям
    """
    nicks = []
    scores = []
    for i in highscores.keys():     # Разбиваем на два списка
        scores.append(highscores[i])    # Очки
        nicks.append(i)                 # Ники игроков

    for i in range(len(scores)):
        # Сортировка пузырьком (тк максимум элементов 11, то это будет не долго)
        for j in range(len(scores) - 1):
            if scores[j] < scores[j + 1]:
                scores[j], scores[j + 1] = scores[j + 1], scores[j]
                # Вместе с изменениями в массиве очков
                nicks[j], nicks[j + 1] = nicks[j + 1], nicks[j]      # Меняются и ники

    new_highscores = [nicks, scores]
    # Собираем 2 списка в один (чтобы вернуть одной переменной)
    return new_highscores


def read_from_file(file_name):       # Функция чтения из файла текущего списка рекордов
    """
    Функция чтения из файла текущего списка рекордов
    """
    file = open(file_name, 'r')

    highscores = dict()
    for line in file:
        nick, score = map(str, line.split())
        score = int(score)
        highscores[nick] = score
    file.close()

    return highscores       # Возвращаем словарь


def write_to_file(new_nick, new_score, mode):         # Функция записи в файл
    """
    Функция записи в файл
    """
    if mode == 'normal':
        file_name = 'highscores.txt'
    elif mode == 'reverse':
        file_name = 'highscores_inversed.txt'
    else:
        file_name = 'highscores_on_time.txt'
    highscores = read_from_file(file_name)
    highscores[new_nick] = new_score
    highscores = sorting(highscores)
    # При записи данных в словарь нарушается последовательность
    # и не получается сохранить словарь отсортированным
    # Поэтому можно хранить данные в 2-х списках,
    # где элементы сопоставленны через индексы
    file = open(file_name, 'w')

    nicks = highscores[0]
    scores = highscores[1]
    i = 0
    for i in range(len(nicks)):
        if i < 10:
            file.write('{} {}\n'.format(nicks[i], scores[i]))
        i += 1

    file.close()
