from src import SnakeGame

CELL_SIZE, FIELD_SIZE = 30, (32, 18)

if __name__ == "__main__":
    g = SnakeGame(field_size=FIELD_SIZE, cell_size=CELL_SIZE)
    g.init()
