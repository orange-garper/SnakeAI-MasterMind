import os
from src.agent import SnakeAgent
from src.gym_environment import RewardParametersPack

CELL_SIZE, FIELD_SIZE = 30, (32, 18)
SAVE_MODEL_PATH = os.path.join("saved_models", "Snake_AI_Model")
LOGS_PATH = os.path.join("logs")

learning_rate = 1.1449109792768906e-05
n_steps = 2_368
gae_lambda = 0.8262347644806955
gamma = 0.8715701997208183
ent_coef = 0.0006044987571033965
clip_range = 0.12304573683415493
reward_parameters = RewardParametersPack(
    step_reward_multiplier=0.502614714123699,
    food_reward_multiplier=0.661436584433661,
    stupid_reward_multiplier=1.0174318142692036,
    death_reward_multiplier=0.5047511102044395,
    victory_reward_multiplier=0.9385566770343223,
    max_steps_reward_multiplier=1.238567707813729,
    multiply_by_length=False,
)


def main():
    agent = SnakeAgent(
        FIELD_SIZE,
        CELL_SIZE,
        save_model_path=SAVE_MODEL_PATH,
        tensorboard_log=LOGS_PATH,
        render_mode="human",
        learning_rate=learning_rate,
        n_steps=n_steps,
        gae_lambda=gae_lambda,
        gamma=gamma,
        ent_coef=ent_coef,
        clip_range=clip_range,
        reward_parameters=reward_parameters,
    )
    agent.train_model(100000)
    agent.evalute_model(10)
    agent.save_model()


if __name__ == "__main__":
    main()