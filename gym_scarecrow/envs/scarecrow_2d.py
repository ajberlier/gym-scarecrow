import pygame
import math
import numpy as np
from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *
from gym_scarecrow.envs.key_control import *
from gym_scarecrow.envs.keepout import Keepout
from gym_scarecrow.envs.defender import Defender
from gym_scarecrow.envs.subject import Subject


class Scarecrow2D:

    def __init__(self, is_render=True):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        # display game icon
        set_png_icon(ICON_PATH)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("Arial", 50)
        self.game_speed = GAME_SPEED
        self.keepout = Keepout(self.screen)
        self.defender = Defender(self.screen)
        self.is_render = is_render
        self.prev_distance = 0
        self.cur_distance = 0
        self.subjects = [Subject(self.screen) for _ in range(SUBJECT_COUNT)]
        self.steps = 0

    def action(self, action):
        speed = GRID_SIZE
        # still
        if action == 0:
            pass
        # left
        if action == 1:
            self.defender.position[0] -= speed
            if self.defender.position[0] < 30:
                self.defender.position[0] = 30
        # right
        elif action == 2:
            self.defender.position[0] += speed
            if self.defender.position[0] > 1170:
                self.defender.position[0] = 1170
        # up
        elif action == 3:
            self.defender.position[1] -= speed
            if self.defender.position[1] < 30:
                self.defender.position[1] = 30
        # down
        elif action == 4:
            self.defender.position[1] += speed
            if self.defender.position[1] > 770:
                self.defender.position[1] = 770

        # TODO: multiple defenders
        self.defender.update()
        for s in self.subjects:
            s.bounds()
            # TODO: update to multiple defenders
            s.flock(self.subjects, self.defender)
            s.update(self.defender)
        self.keepout.update(self.subjects)

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

    def observe(self):
        """
        0: empty field (green space)
        1: defender only (blue space)
        2: subject only (red space)
        3: keepout area only (black space)
        4: keepout area and defender (black and blue space)
        5: keepout area and subject (black and red space --> breached!)
        6: defender and subject (red and blue space --> spooked!)
        7: keepout area and defender and subject (black, blue, and red space --> breached! spooked!)
        """
        sub_idx = []
        def_idx = []
        keepout_idx = []

        # set every grid to empty field 0: empty field (green space)
        obs = [0]*GRID_COUNT

        # check 1: defender only (blue space)
        # TODO: update for multiple defenders
        # for d in defenders:
        d = self.defender
        def_idx.append(int(WIDTH_COUNT * (d.grid[1] - 1) + d.grid[0]) - 1)
        # set every defender index to 1: defender only (blue space)
        for idx in def_idx:
            obs[idx] = 1

        # 2: subject only (red space)
        # subject grids
        for s in self.subjects:
            sub_idx.append(int(WIDTH_COUNT * (s.grid[1] - 1) + s.grid[0]) - 1)
        # set every sub_idx to 2: subject only (red space)
        for idx in sub_idx:
            if obs[idx] == 0:
                obs[idx] = 2
            # check 6: defender and subject (red and blue space --> spooked!)
            elif obs[idx] == 1:
                obs[idx] = 6
            elif obs[idx] == 2 or obs[idx] == 6:
                pass
            else:
                print('Subject observation ERROR!')
                print(obs[idx])

        # check 3: keepout area only (black space)
        k = self.keepout
        for i in k.grids:
            keepout_idx.append(int(WIDTH_COUNT * (i[1] - 1) + i[0]) - 1)

        for idx in keepout_idx:
            if obs[idx] == 0:
                obs[idx] = 3
            # check 4: keepout area and defender (black and blue space)
            elif obs[idx] == 1:
                obs[idx] = 4
            # 5: keepout area and subject (black and red space --> breached!)
            elif obs[idx] == 2:
                obs[idx] = 5
            # 7: keepout area and defender and subject (black, blue, and red space --> breached! spooked!)
            elif obs[idx] == 6:
                obs[idx] = 7
            else:
                print('Keepout observation ERROR!')

        # just checking my observation is correct
        obs_array = np.reshape(np.asarray(obs), (HEIGHT_COUNT, WIDTH_COUNT))

        # return an array of each spaces value
        return obs_array

    # TODO: update with better reward
    def evaluate(self):

        reward = 0

        # encouraging it to stay near the keepout zone helped, small proportional penalty
        d = self.defender
        dist = abs(get_distance(d.position, self.keepout.position))
        # reward = -dist / SCREEN_WIDTH

        # if spooked subject, + 1
        for s in self.subjects:
            if s.spooked:
                reward += 2 * (1 - dist / SCREEN_WIDTH)

        # if subject enters safezone, -10
        if self.keepout.breached:
            reward += -10

        # TODO (when we have multiple agents): if collision of agents, -10


        return reward

    #TODO: Update for infinite horizon
    def is_done(self):
        self.steps += 1
        if self.steps >= MAX_STEPS:
            return True
        return False

    def view(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True

        self.screen.fill((100, 255, 150))

        self.keepout.draw()
        self.defender.draw()
        for s in self.subjects:
            s.draw()
            self.draw_text(s)
        self.draw_grid()

        pygame.display.flip()
        self.clock.tick(self.game_speed)

    def draw_grid(self):

        for w in range(int(SCREEN_WIDTH / GRID_SIZE)):
            pygame.draw.line(self.screen, (0, 0, 0), (w * GRID_SIZE, 0), (w * GRID_SIZE, SCREEN_HEIGHT))

        for h in range(int(SCREEN_HEIGHT / GRID_SIZE)):
            pygame.draw.line(self.screen, (0, 0, 0), (0, h * GRID_SIZE), (SCREEN_WIDTH, h * GRID_SIZE))

    def draw_text(self, s):
        if s.spooked:
            text = self.font.render("Spooked!", True, SPOOK_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10)
            self.screen.blit(text, text_rect)

        if self.keepout.breached:
            text = self.font.render("Breached!", True, BREACH_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 20)
            self.screen.blit(text, text_rect)
