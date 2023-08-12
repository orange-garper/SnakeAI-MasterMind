import numpy as np
import game, pygame, sys
from game import CELL_NUMBER_H, CELL_NUMBER_W, CELL_SIZE, DIRECTION, SCREEN_UPDATE

import gymnasium as gym
from gymnasium import spaces

def get_max_steps(ln_snake):
    return CELL_NUMBER_H * ln_snake * CELL_NUMBER_W - (ln_snake ** 2 + ln_snake) / 2 - 2 * CELL_NUMBER_H * CELL_NUMBER_W + 3

class SnakeEnvironment(gym.Env):
    metadata = {
        "render_modes": ['human'],
        "render_fps": 60
    }

    def __init__(self, game: game.Game, render_mode = None, clock = None):

        self.observation_space = spaces.Box(
            low = np.zeros((CELL_NUMBER_W, CELL_NUMBER_H)),
            high = np.full((CELL_NUMBER_W, CELL_NUMBER_H), 2),
            shape = (CELL_NUMBER_W, CELL_NUMBER_H),
            dtype = np.integer
        )

        self.action_space = spaces.Discrete(4)

        self._action_to_diretion = [move for move in DIRECTION.values()]

        self.game = game

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.clock = clock
        self.window = None
    
    def _get_observation(self):
        ...

    def _get_info(self):
        ...
    
    def reset(self, seed = None, options = None):
        super().reset(seed=seed)

        self.game.reset()
        self._distance = self.game.distance()
        self._steps = 0
        observation, info = self._get_observation, self._get_info

        if self.render_mode == "human":
            self.render()
        
        return observation, info

    def step(self, action):
        direction = self._action_to_direction[action]
        self.game.change_direction(direction)
        self.game.update()

        self._steps += 1
        self._score = self.game.get_len_snake()

        terminated = self.game.check_hit() or self.game.do_win()
        
        reward_for_grown = 10 * self.game.get_len_snake() if self.game.snake.grown else 0
        reward_for_move = 1 if self._distance < self.game.distance() else -1
        reward_for_win = (1 / (self._steps / get_max_steps(self._score)) ** 2) * (CELL_NUMBER_H * CELL_NUMBER_W) * self._score if terminated else 0
        reward = sum((reward_for_grown, reward_for_move, reward_for_win))

        observation = self._get_observation()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, info

    def render(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER_W, CELL_SIZE * CELL_NUMBER_H))
        
        if self.clock is None or self.render_mode == "human":
            self.clock = pygame.time.Clock()
        
        pygame.time.set_timer(SCREEN_UPDATE, 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
        self.window.fill((0, 0, 0))
        self.game.render(self.window)
        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])
    
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()