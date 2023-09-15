import os, json   # noqa: E401
from src import HyperparametersDefining

CELL_SIZE, FIELD_SIZE = 30, (32, 18)
LOGS_PATH = os.path.join("logs")
PARAMS_PATH = os.path.join('logs', 'params.json')

if __name__ == "__main__":
    dh = HyperparametersDefining(
        FIELD_SIZE,
        CELL_SIZE,
        log_path=LOGS_PATH,
        total_timesteps=1,
        n_jobs=1,
        n_trials=1,
    )
    result = dh.optimize()
    
    with open(PARAMS_PATH, "w") as file:
        json.dump(result, file)