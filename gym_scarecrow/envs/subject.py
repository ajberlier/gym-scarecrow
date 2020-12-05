import math
import random
import pygame
import numpy as np
from gym_scarecrow.envs.utils import *
from gym_scarecrow.envs.params import *


class Subject:

    def __init__(self, screen):
        self.screen = screen
        self.color = SUBJECT_COLOR
        # TODO: This should be random
        self.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        # FIXME: velocity may need adjusted
        self.velocity = (np.random.rand(2)) * 10
        self.acceleration = (np.random.rand(2))
        # TODO: make these parameters
        self.max_speed = 5
        self.max_force = 0.2
        self.perception = 50
        self.spooked = False
        self.grid = get_grid(self.position)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], SUBJECT_SIZE)

    def update(self, defender):
        self.grid = get_grid(self.position)
        self.is_spooked(defender)
        self.position += self.velocity
        self.velocity += self.acceleration
        # speed limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

    def separation(self, subjects):
        avg = np.array([0, 0]).astype(float)
        total = 0
        steering_force = 0
        for s in subjects:
            dist = np.linalg.norm(self.pos - b.pos)
            # dist = distance(self.pos, b.pos)
            if s!= self and (dist < self.perception):
                diff = self.pos - b.pos
                diff /= dist
                total += 1
                avg += diff

        if total:
            avg /= total
            steering_force = avg
            if np.linalg.norm(steering_force) > 0:
                steering_force = (
                                         steering_force / np.linalg.norm(steering_force)) * self.max_speed

            steering_force -= self.velocity
            if np.linalg.norm(steering_force) > self.max_force:
                steering_force = (
                                         steering_force / np.linalg.norm(steering_force)) * (self.max_force + 0.1)

        return steering_force

    def alignment(self, subjects):
        avg = np.array([0, 0]).astype(float)
        total = 0
        steering_force = 0
        for s in subjects:
            if s!= self and (distance(self.position, b.position) < self.perception):
                total += 1
                avg += b.velocity
        if total:
            avg /= total
            # direction vector
            avg = (avg / np.linalg.norm(avg)) * self.max_speed
            steering_force = avg - self.velocity

        return steering_force

    def cohesion(self, subjects):
        avg = np.array([0, 0]).astype(float)
        total = 0
        steering_force = 0
        for s in subjects:
            if s!= self and (distance(self.pos, b.pos) < self.perception):
                total += 1
                avg += b.pos
        if total:
            mass_center = avg / total
            steering_force = mass_center - self.pos

            if np.linalg.norm(steering_force) > 0:
                steering_force = (
                                         steering_force / np.linalg.norm(steering_force)) * self.max_speed

            steering_force -= self.velocity
            if np.linalg.norm(steering_force) > self.max_force:
                steering_force = (
                                         steering_force / np.linalg.norm(steering_force)) * self.max_force

        return steering_force

    def avoidance(self, defenders):
        steering_force = np.array([0, 0]).astype(float)
        total = 0
        for d in defenders:
            # TODO: use the utils distence
            dist = np.linalg.norm(self.position - d.position)
            if dist < self.perception:
                steering_force += (self.position - d.position) / dist
                total += 1

        if total:
            steering_force /= total
            if np.linalg.norm(steering_force) > 0:
                steering_force = (steering_force / np.linalg.norm(steering_force)) * self.max_speed

            if np.linalg.norm(steering_force) > self.max_force:
                steering_force = (steering_force / np.linalg.norm(steering_force)) * self.max_force * 2

        return steering_force

    def flock(self, subjects, defenders):
        self.acceleration = np.zeros(2).astype(float)

        self.acceleration += self.alignment(subjects)
        self.acceleration += self.cohesion(subjects)
        self.acceleration += self.separation(subjects)
        self.acceleration += self.avoidance(defenders)

    def is_spooked(self, defender):
        if get_distance(defender.position, self.position) <= BLOCK_SIZE*2:
            self.spooked = True
            self.color = SPOOK_COLOR
        else:
            self.spooked = False
            self.color = SUBJECT_COLOR

    def bounds(self):
        if self.position[0] > SCREEN_WIDTH:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.ppositionos[0] = SCREEN_WIDTH

        if self.position[1] > SCREEN_HEIGHT:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = SCREEN_HEIGHT


