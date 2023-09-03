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
        self._canvas = canvas
        self._cell_size = cell_size
        self._outline_width = outline_width
        self._outline_color = outline_color
        self._snake_color = snake_color

    def render(self, snake_body):
        """Renders the snake on the canvas.

        Args:
            snake_body: The list of positions representing the snake body.
        """
        rectangles = self.get_bodys_rectangles(snake_body)

        for r in rectangles:
            pygame.draw.rect(self._canvas, self._snake_color, r)
            corners = [
                (r.left, r.top), (r.right-self._outline_width, r.top), 
                (r.left, r.bottom-self._outline_width), (r.right-self._outline_width, r.bottom-self._outline_width),
            ]
            for c in corners:
                pygame.draw.rect(self._canvas, self._outline_color, (*c, self._outline_width, self._outline_width))

        for i, r in enumerate(rectangles):
            neighbours = rectangles[i-1:i] + rectangles[i+1:i+2]
            sides = [
                (r.move(-1,  0), (r.left, r.top+self._outline_width, self._outline_width, r.height-2*self._outline_width)),
                (r.move( 1,  0), (r.right-self._outline_width, r.top+self._outline_width, self._outline_width, r.height-2*self._outline_width)),
                (r.move( 0, -1), (r.left+self._outline_width, r.top, r.width-2*self._outline_width, self._outline_width)),
                (r.move( 0,  1), (r.left+self._outline_width, r.bottom-self._outline_width, r.width-2*self._outline_width, self._outline_width)),
            ]
            for test_rect, line in sides:
                if test_rect.collidelist(neighbours) < 0:
                    pygame.draw.rect(self._canvas, self._outline_color, line)

    
    def get_bodys_rectangles(self, snake_body):
        """Generates rectangles for each element in the snake body.

        Args:
            snake_body: The list of positions representing the snake body.

        Returns:
            np.ndarray: An array of pygame.Rect objects representing the rectangles.
        """
        return [pygame.Rect(int(element[0] * self._cell_size), 
                            int(element[1] * self._cell_size), 
                            self._cell_size, 
                            self._cell_size) for element in snake_body]

class Snake:
    def __init__(self, 
                 body: Tuple[Vector2],
                 snake_render: SnakeRender,
                 start_direction: Vector2 = Vector2(0, 0)):
        """Initialize a Snake instance.

        Args:
            body (Tuple[Vector2]): Initial positions of the snake's body segments.
            snake_render (SnakeRender): An instance of SnakeRender used for rendering the snake.
        """
        self._body = list(body)
        self._grown = False
        self._snake_render = snake_render
        self._direction = start_direction
    
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
        """Move the snake's body based on its current direction.

        This method updates the position of the snake's body segments based on its current direction. If the snake is not
        moving (i.e., its direction is the zero vector), the body remains stationary. Otherwise, the method calculates the new
        coordinates of the snake's head based on the current head position and direction. The new head position is inserted at
        the beginning of the body segment list, simulating the snake's movement in the specified direction.

        If the snake is set to grow (using the `grow` method), the method does not remove the last body segment, effectively
        increasing the length of the snake.

        Note:
            This method does not directly handle collision detection or interaction with the environment. It is responsible
            solely for updating the internal representation of the snake's body.

        """
        if self._direction != Vector2(0, 0):
            body = self._body[:-1] if not self._grown else self._body[:]
            body.insert(0, body[0] + self._direction)
            self._body = body[:]

            if self._grown: 
                self._grown = False
    
    def grow(self, fruit_coords):
        """Indicate that the snake should grow on the next move."""
        if self._body[0] == fruit_coords:
            self._grown = True
            return True
        return False
    
    def change_direction(self, direction: Vector2):
        self._direction = direction
    
    def get_bodys_coords(self):
        """Return an array of the snake's body coordinates as [x, y] pairs."""
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
        if self._body[0] + self._direction in self._body[1:]:
            return True
        return False
    
    def die_status_by_walls(self, field):
        head = self._body[0] + self._direction

        if 0 <= head.x < field.x_size and\
            0 <= head.y < field.y_size:
            return False
        return True