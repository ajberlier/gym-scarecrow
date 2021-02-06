import gym
import gym_scarecrow
from gym_scarecrow.envs.scarecrow_2d import Scarecrow2D

from gym_scarecrow.envs.key_control import KeyControl

env = gym.make("Scarecrow-v0")
obs = env.reset()
while True:
    action = env.scarecrow.human_input()
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
