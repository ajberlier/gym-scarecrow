import gym
from gym.utils import seeding
from gym import error, spaces, utils

from gym_scarecrow.params import *
from gym_scarecrow.envs.scarecrow_2d import Scarecrow2D

import numpy as np


class ScarecrowEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print('Game Init!')
        self.action_space = spaces.Discrete(len(ACTION_MEANING))
        # FIXME: this needs updated if extended to 3D
        # self.observation_space = spaces.Box(low=0, high=7, shape=(HEIGHT_COUNT, WIDTH_COUNT), dtype=np.uint8)
        self.observation_space = spaces.Discrete(OBS_GRID_COUNT ** (SUBJECT_COUNT + DEFENDER_COUNT))
        self.is_view = True
        self.scarecrow = None
        self.memory = []

    def reset(self):

        del self.scarecrow
        self.scarecrow = Scarecrow2D(self.is_view)
        obs = self.scarecrow.observe()
        return obs

    def step(self, action):
        self.scarecrow.action(action)
        reward = self.scarecrow.evaluate()
        done = self.scarecrow.is_done()
        obs = self.scarecrow.observe()

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        if self.is_view:
            self.scarecrow.view()

    def set_view(self, flag):
        self.is_view = flag

    def set_mode(self, mode):
        self.mode = mode

    def save_memory(self, file):
        np.save(file, self.memory)
        print("--- History Logged ---")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def make_input(self, input):
        return np.reshape(input, [1, len(input)])

    def close(self):
        pass

    def get_action_meanings(self):
        return [ACTION_MEANING[i] for i in self._action_set]



