import numpy as np

# gym
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_scarecrow.envs.scarecrow_2d import Scarecrow2D


class ScarecrowEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print('Game Init!')
        # 0:left, 1:right, 2:up, 3:down
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.array([-12, -8, 0]), np.array([12, 8, 120]), dtype=np.int)
        self.is_view = True
        self.scarecrow = Scarecrow2D(self.is_view)
        self.mode = 0
        self.memory = []

    def reset(self):

        del self.scarecrow
        if self.mode == 0:
            self.scarecrow = Scarecrow2D(self.is_view)
        else:
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
        print("history saved")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def make_input(self, input):
        return np.reshape(input, [1, len(input)])

    def close(self):
        pass
