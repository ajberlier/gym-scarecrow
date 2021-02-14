import gym
import gym.spaces

import gym_scarecrow
from gym_scarecrow.params import *
from gym_scarecrow.envs.scarecrow_env import *
from gym_scarecrow.controllers.scarecrow_q import *
from gym_scarecrow.controllers.scarecrow_rules import *
from gym_scarecrow.controllers.scarecrow_human import *
from gym_scarecrow.envs.key_control import KeyControl

import os
import numpy as np
import datetime as dt
from statistics import mean


env = gym.make("Scarecrow-v0")
# always set the seed for reproducibility and comparison of algorithms!
env.seed(1234)

# set paths to save to npy file
date = dt.datetime.now().strftime('%Y%m%d')
date_time = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
save_dir = 'controllers/logging/' + ALGORITHM + '/' + str(date_time) + '/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
os.path.abspath(save_dir)
file_name = ALGORITHM + '_history.npy'
file_path = os.path.join(save_dir, file_name)

if TRAIN:
    # save learned Q-table
    q_file_name = 'qtable.npy'
    q_file_path = os.path.join(save_dir, q_file_name)
else:
    # load learned Q-table
    save_dir = 'controllers/logging/' + ALGORITHM + '/'
    q_file_path = os.path.join(save_dir, PLAY_QTABLE)

# initialize table for Q-learning
if ALGORITHM == 'Qlearn':
    q_table = np.zeros([env.observation_space.n, env.action_space.n])

# main loop
for i in range(NUM_EPISODES):
    print('Starting Episode' + str(i))

    # load initial observation of the scene
    obs = env.reset()

    # TODO: evaluate the Human and Rules against the QLearn with same process of evaluation
    if ALGORITHM == 'Human':
        agent = ScarecrowHuman()
        agent.play(env, obs)

    elif ALGORITHM == 'Rules':
        agent = ScarecrowRules()
        agent.play(env, obs)

    elif ALGORITHM == 'Qlearn':
        agent = ScarecrowQ(i)
        if TRAIN:
            q_table = agent.train(env, obs, q_table)
        else:
            agent.play(env, obs, q_file_path)

# save memory
env.save_memory(file_path)

# save q-table
if ALGORITHM == 'Qlearn' and TRAIN:
    np.save(q_file_path, q_table)
    print("--- Q-table Logged ---")
