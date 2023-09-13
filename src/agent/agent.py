from ..gym_environment import SnakeEnvironment
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import CnnPolicy
from stable_baselines3 import PPO


class SnakeAgent:
    def __init__(
        self,
        field_size,
        cell_size,
        *,
        save_model_path: str | None = None,
        tensorboard_log=None,
        render_mode="human",
        verbose: int = 1,
        learning_rate=0.0005,
        n_steps=256,
        gae_lambda=0.95,
        gamma=0.99,
        ent_coef=0.01,
        clip_range=0.2,
        n_epochs=10,
        batch_size=64,
    ):
        self._environment = VecFrameStack(
            DummyVecEnv(
                [lambda: SnakeEnvironment(field_size, cell_size, render_mode=None)]
            ),
            4,
            channels_order="last",
        )
        self._eval_environment = VecFrameStack(
            DummyVecEnv(
                [lambda: Monitor(SnakeEnvironment(field_size, cell_size, render_mode='human'))]
            ),
            4,
            channels_order="last",
        )

        self._model = PPO(
            CnnPolicy,
            self._environment,
            verbose=verbose,
            learning_rate=learning_rate,
            n_steps=n_steps,
            gae_lambda=gae_lambda,
            gamma=gamma,
            ent_coef=ent_coef,
            clip_range=clip_range,
            n_epochs=n_epochs,
            batch_size=batch_size,
            tensorboard_log=tensorboard_log,
        )

        self._save_model_path = save_model_path

    def train_model(self, total_timesteps, callback=None):
        self._model.learn(total_timesteps=total_timesteps, callback=callback)

    def save_model(self):
        self._model.save(self._save_model_path)

    def evalute_model(self, n_eval_episodes=10, render=True):
        mean_reward, std_reward = evaluate_policy(
            self._model,
            self._eval_environment,
            n_eval_episodes=n_eval_episodes,
            render=render,
        )
        print(f"Mean reward: {mean_reward} +/- {std_reward}")
        return mean_reward, std_reward

    def close_environment(self):
        self._environment.close()
        self._eval_environment.close()
