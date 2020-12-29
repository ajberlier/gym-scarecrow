import sys
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from gym_scarecrow.envs.params import *

# gym
import gym
import gym_scarecrow

# TODO: clean up this whole file

def simulate():
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)
    total_reward = 0
    total_rewards = []
    training_done = False
    threshold = 1000
    env.set_view(True)
    for episode in range(NUM_EPISODES):

        total_rewards.append(total_reward)
        if episode == 30000:
            env.save_memory('30000')
            plt.plot(total_rewards)
            plt.ylabel('rewards')
            plt.show()
            break

        obv = env.reset()
        state_0 = obv
        total_reward = 0

        if episode >= threshold:
            explore_rate = 0.01

        for t in range(MAX_T):
            action = select_action(state_0, explore_rate)
            obv, reward, done, _ = env.step(action)
            state = obv
            env.remember(state_0, action, reward, state, done)
            total_reward += reward

            # Update the Q based on the result
            best_q = np.amax(q_table[state])
            q_table[state_0 + action] += learning_rate * (reward + DISCOUNT_FACTOR * best_q - q_table[state_0 + action])

            # Setting up for the next iteration
            state_0 = state
            env.render()
            if done or t >= MAX_T - 1:
                print("Episode %d finished after %i time steps with total reward = %f."
                      % (episode, t, total_reward))
                break
        # Update parameters
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)


def load_and_play():
    print("Start loading history")
    # history_list = ['history_left_bottom.npy','history_left_up.npy',
    #        'history_right_bottom.npy','history_right_up.npy']
    history_list = ['30000.npy']

    # load data from history file
    print("Start updating q_table")
    DISCOUNT_FACTOR = 0.99
    for list in history_list:
        history = load_data(list)
        learning_rate = get_learning_rate(0)
        print(list)
        file_size = len(history)
        print("file size : " + str(file_size))
        i = 0
        for data in history:
            state_0, action, reward, state, done = data
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + DISCOUNT_FACTOR * best_q - q_table[state_0 + (action,)])
            if done:
                i += 1
                learning_rate = get_learning_rate(i)

    print("Updating q_table is complete")

    # play game
    for episode in range(NUM_EPISODES):
        obv = env.reset()
        state_0 = state_to_bucket(obv)
        total_reward = 0
        for t in range(MAX_T):
            action = select_action(state_0, 0.01)
            obv, reward, done, _ = env.step(action)
            state = state_to_bucket(obv)
            state_0 = state
            total_reward += reward
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + DISCOUNT_FACTOR * best_q - q_table[state_0 + (action,)])
            env.render()
            if done or t >= MAX_T - 1:
                print("Episode %d finished after %i time steps with total reward = %f."
                      % (episode, t, total_reward))
                break

        learning_rate = get_learning_rate(i + episode)


def select_action(state, explore_rate):
    if random.random() < explore_rate:
        action = env.action_space.sample()
    else:
        action = int(np.argmax(q_table[state]))
    return action


def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t + 1) / DECAY_FACTOR)))


def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t + 1) / DECAY_FACTOR)))


def load_data(file):
    np_load_old = np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
    data = np.load(file)
    np.load = np_load_old
    return data


if __name__ == "__main__":
    env = gym.make("Scarecrow-v0")

    NUM_ACTIONS = env.action_space.n
    NUM_OBS = env.observation_space.n

    q_table = np.zeros((GRID_COUNT,) + (NUM_ACTIONS,), dtype=float)
    simulate()
    # load_and_play()
