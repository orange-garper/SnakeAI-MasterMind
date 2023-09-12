from abc import ABC, abstractmethod
from typing import List, Tuple
import pygame
from pygame.math import Vector2


class AbstractController(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def press_button(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    @abstractmethod
    def get_action(self):
        raise NotImplementedError()


class HumansController(AbstractController):
    def __init__(self, start_pressed_button: str | Vector2 = None):
        self._buttons = {
            "K_UP": Vector2(0, -1),
            "K_LEFT": Vector2(-1, 0),
            "K_DOWN": Vector2(0, 1),
            "K_RIGHT": Vector2(1, 0),
        }
        self._pressed_button = start_pressed_button or Vector2(0, 0)
        self._do_stupid: bool | None = None

    def press_button(self, event_key: int, snake_body: List[Vector2]):
        self._pressed_button = next(
            (
                value
                for key, value in self._buttons.items()
                if getattr(pygame, key) == event_key
                and (do_not_stupid := (snake_body[0] + value != snake_body[1]))
            ),
            self._pressed_button,
        )
        self._do_stupid = not do_not_stupid

    @property
    def get_action(self):
        if self._pressed_button is None:
            return
        return self._pressed_button


class AIsController(AbstractController):
    def __init__(self, start_pressed_button: str | Vector2 = None):
        self._buttons = {
            "0": Vector2(0, -1),
            "1": Vector2(-1, 0),
            "2": Vector2(0, 1),
            "3": Vector2(1, 0),
        }
        self._pressed_button = start_pressed_button or Vector2(0, 0)

    def press_button(self, ais_action: int, snake_body: List[Vector2]):
        assert (
            str(ais_action) in self._buttons
        ), f"Oh, is your artificial intelligence so stupidly configured?\
Your artificial intelligence decided that it was necessary to violate the existing boundaries of reality,\
and intended to perform an action under the number {ais_action},\
which is even worse than dividing by zero.\
The {ais_action} number is not recorded in self._buttons,\
so come back when you fix your 'child', which you obviously made under booze.\
The eagle stirs up her nest, isn't it?)"

        action = self._buttons.get(str(ais_action))
        if do_not_stupid := snake_body[0] + action != snake_body[1]:
            self._pressed_button = action
            self._do_stupid = not do_not_stupid

    @property
    def get_action(self):
        if self._pressed_button is None:
            return
        return self._pressed_button

    def do_stupid(self):
        return self._do_stupid
