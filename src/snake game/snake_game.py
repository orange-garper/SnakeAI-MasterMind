from typing import Tuple, NamedTuple
import numpy as np

import pygame
from pygame.math import Vector2

class Field(NamedTuple):
    x_size: int
    y_size: int

class Fruit:
    position: Vector2

    def render(self, field: Field, cell_size, canvas):
        return pygame.Rect(int(self.position.x * field.x_size), int(self.position.y * field.y_size),
                            cell_size, cell_size)

class Snake:
    def __init__(self, body: Tuple[Vector2]):
        self._body = list(body)
        self._grown = False
        self.direction = Vector2(0, 0)
    
    def __len__(self):
        return len(self._body)
    
    def __iter__(self):
        return iter(self.get_bodys_coords())
    
    def render(self):
        #TODO: Реализовать рисовку змеи с обводкой
        ...

    def move(self):
        if self.direction != Vector2(0, 0):
            body = self._body[:-1] if not self._grown else self._body[:]
            body.insert(0, body[0] + self._direction)
            self.body = body[:]

            if self._grown: 
                self._grown = False
    
    def grow(self):
        self._grown = True
    
    def get_bodys_coords(self):
        return np.array(list(map(lambda v: [v.x, v.y], self._body)))

class SnakeGame:
    def __init__(self, 
                 field_size: Tuple[int] = (10, 10), 
                 cell_size: int = 10,
                 seed: int = 0):
        
        assert (2, 2) < field_size < (255, 255),\
            f"The field size does not correspond to the supported limits (minimum - (2, 2); maximum - (255, 255)). The specified field size is {field_size}"
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
