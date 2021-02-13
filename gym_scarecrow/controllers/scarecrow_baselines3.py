import gym
import gym.spaces
import gym_scarecrow
from gym_scarecrow.params import *
from gym_scarecrow.envs.key_control import KeyControl

from stable_baselines3 import DQN, PPO
from stable_baselines3.common.monitor import Monitor

import numpy as np
from datetime import date


env = gym.make("Scarecrow-v0")
# always set the seed for reproducibility!
env.seed(1234)


if ALGORITHM == 'Human':
    obs = env.reset()
    while True:
        action = env.scarecrow.human_input()
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()

elif ALGORITHM == 'Rules':
    obs = env.reset()
    while True:
        action = env.scarecrow.rule_input()
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()

elif ALGORITHM == 'Qlearn':
    obs = env.reset()
    while True:
        action = env.scarecrow.q_input()


else:

    # this is added to include monitoring of things like average reward
    date_today = date.today().strftime("%m-%d-%Y")
    model_name = date_today + '_' + ALGORITHM + '_scarecrow'
    log_name = model_name + '_tb_log'
    log_dir = './' + ALGORITHM + '_scarecrow_tensorboard/'
    env = Monitor(env, log_dir)

    if TRAIN:
        if ALGORITHM == 'DQN':
            from stable_baselines3.dqn import MlpPolicy
            model = DQN(CnnPolicy, env, learning_rate=0.0001, buffer_size=1000000, learning_starts=50000,
                        batch_size=BATCH_SIZE, tau=SOFT_UPDATE, gamma=DISCOUNT_FACTOR, train_freq=4, gradient_steps=1,
                        n_episodes_rollout=- 1, optimize_memory_usage=False, target_update_interval=10000,
                        exploration_fraction=0.5, exploration_initial_eps=1.0, exploration_final_eps=0.05,
                        max_grad_norm=10, tensorboard_log=log_dir, create_eval_env=False, policy_kwargs=None, verbose=2,
                        seed=None, device='cuda', _init_setup_model=True)
            model.learn(total_timesteps=NUM_EPISODES*MAX_STEPS, tb_log_name=log_name, log_interval=1)
            model.save(model_name)

        if ALGORITHM == 'PPO':
            from stable_baselines3.ppo import MlpPolicy
            model = PPO(MlpPolicy, env, tensorboard_log=log_dir, verbose=2)
            model.learn(total_timesteps=NUM_EPISODES*MAX_STEPS, tb_log_name=log_name, log_interval=1)
            model.save(model_name)

        else:
            print('!ERROR: incorrect algorithm selection!')

        del model

    else:
        model_name = '02-08-2021_' + ALGORITHM + '_scarecrow'

        if ALGORITHM == 'DQN':
            model = DQN.load(model_name)
        if ALGORITHM == 'PPO':
            model = PPO.load(model_name)

        obs = env.reset()
        while True:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
            if done:
              obs = env.reset()
