from typing import Tuple, NamedTuple
import numpy as np

import pygame
from pygame.math import Vector2

class Field(NamedTuple):
    x_size: int
    y_size: int


class SnakeGame:
    def __init__(self, 
                 field_size: Tuple[int] = (10, 10), 
                 cell_size: int = 10,
                 seed: int = 0,
                 player_mode: str = "human"):
        _metadata = {"player_modes": ["human", "AI"]}
        
        assert (2, 2) < field_size < (512, 512),\
            f"The field size does not correspond to the supported limits (minimum - (2, 2); maximum - (512, 512)). The specified field size is {field_size}"
        self._field = Field(*field_size)

        assert 2 < cell_size,\
            f"The cell size must be greater than one pixel. The set cell size is {cell_size}"
        self._cell_size = cell_size

        #TODO: Реализовать параметр "seed"

        self._fruit_color = (251, 0, 13)
        self._snake_color = (20, 209, 0)
        self._outline_color = (0, 0, 0)
        self._outline_width = min(1, self._cell_size // 10)
        self._direction = {
            "UP": Vector2(0, -1),
            "LEFT": Vector2(-1, 0),
            "DOWN": Vector2(0, 1),
            "RIGHT": Vector2(1, 0),
        }
