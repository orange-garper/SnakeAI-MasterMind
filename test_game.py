from src.snake_game import SnakeGame
import pygame
import sys

CELL_SIZE, CELL_NUMBER_H, CELL_NUMBER_W = 40, 18, 32
FRUIT_COLOR = (251, 0, 13)
SNAKE_COLOR = (20, 209, 0)
OUTLINE_COLOR = (0, 0, 0)
OUTLINE_WIDTH = 1
SCREEN_UPDATE = pygame.USEREVENT

g = SnakeGame(field_size=(CELL_NUMBER_W, CELL_NUMBER_H),
              cell_size=CELL_SIZE)

g.init()
