import numpy as np
import random
from math import sin, cos, radians
from shapely.geometry import Point
import copy


def rndclosestspeed(spd, min_spd, max_spd):
    a = -3
    b = +3
    if spd < min_spd:
        a = - (spd - min_spd - 3)
    elif spd > max_spd:
        b = max_spd + 3 - spd
    n_spd = random.random()*(b - a) + a
    return n_spd


def rndclosestangle(ang, min_ang, max_ang):
    a = -2
    b = +2
    if ang < min_ang:
        a = min_ang - 2 - ang
    elif ang > max_ang:
        b = max_ang + 2 - ang
    n_ang = random.random()*(b - a) + a
    return n_ang


class Car:

    max_spd = 18
    min_spd = 4
    max_ang = 35
    min_ang = -35

    def __init__(self, num_act, poly_in, poly_out, starting_point, starting_angle):
        self.poly_in = poly_in
        self.poly_out = poly_out
        self.starting_pos = starting_point
        self.pos = starting_point
        self.starting_ang = starting_angle
        self.starting_speed = Car.min_spd
        self.angle = starting_angle
        self.tick = 0
        self.abs_actions = []
        self.rel_actions = []
        self.actions_generator(0, num_act)

    def actions_generator(self, start, num_act):
        if start == 0:
            spd = copy.deepcopy(self.starting_speed)
            ang = 0
            rel_actions = []
        else:
            spd = self.abs_actions[start, 0]
            ang = self.abs_actions[start, 1]
            rel_actions = list(self.rel_actions[:start])
        for i in range(start, num_act):
            delta_spd = rndclosestspeed(spd, self.min_spd, self.max_spd)
            delta_ang = rndclosestangle(ang, self.min_ang, self.max_ang)
            spd += delta_spd
            ang += delta_ang
            rel_actions.append([delta_spd, delta_ang])
        self.rel_actions = rel_actions
        self.update_abs_actions()

    def mute_rel_actions(self, start, end):
        if start < 1:
            start = 0
        spd = self.abs_actions[start - 1, 0]
        ang = self.abs_actions[start - 1, 1]
        for i in range(start, end):
            delta_spd = rndclosestspeed(spd, self.min_spd, self.max_spd)
            delta_ang = rndclosestangle(ang, self.min_ang, self.max_ang)
            spd += delta_spd
            ang += delta_ang
            self.rel_actions[i][0] = copy.deepcopy(delta_spd)
            self.rel_actions[i][1] = copy.deepcopy(delta_ang)
        self.update_abs_actions()

    def update_abs_actions(self):
        abs_actions = [[self.starting_speed, 0]]
        for i in range(0, len(self.rel_actions)):
            abs_act0 = abs_actions[i][0] + self.rel_actions[i][0]
            abs_act1 = abs_actions[i][1] + self.rel_actions[i][1]
            abs_actions.append([abs_act0, abs_act1])
        self.abs_actions = np.array(abs_actions)

    def execute(self):
        self.pos = copy.deepcopy(self.starting_pos)
        self.angle = copy.deepcopy(self.starting_ang)
        self.tick = 0
        waypoints = [copy.deepcopy(self.starting_pos)]
        for a in self.abs_actions:
            self.update_position(a)
            point = Point(self.pos[0], self.pos[1])
            if self.poly_in.contains(point) or not self.poly_out.contains(point):
                break
            self.tick += 1
            waypoints.append(copy.deepcopy(self.pos))
        return np.array(waypoints)

    def update_position(self, action):
        self.angle += action[1]
        self.pos[0] += action[0] * cos(radians(self.angle))
        self.pos[1] += action[0] * sin(radians(self.angle))
