import os
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt

from gym_scarecrow.params import *

import gym
import gym_scarecrow


class ScarecrowQ:
    def __init__(self, i):
        self.epsilon = EPSILON * EPSILON_DECAY ** i

    def train(self, env, obs, q_table):
        # loop for a single episode
        done = False
        while not done:
            # exploration vs exploitation
            if random.uniform(0, 1) < self.epsilon:
                action = env.action_space.sample()  # explore action space
            else:
                action = np.argmax(q_table[obs])  # exploit learned values

            # take action to determine next observed state
            next_obs, reward, done, info = env.step(action)

            # maintain previous Q-value for Bellman Equation
            prev_value = q_table[obs, action]
            # calculate the maximum Q-value for the next observed state
            next_max = np.max(q_table[next_obs])

            # update Q-table with Bellman Equation
            q_table[obs, action] = (1 - ALPHA) * prev_value + ALPHA * (reward + GAMMA * next_max)

            # update observation
            obs = next_obs

        print("Q-learning Algorithm: Training Complete!.\n")

        return q_table


def play(self, env, obs, date):
    # load q table
    file_name = PLAY_QTABLE
    q_table = np.load(file_name)

    # loop for a single episode
    done = False
    while not done:
        action = np.argmax(q_table[obs])  # exploit learned values
        # TODO: send action to hardware

        obs, reward, done, info = env.step(action)
        env.render()



































    # def __init__(self):
    #
    # def q_input(self, obs, action_space):
    #     self.obs = obs
    #     self.action_space = action_space
    #
    # def train(self, episodes, alpha, gamma, epsilon):
    #     # reset environment
    #     state = self.observations
    #     # reset state-action table
    #     obs_n = len(self.observations)
    #     act_n = len(self.action_space)
    #     sa_table = np.zeros([obs_n, act_n])
    #     """Training the agent"""
    #     for i in range(1, episodes + 1):
    #         epochs, penalties, reward, = 0, 0, 0
    #         done = False
    #         while not done:
    #             if random.uniform(0, 1) < epsilon:
    #                 action = random.sample(self.action_space, 1)  # Explore action space
    #             else:
    #                 action = np.argmax(sa_table[state])  # Exploit learned values
    #             next_state, reward, done, info = env.step(
    #                 action)  # TODO: how do we want to handle stepping through the sim?
    #             old_value = sa_table[state, action]
    #             next_max = np.max(sa_table[next_state])
    #             new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
    #             sa_table[state, action] = new_value
    #             if reward == -10:
    #                 penalties += 1
    #             state = next_state
    #             epochs += 1
    #         if i % 100 == 0:
    #             clear_output(wait=True)
    #             print(f"Episode: {i}")
    #             # save table
    #         np.save('sa_table', sa_table)
    #     print("Training finished.\n")
    #
    # def agent_eval(self, episodes):
    #     """Evaluate agent's performance after Q-learning"""
    #     sa_table = np.load('sa_table.npy')
    #     total_epochs, total_penalties, total_reward = 0, 0, 0
    #     for _ in range(episodes):
    #         state = self.observations
    #         epochs, penalties, reward = 0, 0, 0
    #         done = False
    #         while not done:
    #             action = np.argmax(sa_table[state])
    #             obs, reward, done, info = env.step(action)
    #             if reward == -10:
    #                 penalties += 1
    #             epochs += 1
    #         total_reward += reward
    #         total_penalties += penalties
    #         total_epochs += epochs
    #     print(f"Results after {episodes} episodes:")
    #     print(f"- Average reward per episode: {total_reward / episodes}")
    #     print(f"- Average reward per move: {total_reward / total_epochs}")
    #     print(f"- Average timesteps per episode: {total_epochs / episodes}")
    #     print(f"- Average penalties per episode: {total_penalties / episodes}")
    #
    # # TODO:
    # def Run(self):
    #     # TODO: add logic to choose most recent saved table for the chosen algorithm or another one
    #     #    for now i am just going to overwrite all previous trained tables
    #     sa_table = np.load('sa_table.npy')
    #     state = self.observations
    #     action = np.argmax(sa_table[state])
    #     return action
    #
    # def get_output(self):
    #     return []
    #
