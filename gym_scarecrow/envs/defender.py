import math
import random
import pygame

from gym_scarecrow.params import *
from gym_scarecrow.envs.utils import *


class Defender:
    size = 10

    def __init__(self, screen):
        self.screen = screen
        self.color = DEFENDER_COLOR
        self.position = [int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)]
        # self.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        self.grid = get_grid(self.position)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)

    def update(self):
        self.grid = get_grid(self.position)

