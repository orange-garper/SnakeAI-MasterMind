import pygame, sys
from pygame.math import Vector2
from random import randint

CELL_SIZE, CELL_NUMBER = 20, 36
FRUIT_COLOR = (251, 0, 13)
SNAKE_COLOR = (20, 209, 0)
OUTLINE_COLOR = (0, 0, 0)
OUTLINE_WIDTH = 3
DIRECTION = {
    "K_UP": Vector2(0, -1),
    "K_DOWN": Vector2(0, 1),
    "K_RIGHT": Vector2(1, 0),
    "K_LEFT": Vector2(-1, 0)
}
SCREEN_UPDATE = pygame.USEREVENT

class Fruit:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y
        self.position = Vector2(self.x, self.y)
    
    def render(self):
        fruit = pygame.Rect(int(self.position.x * CELL_SIZE), int(self.position.y * CELL_SIZE),
                            CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, FRUIT_COLOR, fruit)

class Snake:
    
    def __init__(self, body = None):
        self.body = body or [Vector2(10, 10),
                             Vector2(9, 10)]
        self.direction = Vector2(0, 0)
        self.grown = False
    
    def render(self):
        for element in self.body:
            sk_element = pygame.Rect(int(element.x * CELL_SIZE), int(element.y * CELL_SIZE),
                                        CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, sk_element)
        
    def move(self):
        if self.direction != Vector2(0, 0):
            body = self.body[:-1] if not self.grown else self.body[:]
            body.insert(0, body[0] + self.direction)
            self.body = body[:]
            if self.grown: self.grown = False
    
    def add_element(self):
        self.grown = True
    
    def get_coords(self, start_with = 0):
        return [(element.x, element.y) for element in self.body[start_with:]]

class Game:

    def __init__(self):
        self.snake = Snake()
        self.fruit = self._generate_fruit()
    
    def update(self):
        self.snake.move()
        self.do_eat_fruit()
        self.check_hit()
    
    def change_direction(self, event_key):
        vector = next((value for key, value in DIRECTION.items() \
                          if all((getattr(pygame, key) == event_key, \
                            self.snake.body[0] + value != self.snake.body[1]))), None)
        if vector: self.snake.direction = vector
    
    def do_eat_fruit(self):
        if self.snake.body[0] == self.fruit.position:
            self.raise_snake()

    def raise_snake(self):
        self.fruit = self._generate_fruit()
        self.snake.add_element()

    def render(self):
        self.fruit.render()
        self.snake.render()
    
    def _generate_fruit(self):
        fruit_x, fruit_y = None, None
        for x, y in self.snake.get_coords():
            fruit_x = (fruit_x, randint(0, CELL_NUMBER - 1))[fruit_x == x or fruit_x is None]
            fruit_y = (fruit_y, randint(0, CELL_NUMBER - 1))[fruit_y == y or fruit_y is None]
        return Fruit(fruit_x, fruit_y)
    
    def check_hit(self):
        if self.do_hit_by_walls() or self.do_hit_himself():
            self.game_over()
    
    def do_hit_by_walls(self):
        if 0 <= self.snake.body[0].x <= CELL_NUMBER - 1 and \
            0 <= self.snake.body[0].y <= CELL_NUMBER - 1:
            return False
        return True

    def do_hit_himself(self):
        if self.snake.body[0] in self.snake.body[1:]:
            return True
        return False

    def game_over(self):
        self.reset()
    
    def reset(self):
        self.snake = Snake()
        self.fruit = self._generate_fruit()

pygame.init()
screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
clock = pygame.time.Clock()

pygame.time.set_timer(SCREEN_UPDATE, 150)

g = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == SCREEN_UPDATE:
            g.update()
        if event.type == pygame.KEYDOWN:
            g.change_direction(event.key)
    screen.fill((0, 0, 0))
    g.render()
    pygame.display.update()
    clock.tick(60)