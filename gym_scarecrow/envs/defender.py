import math
import random
import pygame

from gym_scarecrow.params import *
from gym_scarecrow.envs.utils import *

from src.system.controller.python.controller_interface import Agent


class Defender:
    size = 10

    def __init__(self, screen):
        self.screen = screen
        self.color = DEFENDER_COLOR
        self.game_position = START_POSITION
        self.grid = get_grid(self.game_position)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.game_position[0]), int(self.game_position[1])], self.size)

    def update(self):
        self.grid = get_grid(self.game_position)

    def move(self, action):
        speed = GRID_SIZE

        # still
        if action == 0:
            pass
        # left
        elif action == 1:
            self.game_position[0] -= speed
            if self.game_position[0] < 30:
                self.game_position[0] = 30
        # right
        elif action == 2:
            self.game_position[0] += speed
            if self.game_position[0] > 1170:
                self.game_position[0] = 1170
        # up
        elif action == 3:
            self.game_position[1] -= speed
            if self.game_position[1] < 30:
                self.game_position[1] = 30
        # down
        elif action == 4:
            self.game_position[1] += speed
            if self.game_position[1] > 770:
                self.game_position[1] = 770


class HardwareDefender(Defender):

    def __init__(self, screen, controller):
        Defender.__init__(self, screen)
        self.controller = controller
        self.my_agent = None
        self.controller.register_new_agent_location_callback(self.update_location)

    def update_location(self, new_agent_location):
        self.my_agent = new_agent_location

        # convert unit between hardware and game
        # hardware_position = (self.game_position - START_POSITION)/GRID_SIZE
        self.game_position = list(GRID_SIZE * np.array(list(self.my_agent.get_location())[:2]) + np.array(START_POSITION))

    def move(self, action):
        # get agents
        if len(self.controller.get_my_agents()) == 0:
            return
        agent_id = max(self.controller.get_my_agents())
        agents = self.controller.get_agents()
        if agent_id in agents:
            my_agent = agents[agent_id]
        # get current position
        x, y, z = my_agent.get_location()
        self.my_agent = my_agent
        # set position based on action taken
        if action == 1:  # left
            y += -STEP_DISTANCE
        elif action == 2:  # right
            y += STEP_DISTANCE
        elif action == 3:  # forward
            x += STEP_DISTANCE
        elif action == 4:  # backward
            x += -STEP_DISTANCE
        else:
            return

        x = float(x)
        y = float(y)
        z = float(z)

        # Update the struct
        agent_cmd = Agent()
        agent_cmd.set_id(agent_id)
        agent_cmd.update(
            0,  # Ignored by sender code - ID setting not required
            (0, 0, 0),  # not used (current position)
            (x, y, z)  # Target location
        )

        self.controller.command_agent_location(agent_cmd)

        # prevent more than 10 Hz update
