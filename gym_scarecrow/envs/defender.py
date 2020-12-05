import random
import math
import pygame

from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *


class Defender:
    size = 10

    def __init__(self, screen):
        self.screen = screen
        self.color = DEFENDER_COLOR
        self.position = [SCREEN_WIDTH - SCREEN_WIDTH/2, SCREEN_HEIGHT - SCREEN_HEIGHT/2]
        self.grid = get_grid(self.position)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)

    def update_status(self):
        self.grid = get_grid(self.position)

