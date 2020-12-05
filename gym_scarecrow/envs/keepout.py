import pygame
from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *


class Keepout:

    def __init__(self, screen):
        self.screen = screen
        self.color = KEEPOUT_COLOR
        self.position = [SCREEN_WIDTH - SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 2]
        self.breached = False

    def draw(self):
        pos = self.position
        rect = [pos[0] - (pos[0] % 100) - BLOCK_SIZE * KEEPOUT_SIZE/2, pos[1] - (pos[1] % 100) - BLOCK_SIZE
                * KEEPOUT_SIZE / 2, BLOCK_SIZE * KEEPOUT_SIZE, BLOCK_SIZE * KEEPOUT_SIZE]
        pygame.draw.rect(self.screen, self.color, rect, 5)

    def update_status(self, subject):
        self.is_breached(subject)

    def is_breached(self, subject):
        if get_distance(subject.position, self.position) <= BLOCK_SIZE * KEEPOUT_SIZE:
            self.breached = True
            self.color = BREACH_COLOR
        else:
            self.breached = False
            self.color = KEEPOUT_COLOR