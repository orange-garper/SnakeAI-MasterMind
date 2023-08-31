from typing import Tuple
import numpy as np
import pygame
from pygame.math import Vector2

class SnakeRender:
    def __init__(self,
                 canvas,
                 cell_size: int,
                 outline_width: int,
                 outline_color: Tuple[int],
                 snake_color: Tuple[int]):
        """Initializes the SnakeRender object.

        Args:
            canvas (pygame.Surface): The canvas to draw on.
            cell_size (int): The size of each cell in pixels.
            outline_width (int): The width of the outline.
            outline_color (Tuple[int]): The color of the outline as an RGB tuple.
            snake_color (Tuple[int]): The color of the snake body as an RGB tuple.
        """
        self.canvas = canvas
        self.cell_size = cell_size
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.snake_color = snake_color

    def render(self, snake_body):
        """Renders the snake on the canvas.

        Args:
            snake_body: The list of positions representing the snake body.
        """
        rectangles = self.get_bodys_rectangles(snake_body)
        corners = self.get_rectangles_corners(rectangles)
        lines = self.get_rectangles_collides(rectangles)

        for r in rectangles:
            pygame.draw.rect(self.canvas, self.snake_color, r)
        
        for c in corners:
            pygame.draw.rect(self.canvas, self.outline_color, c)
        
        for l in lines:
            pygame.draw.rect(self.canvas, self.outline_color, l)
    
    def get_rectangles_corners(self, rectangles):
        """Generates corner coordinates for each rectangle.

        Args:
            rectangles: An array of pygame.Rect objects representing the rectangles.

        Returns:
            np.ndarray: An array of corner coordinates.
        """
        rectangles_corners = []
        for r in rectangles:
            corners = [
                (r.left, r.top), (r.right-self.outline_width, r.top), 
                (r.left, r.bottom-self.outline_width), (r.right-self.outline_width, r.bottom-self.outline_width)
            ]
            rectangles_corners.append(corners)
        return np.array(rectangles_corners).ravel()
    
    def get_rectangles_collides(self, rectangles):
        """Generates lines for separating snake body segments.

        Args:
            rectangles: An array of pygame.Rect objects representing the rectangles.

        Returns:
            np.ndarray: An array of line coordinates.
        """
        rectangles_lines = []

        for r1, r, r3 in zip(np.roll(rectangles, 1), rectangles, np.roll(rectangles, -1)):
            neighbours = r1 + r3
            sides = [
                (r.move(-1,  0), (r.left, r.top+self.outline_width, self.outline_width, r.height-2*self.outline_width)),
                (r.move( 1,  0), (r.right-self.outline_width, r.top+self.outline_width, self.outline_width, r.height-2*self.outline_width)),
                (r.move( 0, -1), (r.left+self.outline_width, r.top, r.width-2*self.outline_width, self.outline_width)),
                (r.move( 0,  1), (r.left+self.outline_width, r.bottom-self.outline_width, r.width-2*self.outline_width, self.outline_width)),
            ]
            lines = [line for test_rect, line in sides if test_rect.collidelist(neighbours) < 0]
            rectangles_lines.append(lines)
        return np.array(rectangles_lines).ravel()
    
    def get_bodys_rectangles(self, snake_body):
        """Generates rectangles for each element in the snake body.

        Args:
            snake_body: The list of positions representing the snake body.

        Returns:
            np.ndarray: An array of pygame.Rect objects representing the rectangles.
        """
        return np.array([pygame.Rect(int(element[0] * self.cell_size), 
                            int(element[1] * self.cell_size), 
                            self.cell_size, 
                            self.cell_size) for element in snake_body])

class Snake:
    def __init__(self, 
                 body: Tuple[Vector2],
                 snake_render: SnakeRender):
        """Initialize a Snake instance.

        Args:
            body (Tuple[Vector2]): Initial positions of the snake's body segments.
            snake_render (SnakeRender): An instance of SnakeRender used for rendering the snake.
        """
        self._body = list(body)
        self._grown = False
        self._snake_render = snake_render
        self.direction = Vector2(0, 0)
    
    def __len__(self):
        """Return the number of segments in the snake's body."""
        return len(self._body)
    
    def __iter__(self):
        """Return an iterator over the coordinates of the snake's body segments."""
        return iter(self.get_bodys_coords())
    
    def render(self):
        """Render the snake's body using the associated SnakeRender instance."""
        self._snake_render.render(self.get_bodys_coords())

    def move(self):
        """Move the snake's body based on its current direction."""
        if self.direction != Vector2(0, 0):
            body = self._body[:-1] if not self._grown else self._body[:]
            body.insert(0, body[0] + self._direction)
            self.body = body[:]

            if self._grown: 
                self._grown = False
    
    def grow(self):
        """Indicate that the snake should grow on the next move."""
        self._grown = True
    
    def get_bodys_coords(self):
        """Return an array of the snake's body coordinates as [x, y] pairs."""
        return np.array(list(map(lambda v: [v.x, v.y], self._body)))