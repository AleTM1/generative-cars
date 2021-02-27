import numpy as np
import random
from math import sin, cos, radians
from shapely.geometry import Point
import copy


def rndclosestspeed(spd):
    if 4 < spd < 20:
        if random.randint(0, 1) == 0:
            spd -= 2
        else:
            spd += 2
    elif spd >= 20:
        spd -= 2
    else:
        spd += 2
    return spd


def rndclosestangle(ang):
    if -25 < ang < 25:
        if random.randint(0, 1) == 0:
            ang -= 2
        else:
            ang += 2
    elif ang >= 25:
        ang -= 2
    else:
        ang += 2
    return ang


class Car:
    def __init__(self, num_act, line_in, line_out):
        self.line_in = line_in
        self.line_out = line_out
        self.pos = [0, 0]
        self.angle = 0

        def actions_generator():
            actions = []
            spd = 0
            ang = 0
            for i in range(num_act):
                spd = rndclosestspeed(spd)
                ang = rndclosestangle(ang)
                actions.append([spd, ang])
            return np.array(actions)
        self.actions = actions_generator()

    def execute(self):
        waypoints = [[0, 0]]
        tick = 0
        lenght = 0
        for a in self.actions:
            self.update_position(a)
            point = Point(self.pos[0], self.pos[1])
            waypoints.append(copy.deepcopy(self.pos))
            if self.line_in.contains(point) or not self.line_out.contains(point):
                break
            tick += 1
            lenght += a[0]
        return np.array(waypoints), tick, lenght

    def update_position(self, action):
        self.angle += action[1]
        self.pos[0] += action[0] * cos(radians(self.angle))
        self.pos[1] += action[0] * sin(radians(self.angle))
