import numpy as np
import pygame, sys
from game import CELL_NUMBER_H, CELL_NUMBER_W, CELL_SIZE, DIRECTION, SCREEN_UPDATE, Game

import gymnasium as gym
from gymnasium import spaces

SCORE_CONST = 0.1
DEATH_FACTOR = 0.1
GROWN_CONST = 0.4

def get_max_steps(ln_snake):
    return (CELL_NUMBER_W * CELL_NUMBER_H - (2 + ln_snake) / 2) * (ln_snake - 1)

class SnakeEnvironment(gym.Env):
    metadata = {
        "render_modes": ['human', 'rgb_array'],
        "render_fps": 60
    }

    def __init__(self, game: Game = None, render_mode = None, clock = None):
        super(SnakeEnvironment, self).__init__()

        self.observation_space = spaces.Box(
            low = np.zeros((CELL_NUMBER_W, CELL_NUMBER_H, 3)),
            high = np.full((CELL_NUMBER_W, CELL_NUMBER_H, 3), 1),
            shape = (CELL_NUMBER_W, CELL_NUMBER_H, 3),
            dtype=np.float32
        )

        self.action_space = spaces.Discrete(4)

        self._action_to_direction = [move for move in DIRECTION.values()]

        self.game = game or Game()

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.clock = clock
        self.window = None
    
    def _get_observation(self):
        _obs = np.zeros((CELL_NUMBER_W, CELL_NUMBER_H, 3), dtype=np.float32)

        _obs[self.game.fruit.x, self.game.fruit.y, 2] = 1

        for point in self.game.snake.get_coords():
            if 0 <= point[0] <= CELL_NUMBER_W - 1 and 0 <= point[1] <= CELL_NUMBER_H - 1:
                _ = point == (self.game.snake.body[0].x, self.game.snake.body[0].y)
                _obs[int(point[0]), int(point[1]), _] = 1

        return _obs
    
    def _get_info(self):
        return dict(
            score = self._score,
        )
    
    def reset(self, seed = None, options = None):
        super().reset(seed=seed, options=options)

        self.game.reset()
        self._distance = self.game.distance()
        self._steps = 0
        self._score = 0

        observation, info = self._get_observation(), self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        
        return observation, info

    def step(self, action):
        direction = self._action_to_direction[action]
        self.game.change_direction(direction)
        self.game.update()

        self._steps += 1
        self._score = self.game.get_len_snake()
        self._distance = self.game.distance()

        terminated = self.game.check_hit() or self.game.do_win()
        reward = 5

        observation = self._get_observation()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
    
    def render(self):
        return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER_W, CELL_SIZE * CELL_NUMBER_H))
        
        if self.clock is None or self.render_mode == "human":
            self.clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
        
        if self.render_mode == "human":
            self.window.fill((0, 0, 0))
            self.game.render(self.window)
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])
    
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()