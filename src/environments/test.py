from stable_baselines3.common.env_checker import check_env
from gymnasium.wrappers import NormalizeReward, NormalizeObservation
from snake_environment import SnakeEnvironment
from game import DIRECTION
import pygame

env = SnakeEnvironment(render_mode="human")

obs, info = env.reset()
while True:
    env.render()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            action = next((i for (key, value), i in zip(DIRECTION.items(), range(4))
                          if getattr(pygame, key) == event.key), None)
            if action is not None:
                obs, reward, terminated, truncated, info = env.step(action)
                print(obs)
                if terminated: env.reset()