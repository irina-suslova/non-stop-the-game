"""
Тесты для проекта
"""
import os
import unittest
import pygame
import mock
from constants import Lines_speed, x2_time, boost_time, shield_time
from game import Game
from abstract_line import Line
from water import Water
from road import Road
from forest import Forest
from background import Background
os.environ['SDL_VIDEODRIVER'] = 'dummy'


class TestMove(unittest.TestCase):
    """
    Класс тестов на движение
    """
    def test_move_up(self):
        """
        test move up
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.y = 0
        expected_y = -182
        g.pers.move_order.append(0)
        g.pers.current_step_time = g.pers.step_max_time
        for i in range(20):
            g.pers.move(g.lines)
            g.pers.rect.y -= Lines_speed.lines_speed
        self.assertEqual(g.pers.rect.y, expected_y)

    def test_move_down(self):
        """
        test move down
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.y = 0
        expected_y = 182
        g.pers.move_order.append(1)
        g.pers.current_step_time = g.pers.step_max_time
        for i in range(20):
            g.pers.move(g.lines)
            g.pers.rect.y -= Lines_speed.lines_speed
        self.assertEqual(g.pers.rect.y, expected_y)

    def test_move_right(self):
        """
        test move right
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 0
        expected_x = 182
        g.pers.move_order.append(3)
        g.pers.current_step_time = g.pers.step_max_time
        for i in range(20):
            g.pers.move(g.lines)
        self.assertEqual(g.pers.rect.x, expected_x)

    def test_move_left(self):
        """
        test move left
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.y = g.pers.rect.x = 0
        expected_x = g.pers.rect.x - 182
        g.pers.move_order.append(2)
        g.pers.current_step_time = g.pers.step_max_time
        for i in range(20):
            g.pers.move(g.lines)
        self.assertEqual(g.pers.rect.x, expected_x)

    def test_background_move(self):
        """
        test background move
        """
        back = Background()
        x1 = back.rect_1.x
        x2 = back.rect_2.x
        back.move()
        self.assertEqual((back.rect_1.x, back.rect_2.x), (back.x_shift + x1, back.x_shift + x2))

    def test_abstract_line_move(self):
        """
        test lines move
        """
        line = Line('type')
        y = line.rect.y
        line.move()
        self.assertEqual(line.rect.y, y + line.y_shift)

class TestBordersTrue(unittest.TestCase):
    """
    Тесты на проверку коллизии с границами (true)
    """
    def test_check_right_t(self):
        """
        test check borders right
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 546
        g.pers.rect.y = 364
        g.pers.current_step_time = g.pers.step_max_time
        self.assertTrue(g.pers.check_borders(3))

    def test_check_left_t(self):
        """
        test check borders left
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 546
        g.pers.rect.y = 364
        g.pers.current_step_time = g.pers.step_max_time
        self.assertTrue(g.pers.check_borders(2))

    def test_check_down_t(self):
        """
        test check borders down
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 546
        g.pers.rect.y = 364
        g.pers.current_step_time = g.pers.step_max_time
        self.assertTrue(g.pers.check_borders(1))

    def test_check_up_t(self):
        """
        test check borders up
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 546
        g.pers.rect.y = 364
        g.pers.current_step_time = g.pers.step_max_time
        self.assertTrue(g.pers.check_borders(0))


class TestBordersFalse(unittest.TestCase):
    """
    Тесты на отсутствие коллизии с границами (false)
    """
    def test_check_right_f(self):
        """
        test check borders right
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 1274
        g.pers.rect.y = 364
        g.pers.current_step_time = g.pers.step_max_time
        self.assertFalse(g.pers.check_borders(3))

    def test_check_left_f(self):
        """
        test check borders left
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 0
        g.pers.rect.y = 364
        g.pers.current_step_time = g.pers.step_max_time
        self.assertFalse(g.pers.check_borders(2))

    def test_check_down_f(self):
        """
        test check borders down
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 546
        g.pers.rect.y = 1018
        g.pers.current_step_time = g.pers.step_max_time
        self.assertFalse(g.pers.check_borders(1))

    def test_check_up_f(self):
        """
        test check borders up
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rect.x = 546
        g.pers.rect.y = -182
        g.pers.current_step_time = g.pers.step_max_time
        self.assertFalse(g.pers.check_borders(0))


class PowerUps(unittest.TestCase):
    """
    Тесты бонусов
    """
    def test_double_coins_t(self):
        """
        test double coins true
        """
        pygame.font.init()
        g = Game()
        g.pers.rejim['x2'] = True
        g.pers.x2_time = x2_time
        g.x2_abuse()
        self.assertEqual(2, g.point_per_sec)

    def test_double_coins_f(self):
        """
        test double coins false
        """
        pygame.font.init()
        g = Game()
        g.pers.rejim['x2'] = True
        g.pers.x2_time = 0
        g.x2_abuse()
        self.assertEqual(1, g.point_per_sec)

    def test_boost_normal_t(self):
        """
        test boost true in normal mode true
        :return:
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rejim['boost'] = True
        g.pers.boost_time = boost_time
        g.boost_abuse()
        self.assertEqual(g.lines[0].y_shift, Lines_speed.boost_speed)

    def test_boost_normal_f(self):
        """
        test boost true in normal mode false
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        g.pers.rejim['boost'] = True
        g.pers.boost_time = 0
        g.boost_abuse()
        self.assertEqual(g.lines[0].y_shift, Lines_speed.lines_speed)

    def test_boost_reverse_t(self):
        """
        test boost true in reverse mode true
        """
        pygame.font.init()
        g = Game('reverse')
        g.prepare()
        g.pers.rejim['boost'] = True
        g.pers.boost_time = boost_time
        g.boost_abuse()
        self.assertEqual(g.lines[0].y_shift, -Lines_speed.boost_speed)

    def test_reverse_normal_f(self):
        """
        test boost true in reverse mode false
        """
        pygame.font.init()
        g = Game('reverse')
        g.prepare()
        g.pers.rejim['boost'] = True
        g.pers.boost_time = 0
        g.boost_abuse()
        self.assertEqual(g.lines[0].y_shift, Lines_speed.lines_speed)

    def test_shield_drawing_t(self):
        """
        test shield drawing true
        """
        pygame.font.init()
        g = Game()
        g.pers.rejim['shield'] = True
        g.pers.shield_time = shield_time
        g.shield_abuse()
        self.assertEqual((g.shield_params['rect'].x, g.shield_params['rect'].y),
                         (g.pers.rect.x, g.pers.rect.y))

    def test_shield_drawing_f(self):
        """
        test shield drawing false
        """
        pygame.font.init()
        g = Game()
        g.pers.rejim['shield'] = True
        g.pers.shield_time = 0
        g.shield_abuse()
        self.assertNotEqual((g.shield_params['rect'].x,
                             g.shield_params['rect'].y),
                            (g.pers.rect.x, g.pers.rect.y))

    def test_flag_drawing_t(self):
        """
        test flag drawing true

        """
        pygame.font.init()
        g = Game()
        g.pers.rejim['boost'] = True
        g.pers.boost_time = boost_time
        g.boost_abuse()
        self.assertEqual((g.flag_params['rect'].x,
                             g.flag_params['rect'].y),
                            (g.pers.rect.x, g.pers.rect.y))

    def test_flag_drawing_f(self):
        """
        test flag drawing true

        """
        pygame.font.init()
        g = Game()
        g.pers.rejim['boost'] = True
        g.pers.boost_time = 0
        g.boost_abuse()
        self.assertNotEqual((g.flag_params['rect'].x,
                                g.flag_params['rect'].y),
                             (g.pers.rect.x, g.pers.rect.y))

    def test_remove_powerups(self):
        '''
        Test remove powerups function
        '''
        line = Forest(1, [], 'tree')
        line.remove_powerups()
        self.assertEqual(line.image, line.image_without_powerups)


class TreeCollision(unittest.TestCase):
    """
    Проверка коллизии с деревьями
    """
    def test_tree_collision_f(self):
        """
        test tree collision false
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        lin = Forest(1, [1, 2, 3, 4, 5], 'tree')
        g.lines.append(lin)
        self.assertFalse(g.pers.check_trees_collision(0, g.lines, 'normal'))

    def test_tree_collision_t(self):
        """
        test tree collision true
        """
        pygame.font.init()
        g = Game()
        g.prepare()
        lin = Forest(1, [], 'tree')
        g.lines.append(lin)
        self.assertTrue(g.pers.check_trees_collision(0, g.lines, 'normal'))


class WaterCollision(unittest.TestCase):
    """
    Тесты на коллизию с водой
    """

    def setUp(self):
        """
        Подготовка игры к тесту. Здесь инициализируется библиотека и создаётся объект игры
        """
        pygame.font.init()
        self.game = Game()
        Lines_speed.lines_speed = 0
        self.game.prepare()

    def test_water_collision_f(self):
        """
        test water collision false
        """
        with mock.patch('random.randint', return_value=1):
            w = Water()
        self.game.lines.append(w)
        self.game.pers.add_move_order(0, self.game.lines, 'normal')
        for i in range(20):
            self.game.pers.move(self.game.lines)
        self.assertFalse(self.game.pers.check_water_collision(self.game.lines))

    def test_water_collision_t(self):
        """
        test water collision false

        """
        with mock.patch('random.randint', return_value=3):
            w = Water()
        self.game.lines.append(w)
        self.game.pers.add_move_order(0, self.game.lines, 'normal')
        self.game.pers.speed = 14
        for i in range(20):
            self.game.pers.move(self.game.lines)
        self.assertTrue(self.game.pers.check_water_collision(self.game.lines))


class RoadCollision(unittest.TestCase):
    """
    Тест на коллизию с дорогой
    """
    def setUp(self):
        """
        Подготовка игры к тесту. Здесь инициализируется библиотека и создаётся объект игры
        """
        pygame.font.init()
        self.game = Game()
        Lines_speed.lines_speed = 0
        self.game.prepare()

    def test_road_collision_f(self):
        """
        test road collision false
        """

        with mock.patch('random.randint', return_value=-1):
            r = Road()
        self.game.lines.append(r)
        self.game.pers.add_move_order(0, self.game.lines, 'normal')
        for i in range(20):
            self.game.pers.move(self.game.lines)
        self.assertFalse(self.game.pers.check_road_collision(self.game.lines))


if __name__ == '__main__':
    unittest.main()
