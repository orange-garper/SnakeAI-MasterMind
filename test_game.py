from src.snake_game import SnakeGame

CELL_SIZE, CELL_NUMBER_H, CELL_NUMBER_W = 40, 18, 32

if __name__ == "__main__":
    g = SnakeGame(field_size=(CELL_NUMBER_W, CELL_NUMBER_H), cell_size=CELL_SIZE)
    g.init()
