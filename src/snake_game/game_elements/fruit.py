from typing import Tuple
import pygame
from pygame.math import Vector2


class FruitRender:
    def __init__(self, cell_size: int, fruit_color: Tuple[int], canvas: pygame.Surface):
        self._cell_size = cell_size
        self._fruit_color = fruit_color
        self._canvas = canvas

    def render(self, position: Vector2):
        rectangle = pygame.Rect(
            int((position.x + 0.25) * self._cell_size),
            int((position.y + 0.25) * self._cell_size),
            self._cell_size // 2,
            self._cell_size // 2,
        )
        pygame.draw.rect(self._canvas, self._fruit_color, rectangle)


class Fruit:
    def __init__(self, position: Vector2, fruit_render: FruitRender):
        self.position = position
        self._fruit_render = fruit_render

    def render(self):
        self._fruit_render.render(self.position)
