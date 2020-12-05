import random
import math
import pygame
from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *


class Subject:

    def __init__(self, screen):
        self.screen = screen
        self.color = SUBJECT_COLOR
        self.position = [SCREEN_WIDTH - SCREEN_WIDTH/2, SCREEN_HEIGHT - SCREEN_HEIGHT/2]
        self.spooked = False
        self.grid = get_grid(self.position)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], SUBJECT_SIZE)

    def update_status(self, defender):
        self.grid = get_grid(self.position)
        self.is_spooked(defender)

    def is_spooked(self, defender):
        if get_distance(defender.position, self.position) <= BLOCK_SIZE*2:
            self.spooked = True
            self.color = SPOOK_COLOR
        else:
            self.spooked = False
            self.color = SUBJECT_COLOR
