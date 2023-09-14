import os
from src.agent import HyperparametersDefining

CELL_SIZE, FIELD_SIZE = 30, (32, 18)
LOGS_PATH = os.path.join("logs")

if __name__ == "__main__":
    dh = HyperparametersDefining(
        FIELD_SIZE,
        CELL_SIZE,
        log_path=LOGS_PATH,
        total_timesteps=50000,
        n_jobs=2,
        n_trials=200,
    )
    print(dh.optimize())
