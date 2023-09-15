from ..gym_environment import SnakeEnvironment, RewardParametersPack
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import CnnPolicy
from stable_baselines3 import PPO


class SnakeAgent:
    def __init__(
        self,
        field_size: int | None = None,
        cell_size: int | None = None,
        *,
        save_model_path: str | None = None,
        tensorboard_log=None,
        render_mode: str | None = "human",
        verbose: int = 1,
        learning_rate=0.0005,
        n_steps=256,
        gae_lambda=0.95,
        gamma=0.99,
        ent_coef=0.01,
        clip_range=0.2,
        n_epochs=10,
        batch_size=64,
        model: PPO | None = None,
        env=None,
        reward_parameters: RewardParametersPack | None = None,
    ):
        if env is None:
            (
                self._environment,
                self._eval_environment,
            ) = self._generate_environment(
                field_size,
                cell_size,
                render_mode,
                reward_parameters,
            )
        else:
            self._environment, self._environment = env, Monitor(env)

        if model is None:
            self._model = self._generate_model(
                verbose,
                learning_rate,
                n_steps,
                gae_lambda,
                gamma,
                ent_coef,
                clip_range,
                n_epochs,
                batch_size,
                tensorboard_log,
            )
        else:
            self._model = model
        self._save_model_path = save_model_path

    def _generate_environment(
        self,
        field_size,
        cell_size,
        render_mode,
        reward_parameters,
    ):
        environment = VecFrameStack(
            DummyVecEnv(
                [
                    lambda: SnakeEnvironment(
                        field_size,
                        cell_size,
                        render_mode=None,
                        reward_parameters=reward_parameters,
                    )
                ]
            ),
            4,
            channels_order="last",
        )
        eval_environment = VecFrameStack(
            DummyVecEnv(
                [
                    lambda: Monitor(
                        SnakeEnvironment(
                            field_size,
                            cell_size,
                            render_mode=render_mode,
                            reward_parameters=reward_parameters,
                        )
                    )
                ]
            ),
            4,
            channels_order="last",
        )
        return environment, eval_environment

    def _generate_model(
        self,
        verbose,
        learning_rate,
        n_steps,
        gae_lambda,
        gamma,
        ent_coef,
        clip_range,
        n_epochs,
        batch_size,
        tensorboard_log,
    ):
        model = PPO(
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

        return model

    def train_model(self, total_timesteps, callback=None):
        self._model.learn(total_timesteps=total_timesteps, callback=callback)

    @classmethod
    def load_model(
        cls, path: str, field_size: int | None = None, cell_size: int | None = None
    ):
        model = PPO.load(path)
        env = model.get_env()
        return cls(
            field_size=field_size,
            cell_size=cell_size,
            model=model,
            env=env,
            save_model_path=path,
        )

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