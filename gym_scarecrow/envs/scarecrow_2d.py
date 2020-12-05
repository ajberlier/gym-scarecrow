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
        self.subject = Subject(self.screen)
        self.is_render = is_render
        self.prev_distance = 0
        self.cur_distance = 0

    def action(self, action):
        self.prev_distance = self.cur_distance
        speed = BLOCK_SIZE

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

        self.defender.update_status()
        self.subject.update_status(self.defender)
        self.keepout.update_status(self.subject)

        self.cur_distance = get_distance(self.defender.position, self.subject.position)

    # TODO: update this with the observation feature vector on white board
    def observe(self):
        # return dif_w, dif_h
        dif_w = self.defender.grid[0] - self.subject.grid[0]
        dif_h = self.defender.grid[1] - self.subject.grid[1]
        return dif_w, dif_h

    # TODO: update with better reward
    def evaluate(self):
        reward = 0
        # TODO: if subject enters safezone, -10
        # TODO: if collision of agents, -10
        # TODO: if spooked subject, +1
        # TODO: if subject hits edge +5
        if self.cur_distance < self.prev_distance:
            reward = 1
        if self.subject.spooked:
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.game_speed += 30
                elif event.key == pygame.K_PAGEDOWN:
                    self.game_speed -= 30
                if self.game_speed < 0:
                    self.game_speed = 0
                elif self.game_speed > 150:
                    self.game_speed = 150

        self.screen.fill((100, 255, 150))

        self.keepout.draw()
        self.defender.draw()
        self.subject.draw()
        self.draw_text()
        self.draw_grid()

        pygame.display.flip()
        self.clock.tick(self.game_speed)

    def draw_grid(self):

        for w in range(int(SCREEN_WIDTH / BLOCK_SIZE)):
            pygame.draw.line(self.screen, (0, 0, 0), (w * BLOCK_SIZE, 0), (w * BLOCK_SIZE, SCREEN_HEIGHT))

        for h in range(int(SCREEN_HEIGHT / BLOCK_SIZE)):
            pygame.draw.line(self.screen, (0, 0, 0), (0, h * BLOCK_SIZE), (SCREEN_WIDTH, h * BLOCK_SIZE))

    def draw_text(self):

        if self.subject.spooked:
            text = self.font.render("Spooked!", True, SPOOK_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10)
            self.screen.blit(text, text_rect)

        if self.keepout.breached:
            text = self.font.render("Breached!", True, BREACH_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 20)
            self.screen.blit(text, text_rect)
