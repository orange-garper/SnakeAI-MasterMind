from stable_baselines3.common.env_checker import check_env
from snake_environment import SnakeEnvironment

env = SnakeEnvironment(render_mode="human")

check_env(env)