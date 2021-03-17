import numpy as np
import random
from math import sin, cos, radians
from shapely.geometry import Point
import copy


def rndclosestspeed(spd, min_spd, max_spd):
    a = -3
    b = +3
    if spd < min_spd:
        a = - (spd - min_spd - 2)
    elif spd > max_spd:
        b = max_spd + 2 - spd
    n_ang = spd + random.random()*(b - a) + a
    return n_ang


def rndclosestangle(ang, min_ang, max_ang):
    a = -2
    b = +2
    if ang < min_ang:
        a = min_ang - 2 - ang
    elif ang > max_ang:
        b = max_ang + 2 - ang
    n_ang = ang + random.random()*(b - a) + a
    return n_ang


class Car:

    max_spd = 15
    min_spd = 2
    max_ang = 35
    min_ang = -35

    def __init__(self, num_act, poly_in, poly_out, starting_point, starting_angle, starting_speed):
        self.line_in = poly_in
        self.line_out = poly_out
        self.starting_pos = starting_point
        self.pos = starting_point
        self.starting_ang = starting_angle
        self.starting_speed = starting_speed
        self.angle = starting_angle
        self.tick = 0
        self.actions = []
        self.actions_generator(0, num_act)

    def actions_generator(self, start, num_act):
        if start == 0:
            spd = copy.deepcopy(self.starting_speed)
            ang = 0
            actions = []
        else:
            spd = self.actions[start, 0]
            ang = self.actions[start, 1]
            actions = list(self.actions[:start])
        for i in range(start, num_act):
            spd = rndclosestspeed(spd, self.min_spd, self.max_spd)
            ang = rndclosestangle(ang, self.min_ang, self.max_ang)
            actions.append([spd, ang])
        self.actions = np.array(actions)

    def execute(self):
        self.pos = copy.deepcopy(self.starting_pos)
        self.angle = copy.deepcopy(self.starting_ang)
        self.tick = 0
        waypoints = [copy.deepcopy(self.starting_pos)]
        lenght = 0
        for a in self.actions:
            self.update_position(a)
            point = Point(self.pos[0], self.pos[1])
            if self.line_in.contains(point) or not self.line_out.contains(point):
                break
            self.tick += 1
            lenght += a[0]
            waypoints.append(copy.deepcopy(self.pos))
        return np.array(waypoints), lenght

    def update_position(self, action):
        self.angle += action[1]
        self.pos[0] += action[0] * cos(radians(self.angle))
        self.pos[1] += action[0] * sin(radians(self.angle))

    def get_angle(self, point_num):
        acc = copy.deepcopy(self.starting_ang)
        for i in range(point_num):
            acc += self.actions[i][1]
        return acc
