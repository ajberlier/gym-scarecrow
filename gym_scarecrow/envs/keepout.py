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
        self.grids = []
        pos = self.position
        left_top = get_grid([pos[0] - (pos[0] % 100) - GRID_SIZE * KEEPOUT_SIZE / 2, pos[1] -
                             (pos[1] % 100) - GRID_SIZE * KEEPOUT_SIZE / 2])
        for i in range(KEEPOUT_SIZE):
            for j in range(KEEPOUT_SIZE):
                self.grids.append([left_top[0] + i, left_top[1] + j])

    def draw(self):
        pos = self.position
        rect = [pos[0] - (pos[0] % 100) - GRID_SIZE * KEEPOUT_SIZE / 2, pos[1] - (pos[1] % 100) - GRID_SIZE
                * KEEPOUT_SIZE / 2, GRID_SIZE * KEEPOUT_SIZE, GRID_SIZE * KEEPOUT_SIZE]
        pygame.draw.rect(self.screen, self.color, rect, 5)

    def update(self, subjects):
        self.is_breached(subjects)

    def is_breached(self, subjects):
        breach_list = []
        breach_subjects = []
        for s in subjects:
            breach = (s.position[0] <= self.position[0] + GRID_SIZE * KEEPOUT_SIZE / 2
                      >= s.position[0] >= self.position[0] - GRID_SIZE * KEEPOUT_SIZE / 2 and
                      s.position[1] <= self.position[1] + GRID_SIZE * KEEPOUT_SIZE / 2
                      >= s.position[1] >= self.position[1] - GRID_SIZE * KEEPOUT_SIZE / 2)
            breach_list.append(breach)
            if breach:
                breach_subjects.append(s)
        if any(breach_list):
            self.breached = True
            self.color = BREACH_COLOR
        else:
            self.breached = False
            self.color = KEEPOUT_COLOR
