import gym

import gym_scarecrow
from gym_scarecrow.envs.key_control import KeyControl
from gym_scarecrow.envs.scarecrow_2d import Scarecrow2D

import pygame


class ScarecrowHuman:
    def __init__(self):
        pass

    def human_input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            action = 1
        elif keys_pressed[pygame.K_RIGHT]:
            action = 2
        elif keys_pressed[pygame.K_UP]:
            action = 3
        elif keys_pressed[pygame.K_DOWN]:
            action = 4
        else:
            action = 0

        return action

    def play(self, env, obs):
        # loop for a single episode
        done = False
        while not done:
            action = self.human_input()
            obs, reward, done, info = env.step(action)
            env.render()
