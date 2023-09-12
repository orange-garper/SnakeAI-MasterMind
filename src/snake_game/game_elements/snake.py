from typing import Tuple
import numpy as np
import pygame
from pygame.math import Vector2


class SnakeRender:
    def __init__(
        self,
        canvas,
        cell_size: int,
        outline_width: int,
        outline_color: Tuple[int],
        snake_color: Tuple[int],
    ):
        self._canvas = canvas
        self._cell_size = cell_size
        self._outline_width = outline_width
        self._outline_color = outline_color
        self._snake_color = snake_color

    def render(self, snake_body):
        rectangles = self.get_bodys_rectangles(snake_body)

        for r in rectangles:
            pygame.draw.rect(self._canvas, self._snake_color, r)
            corners = [
                (r.left, r.top),
                (r.right - self._outline_width, r.top),
                (r.left, r.bottom - self._outline_width),
                (r.right - self._outline_width, r.bottom - self._outline_width),
            ]
            for c in corners:
                pygame.draw.rect(
                    self._canvas,
                    self._outline_color,
                    (*c, self._outline_width, self._outline_width),
                )

        for i, r in enumerate(rectangles):
            neighbours = rectangles[i - 1 : i] + rectangles[i + 1 : i + 2]
            sides = [
                (
                    r.move(-1, 0),
                    (
                        r.left,
                        r.top + self._outline_width,
                        self._outline_width,
                        r.height - 2 * self._outline_width,
                    ),
                ),
                (
                    r.move(1, 0),
                    (
                        r.right - self._outline_width,
                        r.top + self._outline_width,
                        self._outline_width,
                        r.height - 2 * self._outline_width,
                    ),
                ),
                (
                    r.move(0, -1),
                    (
                        r.left + self._outline_width,
                        r.top,
                        r.width - 2 * self._outline_width,
                        self._outline_width,
                    ),
                ),
                (
                    r.move(0, 1),
                    (
                        r.left + self._outline_width,
                        r.bottom - self._outline_width,
                        r.width - 2 * self._outline_width,
                        self._outline_width,
                    ),
                ),
            ]
            for test_rect, line in sides:
                if test_rect.collidelist(neighbours) < 0:
                    pygame.draw.rect(self._canvas, self._outline_color, line)

    def get_bodys_rectangles(self, snake_body):
        return [
            pygame.Rect(
                int(element[0] * self._cell_size),
                int(element[1] * self._cell_size),
                self._cell_size,
                self._cell_size,
            )
            for element in snake_body
        ]


class Snake:
    def __init__(
        self,
        body: Tuple[Vector2],
        snake_render: SnakeRender,
        start_direction: Vector2 = Vector2(0, 0),
    ):
        self._body = list(body)
        self._grown = False
        self._snake_render = snake_render
        self._direction = start_direction

    def __len__(self):
        return len(self._body)

    def __iter__(self):
        return iter(self.get_bodys_coords())

    def render(self):
        self._snake_render.render(self.get_bodys_coords())

    def move(self):
        if self._direction != Vector2(0, 0):
            body = self._body[:-1] if not self._grown else self._body[:]
            body.insert(0, body[0] + self._direction)
            self._body = body[:]

            if self._grown:
                self._grown = False

    def grow(self, fruit_coords):
        if self._body[0] == fruit_coords:
            self._grown = True
            return True
        return False

    def change_direction(self, direction: Vector2):
        self._direction = direction

    def get_bodys_coords(self):
        return list(map(lambda v: (v.x, v.y), self._body))

    def get_body(self):
        return self._body

    def get_direction(self):
        return self._direction

    @property
    def grown_status(self):
        return self._grown

    @property
    def die_status(self):
        if self._body[0] + self._direction in self._body[1:-1]:
            return True
        return False

    def die_status_by_walls(self, field):
        head = self._body[0] + self._direction

        if 0 <= head.x < field.x_size and 0 <= head.y < field.y_size:
            return False
        return True
