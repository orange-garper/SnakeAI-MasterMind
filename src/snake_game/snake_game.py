from typing import Tuple, NamedTuple
from random import sample
import pygame
from pygame.math import Vector2
from .game_elements import HumansController, AIsController, Snake, SnakeRender, Fruit, FruitRender
import sys

class Field(NamedTuple):
    x_size: int
    y_size: int
    cell_size: int


class SnakeGame:
    def __init__(self,
                 field_size: Tuple[int] = (10, 10), 
                 cell_size: int = 10,
                 seed: int | None = None,
                 player_mode: str = "human"):
        self._metadata = {"player_modes": ["human", "AI"], "render_fps": 60}
        
        assert (2, 2) < field_size < (512, 512),\
            f"The field size does not correspond to the supported limits (minimum - (2, 2); maximum - (512, 512)). The specified field size is {field_size}"
        assert 2 < cell_size,\
            f"The cell size must be greater than one pixel. The set cell size is {cell_size}"
        self._field = Field(*field_size, cell_size)

        #TODO: Реализовать параметр "seed"
        self.seed = seed

        assert player_mode in self._metadata["player_modes"],\
            f"The set player mode is not predefined for the class. The current player mode is {player_mode}."
        self._player_mode = player_mode
        
        self._canvas = pygame.Surface(size=(self._field.x_size * self._field.cell_size, 
                                            self._field.y_size * self._field.cell_size))
        self._fruit_color = (251, 0, 13)
        self._snake_color = (20, 209, 0)
        self._outline_color = (0, 0, 0)
        self._outline_width = min(1, self._field.cell_size // 10)
        self.window = None
        self.clock = None
        
        self._generate_game()
    
    def init(self, render_mode = True):
        
        if self.window is None and render_mode == True:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self._field.x_size * self._field.cell_size, self._field.y_size * self._field.cell_size))
            self._screen_update = pygame.USEREVENT
            pygame.time.set_timer(self._screen_update, 150)
        if self.clock is None and render_mode == True:
            self.clock = pygame.time.Clock()

        if render_mode == True:
            if self._player_mode == "human":
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit
                        if event.type == self._screen_update:
                            self.update()
                        if event.type == pygame.KEYDOWN:
                            self.make_action(event.key)
                    
                    self.render()
                    self.window.blit(self._canvas, self._canvas.get_rect())
                    pygame.display.update()

                    self.clock.tick(self._metadata["render_fps"])
            else:
                self.render()
                pygame.event.pump()
                pygame.display.update()
    
    def render(self):
        self._canvas.fill((0, 0, 0))
        self._fruit.render()
        self._snake.render()
    
    def make_action(self, action):
        self._controller.press_button(action, self._snake.get_body())
        self._snake.change_direction(self._controller.get_action)

        if self._player_mode == "AI":
            self.update()
    
    def update(self):
        if self.game_over: 
            self.reset()
        else:
            self._snake.move()
            if self._snake.grow(self._fruit.position):
                self._fruit = self._generate_fruit()
    
    def reset(self):
        self._generate_game()

    def _generate_game(self):
        if self.seed is None:
            self._snake: Snake = self._generate_snake(snake_body=(Vector2(self._field.x_size // 2, self._field.y_size // 2),
                                               Vector2(self._field.x_size // 2 - 1, self._field.y_size // 2)))
            self._fruit: Fruit = self._generate_fruit()
            
            if self._player_mode == "human":
                self._controller = HumansController()
            elif self._player_mode == "AI":
                self._controller = AIsController()

    
    def _generate_snake(self, snake_body: Tuple[Vector2]) -> Snake:
        if self._player_mode == "human":
            start_direction = Vector2(0, 0)
        elif self._player_mode == "AI":
            start_direction = self._direction["RIGHT"]

        return Snake(body=snake_body,
                     snake_render=SnakeRender(canvas=self._canvas,
                                         cell_size=self._field.cell_size,
                                         outline_width=self._outline_width,
                                         outline_color=self._outline_color,
                                         snake_color=self._snake_color),
                     start_direction=start_direction)

    def _generate_fruit(self, defined_coordinates = None) -> Fruit:
        if defined_coordinates is None:
            
            assert self._snake is not None, \
                "Before generating the coordinates for the Fruit, the coordinates of the Snake itself are needed. Apparently it hasn't been initialized yet."
            
            snake_coords = self._snake.get_bodys_coords()
            available_cells = [(x, y) for x in range(self._field.x_size) 
                                    for y in range(self._field.y_size)
                                    if (x, y) not in snake_coords]
            fruit_coords = sample(available_cells, k=1)
        else:
            fruit_coords = defined_coordinates

        return Fruit(position=Vector2(*fruit_coords),
                     fruit_render=FruitRender(cell_size=self._field.cell_size,
                                              fruit_color=self._fruit_color,
                                              canvas=self._canvas))
    
    @property
    def game_over(self):
        return self._snake.die_status or self._snake.die_status_by_walls(self._field)