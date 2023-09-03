from typing import Tuple
import pygame
from pygame.math import Vector2

class FruitRender:
    def __init__(self, cell_size: int, fruit_color: Tuple[int], canvas: pygame.Surface):
        """Initialize FruitRender.

        Args:
            cell_size (int): The size of each cell in pixels.
            canvas (pygame.Surface): The surface where the fruit will be drawn.
        """
        self._cell_size = cell_size
        self._fruit_color = fruit_color
        self._canvas = canvas

    def render(self, position: Vector2):
        """Render the fruit at the specified position on the canvas.

        Args:
            position (Vector2): The position of the fruit.
        """
        rectangle = pygame.Rect(int(position.x * self._cell_size), int(position.y * self._cell_size),
                            self._cell_size, self._cell_size)
        pygame.draw.rect(self._canvas, self._fruit_color, rectangle)

class Fruit:
    def __init__(self, position: Vector2, fruit_render: FruitRender):
        """Initialize Fruit.

        Args:
            position (Vector2): The initial position of the fruit.
            fruit_render (FruitRender): An instance of FruitRender used for rendering.
        """
        self.position = position
        self._fruit_render = fruit_render

    def render(self):
        """Render the fruit using the associated FruitRender instance."""
        self.fruit_render.render(self.position)
