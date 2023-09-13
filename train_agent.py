import os
from src.agent import SnakeAgent

CELL_SIZE, FIELD_SIZE = 30, (32, 18)
SAVE_MODEL_PATH = os.path.join("saved_models", "Snake_AI_Model")
LOGS_PATH = os.path.join("logs")


def main():
    agent = SnakeAgent(
        FIELD_SIZE,
        CELL_SIZE,
        save_model_path=SAVE_MODEL_PATH,
        tensorboard_log=LOGS_PATH,
    )
    agent.train_model(1000)
    agent.evalute_model(10)
    agent.save_model()


if __name__ == "__main__":
    main()