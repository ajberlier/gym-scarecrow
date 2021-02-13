import gym
import gym_scarecrow
from gym_scarecrow.envs.scarecrow_2d import Scarecrow2D

# FIXME:!!!!!!!!!!!!!!!!
class ScarecrowRules:
    def __init__(self):
        pass

    def rules_input(self):
        # find the subject that is closest to the keepout center
        s_dist_list = []
        for s in Scarecrow2D.subjects:
            dist = abs(get_distance(s.position, Scarecrow2D.keepout.position))
            s_dist_list.append(dist)

        # get the shortest distance
        min_idx = s_dist_list.index(min(s_dist_list))
        closest_s = Scarecrow2D.subjects[min_idx]

        if min(s_dist_list) > 400 or closest_s.spooked:

            # return to center of keepout
            # grid positions
            d = Scarecrow2D.defender
            wd = d.grid[0]
            hd = d.grid[1]
            k = Scarecrow2D.keepout
            k_grid = get_grid(k.position)
            ws = k_grid[0]
            hs = k_grid[1]

            # chose the action in that direction
            if wd > ws and hd > hs:
                if abs(wd - ws) > abs(hd - hs):
                    # left
                    action = 1
                elif abs(wd - ws) < abs(hd - hs):
                    # forward
                    action = 3
                elif abs(wd - ws) == abs(hd - hs):
                    # left, there is more ground to cover in the width
                    action = 1
            elif wd > ws and hd < hs:
                if abs(wd - ws) > abs(hd - hs):
                    # left
                    action = 1
                elif abs(wd - ws) < abs(hd - hs):
                    # backward
                    action = 4
                elif abs(wd - ws) == abs(hd - hs):
                    # left, there is more ground to cover in the width
                    action = 1
            elif wd > ws and hd == hs:
                # left
                action = 1
            elif wd < ws and hd > hs:
                if abs(wd - ws) > abs(hd - hs):
                    # right
                    action = 2
                elif abs(wd - ws) < abs(hd - hs):
                    # forward
                    action = 3
                elif abs(wd - ws) == abs(hd - hs):
                    # right, there is more ground to cover in the width
                    action = 2
            elif wd < ws and hd < hs:
                if abs(wd - ws) > abs(hd - hs):
                    # right
                    action = 2
                elif abs(wd - ws) < abs(hd - hs):
                    # backward
                    action = 4
                elif abs(wd - ws) == abs(hd - hs):
                    # right, there is more ground to cover in the width
                    action = 2
            elif wd < ws and hd == hs:
                # right
                action = 2
            elif wd == ws and hd < hs:
                # backward
                action = 4
            elif wd == ws and hd > hs:
                # forward
                action = 3
            else:
                action = 0

        else:

            # grid positions
            d = Scarecrow2D.defender
            wd = d.grid[0]
            hd = d.grid[1]
            ws = closest_s.grid[0]
            hs = closest_s.grid[1]

            # chose the action in that direction
            if wd > ws and hd > hs:
                if abs(wd - ws) > abs(hd - hs):
                    # left
                    action = 1
                elif abs(wd - ws) < abs(hd - hs):
                    # forward
                    action = 3
                elif abs(wd - ws) == abs(hd - hs):
                    # left, there is more ground to cover in the width
                    action = 1
            elif wd > ws and hd < hs:
                if abs(wd - ws) > abs(hd - hs):
                    # left
                    action = 1
                elif abs(wd - ws) < abs(hd - hs):
                    # backward
                    action = 4
                elif abs(wd - ws) == abs(hd - hs):
                    # left, there is more ground to cover in the width
                    action = 1
            elif wd > ws and hd == hs:
                # left
                action = 1
            elif wd < ws and hd > hs:
                if abs(wd - ws) > abs(hd - hs):
                    # right
                    action = 2
                elif abs(wd - ws) < abs(hd - hs):
                    # forward
                    action = 3
                elif abs(wd - ws) == abs(hd - hs):
                    # right, there is more ground to cover in the width
                    action = 2
            elif wd < ws and hd < hs:
                if abs(wd - ws) > abs(hd - hs):
                    # right
                    action = 2
                elif abs(wd - ws) < abs(hd - hs):
                    # backward
                    action = 4
                elif abs(wd - ws) == abs(hd - hs):
                    # right, there is more ground to cover in the width
                    action = 2
            elif wd < ws and hd == hs:
                # right
                action = 2
            elif wd == ws and hd < hs:
                # backward
                action = 4
            elif wd == ws and hd > hs:
                # forward
                action = 3
            else:
                action = 0

            return action

    def play(self, env, obs):
        # loop for a single episode
        done = False
        while not done:
            action = self.rules_input()
            # TODO: send action to hardware

            obs, reward, done, info = env.step(action)
            env.render()
