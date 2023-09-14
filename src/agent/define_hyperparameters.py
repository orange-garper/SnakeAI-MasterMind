import optuna
from .agent import SnakeAgent
from ..gym_environment import RewardParametersPack
from typing import Tuple


class HyperparametersDefining:
    def __init__(
        self,
        field_size: Tuple[int, int],
        cell_size: int,
        *,
        log_path: str = None,
        total_timesteps: int = 10000,
        n_trials: int = 100,
        n_jobs: int = 1,
        n_eval_episodes: int = 10,
        verbose: bool = False,
    ):
        self._field_size = field_size
        self._cell_size = cell_size
        self._log_path = log_path
        self._total_timesteps = total_timesteps
        self._n_trials = n_trials
        self._n_jobs = n_jobs
        self._n_eval_episodes = n_eval_episodes
        self._verbose = verbose

    def _get_hyperparameters(self, trial):
        return dict(
            learning_rate=trial.suggest_float("learning_rate", 1e-5, 1e-4, log=True),
            n_steps=64 * trial.suggest_int("n_steps", 32, 128, log=True),
            gae_lambda=trial.suggest_float("gae_lambda", 0.8, 0.99, log=True),
            gamma=trial.suggest_float("gamma", 0.8, 0.9999, log=True),
            ent_coef=trial.suggest_float("ent_coef", 1e-4, 0.1, log=True),
            clip_range=trial.suggest_float("clip_range", 0.1, 0.4, log=True),
            reward_parameters=RewardParametersPack(
                step_reward_multiplier=trial.suggest_float(
                    "step_reward_multiplier", 0.5, 2, log=True
                ),
                food_reward_multiplier=trial.suggest_float(
                    "food_reward_multiplier", 0.5, 2, log=True
                ),
                stupid_reward_multiplier=trial.suggest_float(
                    "stupid_reward_multiplier", 0.5, 2, log=True
                ),
                death_reward_multiplier=trial.suggest_float(
                    "death_reward_multiplier", 0.5, 2, log=True
                ),
                victory_reward_multiplier=trial.suggest_float(
                    "victory_reward_multiplier", 0.5, 2, log=True
                ),
                max_steps_reward_multiplier=trial.suggest_float(
                    "max_steps_reward_multiplier", 0.5, 2, log=True
                ),
                multiply_by_length=trial.suggest_categorical(
                    "multiply_by_length", [False, True]
                ),
            ),
        )

    def _optimize_agent(self, trial):
        model_params = self._get_hyperparameters(trial)
        agent = SnakeAgent(
            self._field_size,
            self._cell_size,
            verbose=self._verbose,
            tensorboard_log=self._log_path,
            **model_params,
        )

        agent.train_model(total_timesteps=self._total_timesteps)
        mean_reward, _ = agent.evalute_model(n_eval_episodes=self._n_eval_episodes)
        agent.close_environment()

        return mean_reward

    def optimize(self):
        study = optuna.create_study(direction="maximize")
        study.optimize(
            self._optimize_agent, n_trials=self._n_trials, n_jobs=self._n_jobs
        )
        return study.best_params
