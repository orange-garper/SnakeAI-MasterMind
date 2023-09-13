from src.snake_game import SnakeGame

CELL_SIZE, FIELD_SIZE = 40, (18, 32)

if __name__ == "__main__":
    g = SnakeGame(field_size=FIELD_SIZE, cell_size=CELL_SIZE)
    g.init()
