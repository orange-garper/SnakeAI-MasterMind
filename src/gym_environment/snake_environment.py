from numpy.typing import NDArray
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from ..snake_game import SnakeGame
from typing import Tuple, Dict, Any


class SnakeEnvironment(gym.Env):
    def __init__(
        self, field_size: Tuple[int, int], cell_size: int, render_mode: str = "human"
    ) -> None:
        _metadata = {"render_mode": ["human"]}

        self._snake_game = SnakeGame(
            field_size=field_size, cell_size=cell_size, player_mode="AI"
        )

        self.observation_space = spaces.Box(
            low=0, high=255, shape=(field_size[0], field_size[1], 3), dtype=np.uint8
        )
        self.action_space = spaces.Discrete(4)

        assert (
            render_mode in _metadata["render_mode"]
        ), f"The specified rendering mode is not provided. Available render modes : {', '.join(_metadata['render_mode'])}"
        self._render_mode = render_mode

    def _get_observation(self) -> NDArray:
        return self._snake_game.get_state()

    def _get_info(self) -> Dict:
        return dict(length=self._snake_game.get_snake_length())

    def _reward_analize(self) -> float:
        reward_for_step = -0.01
        reward_for_eating_fruit = 1 if self._snake_game.grown else 0
        reward_for_death = -1 if self._snake_game.game_over else 0
        reward_for_victory = float("+inf") if self._snake_game.won else 0

        return sum(
            (
                reward_for_step,
                reward_for_eating_fruit,
                reward_for_death,
                reward_for_victory,
            )
        )

    def step(self, action: int) -> Tuple[NDArray, float, bool, dict]:
        self._snake_game.make_action(action)
        self._snake_game.update()

        observation = self._get_observation()
        reward = self._reward_analize()
        terminated = self._snake_game.game_over or self._snake_game.won
        truncated = False
        info = self._get_info

        return observation, reward, terminated, truncated, info

    def reset(self) -> Tuple[NDArray, dict]:
        self._snake_game.reset()
        self._snake_game.init()
        return self._get_observation(), self._get_info()

    def render(self) -> None:
        if self._render_mode == "human":
            self._snake_game.render()

    def close(self) -> None:
        self._snake_game.close()
