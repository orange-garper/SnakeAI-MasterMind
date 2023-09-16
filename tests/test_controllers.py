import unittest, pygame  # noqa: E401
from pygame.math import Vector2
from src import AIsController, HumansController


class TestSnakeControllers(unittest.TestCase):
    def test_human_controller_press_button(self):
        human_controller = HumansController()
        snake_body = [Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)]

        # Попробуйте симулировать нажатие разных клавиш и проверьте, что состояние контроллера обновляется правильно
        human_controller.press_button(pygame.K_DOWN, snake_body)  # Move down
        self.assertTupleEqual(tuple(map(int, human_controller.get_action)), (0, 1))

        human_controller.press_button(pygame.K_RIGHT, snake_body)  # Move left
        self.assertTupleEqual(tuple(map(int, human_controller.get_action)), (0, 1))

    def test_ai_controller_press_button(self):
        ai_controller = AIsController()
        snake_body = [Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)]

        ai_controller.press_button(2, snake_body)  # Move down
        self.assertTupleEqual(tuple(map(int, ai_controller.get_action)), (0, 1))
        self.assertFalse(ai_controller.do_stupid)

        ai_controller.press_button(3, snake_body)  # Move left
        self.assertTupleEqual(tuple(map(int, ai_controller.get_action)), (0, 1))
        self.assertTrue(ai_controller.do_stupid)
