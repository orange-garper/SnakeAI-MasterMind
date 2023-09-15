import os
from src import SnakeAgent

CELL_SIZE, FIELD_SIZE = 30, (32, 18)
saved_model = os.path.join("saved_models", "Snake_AI_Model.zip")

if __name__ == "__main__":
    model = SnakeAgent.load_model(
        saved_model, field_size=FIELD_SIZE, cell_size=CELL_SIZE
    )
    model.evalute_model(10)
