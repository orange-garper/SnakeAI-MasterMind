import os
import numpy as np
from environments.snake_environment import SnakeEnvironment
from gymnasium.wrappers import NormalizeObservation, NormalizeReward
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.ppo import MlpPolicy, CnnPolicy
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback, StopTrainingOnRewardThreshold, EvalCallback

log_path = os.path.join('logs')
ppo_path = os.path.join("models", "Snake-PPO-model")
savepoint_path = os.path.join("models", "Snake-PPO-model-SP")

mean_rewards_history = []

wrapping_env = lambda cls, **kwargs: cls(**kwargs)
env = DummyVecEnv([lambda: wrapping_env(SnakeEnvironment)])
eval_env = Monitor(SnakeEnvironment(render_mode="human"))

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
    tensorboard_log=log_path
)

checkpoint_callback = CheckpointCallback(
    save_freq=10000,
    save_path=savepoint_path,
    name_prefix="rl_model",
    save_replay_buffer=True,
    save_vecnormalize=True,
)

callback_on_best = StopTrainingOnRewardThreshold(
    reward_threshold=10, 
    verbose=1)

eval_callback = EvalCallback(
    eval_env, 
    callback_on_new_best=callback_on_best, 
    verbose=1,
    log_path=savepoint_path
)

total_timesteps = 10_000_000
log_interval = 10_000

for timestep in range(0, total_timesteps, log_interval):
    print(f"Training for {log_interval} timesteps")
    model.learn(total_timesteps=log_interval, callback=checkpoint_callback)
    print("Evaluating model")
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10, render=True)
    print(f"Timestep: {timestep}, Mean reward: {mean_reward} +/- {std_reward}")

    # Update the plot
    mean_rewards_history.append(mean_reward)

model.save(ppo_path)

print("Evaluating final model")
mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=100, render = True)
print(f"Final Mean reward: {mean_reward} +/- {std_reward}")