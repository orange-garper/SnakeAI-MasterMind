import os
from stable_baselines3 import PPO
from environments.snake_environment import SnakeEnvironment
from stable_baselines3.common.evaluation import evaluate_policy
import sys
import numpy as np

ppo_path = os.path.join("models", "Snake-PPO-model")
env = SnakeEnvironment(render_mode="human")

model = PPO.load(ppo_path, env)

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Final Mean reward: {mean_reward} +/- {std_reward}")