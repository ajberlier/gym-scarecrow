from gym_scarecrow.envs.utils import *
from gym_scarecrow.params import *
from gym_scarecrow.envs.keepout import Keepout
from gym_scarecrow.envs.defender import *
from gym_scarecrow.envs.subject import Subject

if HARDWARE:
    from src.system.controller.python.controller_interface import ControllerInterface

import pygame


class Scarecrow2D:

    def __init__(self, is_render=True):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        # display game icon
        set_png_icon(ICON_PATH)
        self.clock = pygame.time.Clock()
        self.is_render = is_render
        # FIXME: do not draw the screen in training...
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("Arial", 50)
        self.game_speed = GAME_SPEED
        self.keepout = Keepout(self.screen)
        if HARDWARE:
            self.controller = ControllerInterface()
            self.controller.start()
            self.defender = HardwareDefender(self.screen, self.controller)
        else:
            self.defender = Defender(self.screen)
        self.prev_distance = 0
        self.cur_distance = 0
        self.subjects = [Subject(self.screen) for _ in range(SUBJECT_COUNT)]
        self.steps = 0

    def action(self, action):

        self.defender.move(action)

        # TODO: multiple defenders
        self.defender.update()
        for s in self.subjects:
            s.bounds()
            # TODO: update to multiple defenders
            s.flock(self.subjects, self.defender)
            s.update(self.defender)
        self.keepout.update(self.subjects)

        return action

    def observe(self):
        obs = []

        # grid position for defender
        d = self.defender
        obs.append(d.grid[0])
        obs.append(d.grid[1])

        # grid position for all subjects
        for s in self.subjects:
            obs.append(s.grid[0])
            obs.append(s.grid[1])

        # encode as int
        encode_obs = quinary_to_int(obs)

        # return an array of each spaces value
        return encode_obs

    # TODO: update with better reward
    def evaluate(self):

        reward = 0

        # encouraging it to stay near the keepout zone helped, small proportional penalty
        d = self.defender
        dist = abs(get_distance(d.game_position, self.keepout.position))
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
