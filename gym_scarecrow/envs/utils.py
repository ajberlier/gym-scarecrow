import os
import math
import pygame
import numpy as np
from gym_scarecrow.envs.params import *


def get_grid(position):
    return [int(position[0] / GRID_SIZE), int(position[1] / GRID_SIZE)]


def get_distance(p1, p2):
    return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))


def check_collision(p1, p2):
    if get_distance(p1.position, p2.position) <= p1.size + p2.size:
        return True
    return False


def load_pickle(file):
    np_load_old = np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
    data = np.load(file)
    np.load = np_load_old
    return data

def set_png_icon(image_path):
    """
    sets the pygame icon with a transparent background
    :param image_path: image path to be set as the icon
    :return:
    """
    # get current path
    current_path = os.path.dirname(__file__)
    # get full image path
    full_path = os.path.join(current_path, image_path)
    # display game icon
    icon = pygame.image.load(full_path)
    # manipulate icon to look better
    # force image scale, sometime reduce of a large image looks bad
    icon = pygame.transform.scale(icon, (32, 32))
    # description of the icon surface
    surface = pygame.Surface(icon.get_size())
    # establish color key, per-pixel alpha is not supported for pygame icons
    key = (0, 255, 0)
    # fill surface with a solid color
    surface.fill(key)
    # set the transparent colorkey
    surface.set_colorkey(key)
    # draw icon back onto transparent background
    surface.blit(icon, (0, 0))

    pygame.display.set_icon(surface)