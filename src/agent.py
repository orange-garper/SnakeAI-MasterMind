import os
import numpy as np
from environments.snake_environment import SnakeEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.evaluation import evaluate_policy

log_path = os.path.join('logs')
ppo_path = os.path.join("models", "Snake-PPO-model")

mean_rewards_history = []

env = DummyVecEnv([lambda: SnakeEnvironment()])

eval_env = SnakeEnvironment(render_mode="human")

learning_rate = 0.0005
n_steps = 256
gae_lambda = 0.95
gamma = 0.99
ent_coef = 0.01
clip_range = 0.2
n_epochs = 10
batch_size = 64
    
# model = PPO.load(path=ppo_path, env=env)
model = PPO(
    MlpPolicy,
    env,
    verbose=1,
    learning_rate=learning_rate,
    n_steps=n_steps,
    gae_lambda=gae_lambda,
    gamma=gamma,
    ent_coef=ent_coef,
    clip_range=clip_range,
    n_epochs=n_epochs,
    batch_size=batch_size,
)

total_timesteps = 10_000
log_interval = 10_000

for timestep in range(0, total_timesteps, log_interval):
    print(f"Training for {log_interval} timesteps")
    model.learn(total_timesteps=log_interval)
    print("Evaluating model")
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10, render =  True)
    print(f"Timestep: {timestep}, Mean reward: {mean_reward} +/- {std_reward}")

    # Update the plot
    mean_rewards_history.append(mean_reward)

model.save(ppo_path)

print("Evaluating final model")
mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10, render = True)
print(f"Final Mean reward: {mean_reward} +/- {std_reward}")