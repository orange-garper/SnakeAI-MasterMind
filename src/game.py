import pygame, sys
from pygame.math import Vector2
import secrets

CELL_SIZE, CELL_NUMBER_H, CELL_NUMBER_W = 40, 18, 32
FRUIT_COLOR = (251, 0, 13)
SNAKE_COLOR = (20, 209, 0)
OUTLINE_COLOR = (0, 0, 0)
OUTLINE_WIDTH = 2
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
    
    def render(self, screen):
        rectangle = pygame.Rect(int((self.position.x + 0.25) * CELL_SIZE), int((self.position.y + 0.25) * CELL_SIZE),
                            CELL_SIZE // 2, CELL_SIZE // 2)
        
        pygame.draw.rect(screen, FRUIT_COLOR, rectangle)

class Snake:
    
    def __init__(self, body = None):
        self.body = body or [Vector2(10, 10),
                             Vector2(9, 10)]
        self.direction = Vector2(0, 0)
        self.grown = False
    
    def __len__(self):
        return len(self.body)

    def render(self, screen):
        rectangles = self.render_body()

        for r in rectangles:
            pygame.draw.rect(screen, SNAKE_COLOR, r)
            corners = [
                (r.left, r.top), (r.right-OUTLINE_WIDTH, r.top), 
                (r.left, r.bottom-OUTLINE_WIDTH), (r.right-OUTLINE_WIDTH, r.bottom-OUTLINE_WIDTH),
            ]
            for c in corners:
                pygame.draw.rect(screen, OUTLINE_COLOR, (*c, OUTLINE_WIDTH, OUTLINE_WIDTH))

        for i, r in enumerate(rectangles):
            neighbours = rectangles[i-1:i] + rectangles[i+1:i+2]
            sides = [
                (r.move(-1,  0), (r.left, r.top+OUTLINE_WIDTH, OUTLINE_WIDTH, r.height-2*OUTLINE_WIDTH)),
                (r.move( 1,  0), (r.right-OUTLINE_WIDTH, r.top+OUTLINE_WIDTH, OUTLINE_WIDTH, r.height-2*OUTLINE_WIDTH)),
                (r.move( 0, -1), (r.left+OUTLINE_WIDTH, r.top, r.width-2*OUTLINE_WIDTH, OUTLINE_WIDTH)),
                (r.move( 0,  1), (r.left+OUTLINE_WIDTH, r.bottom-OUTLINE_WIDTH, r.width-2*OUTLINE_WIDTH, OUTLINE_WIDTH)),
            ]
            for test_rect, line in sides:
                if test_rect.collidelist(neighbours) < 0:
                    pygame.draw.rect(screen, OUTLINE_COLOR, line)
    
    def render_body(self):
        return [pygame.Rect(int(element.x * CELL_SIZE), 
                            int(element.y * CELL_SIZE), 
                            CELL_SIZE, 
                            CELL_SIZE) for element in self.body]
            
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
    
    def change_direction(self, event_key):
        vector = next((value for key, value in DIRECTION.items() \
                          if all((getattr(pygame, key) == event_key, \
                            self.snake.body[0] + value != self.snake.body[1]))), None)
        if vector: self.snake.direction = vector
    
    def do_eat_fruit(self):
        if self.snake.body[0] == self.fruit.position:
            self.raise_snake()
    
    def distance(self):
        return ((self.snake.body[0].x - self.fruit.position.x) ** 2 \
                + (self.snake.body[0].y - self.fruit.position.y) ** 2) ** 0.5

    def raise_snake(self):
        self.fruit = self._generate_fruit()
        self.snake.add_element()

    def render(self, screen):
        self.fruit.render(screen)
        self.snake.render(screen)
    
    def _generate_fruit(self):
        coords = self.snake.get_coords()
        free_cells = [(x, y) 
                      for x, y in zip(range(0, CELL_NUMBER_W), range(0, CELL_NUMBER_H)) 
                      if (x, y) not in coords]
        return Fruit(*secrets.choice(free_cells))
    
    def get_len_snake(self):
        return len(self.snake)
    
    def check_end(self):
        if self.check_hit() or self.do_win():
            self.game_over()

    def check_hit(self):
        if self.do_hit_by_walls() or self.do_hit_himself():
            return True
        return False
    
    def do_hit_by_walls(self):
        if 0 <= self.snake.body[0].x <= CELL_NUMBER_W - 1 and \
            0 <= self.snake.body[0].y <= CELL_NUMBER_H - 1:
            return False
        return True

    def do_hit_himself(self):
        if self.snake.body[0] in self.snake.body[1:]:
            return True
        return False

    def game_over(self):
        self.reset()
    
    def do_win(self):
        if len(self.snake.body) >= CELL_NUMBER_W * CELL_NUMBER_H:
            return True
        return False
    
    def reset(self):
        self.snake = Snake()
        self.fruit = self._generate_fruit()