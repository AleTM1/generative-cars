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
        self.tick = 0
        self.actions = []
        self.actions_generator(0, num_act)

    def actions_generator(self, start, num_act):
        if start == 0:
            spd = 0
            ang = 0
            actions = []
        else:
            spd = self.actions[start, 0]
            ang = self.actions[start, 1]
            actions = list(self.actions[:start])
        for i in range(start, num_act):
            spd = rndclosestspeed(spd)
            ang = rndclosestangle(ang)
            actions.append([spd, ang])
        self.actions = np.array(actions)

    def execute(self):
        self.pos = [0, 0]
        self.angle = 0
        self.tick = 0
        waypoints = [self.pos]
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
        self.tick = tick
        return np.array(waypoints), tick, lenght

    def update_position(self, action):
        self.angle += action[1]
        self.pos[0] += action[0] * cos(radians(self.angle))
        self.pos[1] += action[0] * sin(radians(self.angle))
