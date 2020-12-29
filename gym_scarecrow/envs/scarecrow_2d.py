import pygame
import math
from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *
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

    def action(self, action):
        speed = GRID_SIZE

        if action == 0:
            self.defender.position[0] -= speed
            if self.defender.position[0] < 30:
                self.defender.position[0] = 30
        elif action == 1:
            self.defender.position[0] += speed
            if self.defender.position[0] > 1170:
                self.defender.position[0] = 1170
        elif action == 2:
            self.defender.position[1] -= speed
            if self.defender.position[1] < 30:
                self.defender.position[1] = 30
        elif action == 3:
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
        grid_width = SCREEN_WIDTH / GRID_SIZE
        sub_idx = []
        def_idx = []
        keepout_idx = []

        # set every grid to empty field 0: empty field (green space)
        obs = [0]*GRID_COUNT

        # subject grids
        for s in self.subjects:
            sub_idx.append(grid_width*s.grid[0]+s.grid[1])

        #

        # TODO: update for multiple defenders
        # for d in defenders:
        d = self.defender
        def_idx.append(grid_width*d.grid[0]+d.grid[1])
        for idx in def_idx:
            obs[idx] = 2

        # check 3: keepout area only (black space)
        for i in range(KEEPOUT_SIZE*2):
            for j in range(KEEPOUT_SIZE*2):
                keepout_idx.append(grid_width*(self.keepout.grid[0]-KEEPOUT_SIZE+i)+(self.keepout.grid[1]-KEEPOUT_SIZE+j))
        for idx in keepout_idx:
            obs[idx] = 3

        # check 4


        # check 5

        # check 6

        # check 7

        print(obs)

        # return an array of each spaces value
        return obs

    # TODO: update with better reward
    def evaluate(self):
        reward = 0
        # TODO: if subject enters safezone, -10
        # TODO: if collision of agents, -10
        # TODO: if spooked subject, +1
        # TODO: if subject hits edge +5
        if self.cur_distance < self.prev_distance:
            reward = 1
        for s in self.subjects:
            if s.spooked:
                reward = 1000
        return reward

    #TODO: Update for infinite horizon
    def is_done(self):
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
