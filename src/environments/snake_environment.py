import numpy as np
import pygame, sys
from environments.game import CELL_NUMBER_H, CELL_NUMBER_W, CELL_SIZE, DIRECTION, SCREEN_UPDATE, Game

import gymnasium as gym
from gymnasium import spaces

WIN_FACTOR = 100
DEATH_FACTOR = 1
GROWN_FACTOR = 0.1
STUPID_DEATH_FACTOR = 2

def get_max_steps(ln_snake):
    return (CELL_NUMBER_W * CELL_NUMBER_H - (2 + ln_snake) / 2) * (ln_snake - 1)

class SnakeEnvironment(gym.Env):
    metadata = {
        "render_modes": ['human', 'human_controlling'],
        "render_fps": 60
    }

    def __init__(self, game: Game = None, render_mode = None, clock = None, ep_length = float('inf')):
        super(SnakeEnvironment, self).__init__()

        self.observation_space = spaces.Dict({
            "head": spaces.Box(low = 0, 
                                high = max((CELL_NUMBER_H, CELL_NUMBER_W)), 
                                shape = (2, ), 
                                dtype=np.float64),
            "target": spaces.Box(low = -max((CELL_NUMBER_H, CELL_NUMBER_W)), 
                                 high = max((CELL_NUMBER_H, CELL_NUMBER_W)), 
                                 shape = (2, ), 
                                 dtype = np.float64),
            "body": spaces.Box(low = 0,
                               high = max((CELL_NUMBER_H, CELL_NUMBER_W)),
                               shape = (CELL_NUMBER_H * CELL_NUMBER_W - 2, 3),
                               dtype = np.float64)
        })
            
        self.action_space = spaces.Discrete(4)

        self._action_to_direction = [move for move in DIRECTION.values()]
        self.ep_length = ep_length

        self.game = game or Game()

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.clock = clock
        self.window = None
    
    def _get_observation(self):

        #Snake coords
        _body = np.zeros(shape=(CELL_NUMBER_H * CELL_NUMBER_W - 2, 3), dtype=np.float64)

        for index, (element, _) in enumerate(zip(self.game.snake.get_coords(start_with=1), _body)):
            _body[index, 0] = element[0]
            _body[index, 1] = element[1]
            _body[index, 2] = 1
        
        _head = np.array([self.game.snake.body[0].x, self.game.snake.body[0].y])
        
        # Fruit coords
        _target = np.array([self.game.fruit.x - self.game.snake.body[0].x,
                             self.game.fruit.y - self.game.snake.body[0].y])

        return dict(head=_head, target=_target, body=_body)
    
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
        self._mistakes = 0

        observation, info = self._get_observation(), self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        
        return observation, info

    def step(self, action):
        reward = 0
        terminated = False
        self._mistakes = 0 if self.game.snake.grown else self._mistakes

        direction = self._action_to_direction[action]
        if self.game.snake.direction != self._action_to_direction[(action + 2) % 4]:
            self.game.change_direction(direction)
        else: 
            # reward -= CELL_NUMBER_H*CELL_NUMBER_W*(2 + self._score)*(self._score - 1)*STUPID_DEATH_FACTOR/2
            reward -= 100
        self.game.update()

        self._steps += 1
        self._score = self.game.get_len_snake()
        self._mistakes += (0, 1)[self.game.do_stupid_snake]

        terminated = any((self.game.check_hit(), 
                         self.game.do_win(), 
                         self._steps > get_max_steps(self._score),
                         terminated,
                         self._mistakes > 9))
        reward += + (1, -1)[self._distance < self.game.distance()]\
                  + (0, 500)[self.game.snake.grown]\
                  + (0, -1000)[self.game.check_hit()]\
                  + (0, -1000)[self._steps > get_max_steps(self._score)]\
                  + (0, -1)[self.game.do_stupid_snake]
                #  + (0, CELL_NUMBER_H*CELL_NUMBER_W*self._score*GROWN_FACTOR)[self.game.snake.grown]\
                #  - (0, CELL_NUMBER_H*CELL_NUMBER_W*(2 + self._score)*(self._score - 1)*\
                # DEATH_FACTOR/2)[self.game.check_hit()]\
                #  - (0, CELL_NUMBER_H*CELL_NUMBER_W*(2 + self._score)*(self._score - 1)*\
                # STUPID_DEATH_FACTOR/2)[self._steps > get_max_steps(self._score)]\
                #  + (0, (get_max_steps(self._score)/self._steps)*CELL_NUMBER_H* \
                #  CELL_NUMBER_W*self._score*WIN_FACTOR)[self.game.do_win()]\
                #  - (0, self._mistakes ** self._mistakes)[self.game.do_stupid_snake]
        
        observation = self._get_observation()
        info = self._get_info()
        truncated = self._steps > self.ep_length

        self._distance = self.game.distance()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, truncated, info
    
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