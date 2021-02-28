import numpy as np
import random
from math import sin, cos, radians
from shapely.geometry import Point
import copy


def rndclosestspeed(spd):
    max_spd = 20
    min_spd = 4
    a = -2
    b = +2
    if spd < min_spd:
        a = - (spd - min_spd - 2)
    elif spd > max_spd:
        b = max_spd + 2 - spd
    n_ang = spd + random.random()*(b - a) + a
    return n_ang


def rndclosestangle(ang):
    max_ang = 25
    min_ang = -25
    a = -2
    b = +2
    if ang < min_ang:
        a = min_ang - 2 - ang
    elif ang > max_ang:
        b = max_ang + 2 - ang
    n_ang = ang + random.random()*(b - a) + a
    return n_ang


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
        waypoints = [[0, 0]]
        tick = 0
        lenght = 0
        for a in self.actions:
            self.update_position(a)
            point = Point(self.pos[0], self.pos[1])
            if self.line_in.contains(point) or not self.line_out.contains(point):
                break
            tick += 1
            lenght += a[0]
            waypoints.append(copy.deepcopy(self.pos))
        self.tick = tick
        return np.array(waypoints), tick, lenght

    def update_position(self, action):
        self.angle += action[1]
        self.pos[0] += action[0] * cos(radians(self.angle))
        self.pos[1] += action[0] * sin(radians(self.angle))
