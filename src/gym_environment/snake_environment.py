from numpy.typing import NDArray
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from ..snake_game import SnakeGame
from typing import Tuple, Dict, NamedTuple, Any
import cv2


class RewardParametersPack(NamedTuple):
    step_reward_multiplier: int = 1
    food_reward_multiplier: int = 1
    stupid_reward_multiplier: int = 1
    death_reward_multiplier: int = 1
    victory_reward_multiplier: int = 1
    max_steps_reward_multiplier: int = 0
    multiply_by_length: bool = False


class SnakeEnvironment(gym.Env):
    def __init__(
        self,
        field_size: Tuple[int, int] | None = None,
        cell_size: int | None = None,
        *,
        render_mode: str | None = None,
        define_params_mode: bool = False,
        reward_parameters: RewardParametersPack | None = None,
    ) -> None:
        _metadata = {"render_mode": ["human"]}

        self._field_size = field_size or (10, 10)
        self._cell_size = cell_size or 2
        self._snake_game = SnakeGame(
            field_size=self._field_size, cell_size=self._cell_size, player_mode="AI"
        )

        self.observation_space = spaces.Box(
            low=0, high=255, shape=(84, 84, 1), dtype=np.uint8
        )
        self.action_space = spaces.Discrete(4)

        assert (
            render_mode is None or render_mode in _metadata["render_mode"]
        ), f"The specified rendering mode is not provided.\
 Available render modes\
 : {', '.join(_metadata['render_mode'])}"
        self._render_mode = render_mode

        self.reward_parameters = reward_parameters or RewardParametersPack()
        self._do_max_steps = lambda field_size, lenght_size, steps: steps > (
            field_size[0] * field_size[1] * (lenght_size - 1)
        )
        self._previous_state = None
        self._define_params_mode = define_params_mode

    def _preprocess(self, observation):
        shape = self.observation_space.shape

        gray = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
        resize = cv2.resize(gray, shape[:2], cv2.INTER_CUBIC)
        channels = np.reshape(resize, shape)
        return channels

    def _get_observation(self) -> NDArray:
        current_state = self._snake_game.get_state()
        grey_state = self._preprocess(current_state)

        if self._previous_state is not None:
            state_delta = grey_state - self._previous_state
        else:
            state_delta = grey_state

        self._previous_state = grey_state
        return state_delta

    def _get_info(self) -> Dict:
        return dict(length=self._snake_game.snake_length)

    def _reward_analize(self) -> float:
        reward_for_step = (
            -0.01
            * (1, self.reward_parameters.step_reward_multiplier)[
                not self._define_params_mode
            ]
            / (1, self._snake_game.snake_length**2)[
                self.reward_parameters.multiply_by_length
                and not self._define_params_mode
            ]
        )
        reward_for_eating_fruit = (
            1
            * (1, self.reward_parameters.food_reward_multiplier)[
                not self._define_params_mode
            ]
            if self._snake_game.grown
            else 0
        )
        reward_for_stupid_move = (
            -0.1
            * (1, self.reward_parameters.stupid_reward_multiplier)[
                not self._define_params_mode
            ]
            if self._snake_game.do_stupid
            else 0
        )
        reward_for_death = (
            -1
            * (1, self.reward_parameters.death_reward_multiplier)[
                not self._define_params_mode
            ]
            if self._snake_game.game_over
            else 0
        )
        reward_for_victory = (
            float("+inf")
            * (1, self.reward_parameters.victory_reward_multiplier)[
                not self._define_params_mode
            ]
            if self._snake_game.won
            else 0
        )
        reward_for_max_steps = (
            -1
            * (1, self.reward_parameters.max_steps_reward_multiplier)[
                not self._define_params_mode
            ]
            if self._do_max_steps(
                self._field_size, self._snake_game.snake_length, self._snake_game.steps
            )
            else 0
        )

        reward = (
            sum(
                (
                    reward_for_step,
                    reward_for_eating_fruit,
                    reward_for_stupid_move,
                    reward_for_death,
                    reward_for_victory,
                    reward_for_max_steps,
                )
            )
            * (1, self._snake_game.snake_length)[
                self.reward_parameters.multiply_by_length
                and not self._define_params_mode
            ]
        )

        return reward

    def step(self, action: int) -> Tuple[NDArray, float, bool, bool, dict]:
        self._snake_game.make_action(action)
        self._snake_game.update()

        observation = self._get_observation()
        reward = self._reward_analize()
        terminated = (
            self._snake_game.game_over
            or self._snake_game.won
            or self._do_max_steps(
                self._field_size, self._snake_game.snake_length, self._snake_game.steps
            )
        )
        truncated = False
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> Tuple[NDArray, dict]:
        self._snake_game.reset()

        return self._get_observation(), self._get_info()

    def render(self) -> None:
        if self._render_mode == "human":
            self._snake_game.render()

    def close(self) -> None:
        self._snake_game.close()