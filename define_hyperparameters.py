from src.agent import HyperparametersDefining

CELL_SIZE, FIELD_SIZE = 10, (18, 32)

if __name__ == '__main__':
    dh = HyperparametersDefining(FIELD_SIZE, CELL_SIZE, total_timesteps=10, n_trials=1, n_jobs=4)
    print(dh.optimize())
