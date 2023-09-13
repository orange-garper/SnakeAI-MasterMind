from src.gym_environment import SnakeEnvironment

CELL_SIZE, FIELD_SIZE = 30, (32, 18)

env = SnakeEnvironment(
    field_size=FIELD_SIZE, cell_size=CELL_SIZE, render_mode="human"
)
height, width, channels = env.observation_space.shape
action = env.action_space.n

episodes = 10

for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0
    while not done:
        env.render()
        action = env.action_space.sample()
        next_state, reward, done, _, info = env.step(action)
        state = next_state
        score += reward
    print(f"Episode: {episode}, Score: {score}")
env.close()
