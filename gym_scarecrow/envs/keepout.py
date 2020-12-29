import pygame
import math
from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *


class Keepout:

    def __init__(self, screen):
        self.screen = screen
        self.color = KEEPOUT_COLOR
        self.position = [SCREEN_WIDTH - SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 2]
        self.breached = False
        self.breach_list = []
        self.breach_subjects = []
        self.grids = get_grid(self.position)

    def draw(self):
        pos = self.position
        rect = [pos[0] - (pos[0] % 100) - GRID_SIZE * KEEPOUT_SIZE / 2, pos[1] - (pos[1] % 100) - GRID_SIZE
                * KEEPOUT_SIZE / 2, GRID_SIZE * KEEPOUT_SIZE, GRID_SIZE * KEEPOUT_SIZE]
        pygame.draw.rect(self.screen, self.color, rect, 5)

    def update(self, subjects):
        self.is_breached(subjects)

    def is_breached(self, subjects):
        for s in subjects:
            breach = (s.position[0] <= self.position[0] + GRID_SIZE * KEEPOUT_SIZE / 2
                      >= s.position[0] >= self.position[0] - GRID_SIZE * KEEPOUT_SIZE / 2 and
                      s.position[1] <= self.position[1] + GRID_SIZE * KEEPOUT_SIZE / 2
                      >= s.position[1] >= self.position[1] - GRID_SIZE * KEEPOUT_SIZE / 2)
            self.breach_list.append(breach)
            if breach:
                self.breach_subjects.append(s)
        if any(breach_list):
            self.breached = True
            self.color = BREACH_COLOR
        else:
            self.breached = False
            self.color = KEEPOUT_COLOR
