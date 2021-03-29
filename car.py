import numpy as np
import random
from math import sin, cos, radians
from shapely.geometry import Point
import copy


class Car:

    # global parameter of Car
    max_spd = 20
    min_spd = 5
    max_ang = 35
    min_ang = -35

    def __init__(self, num_act, poly_in, poly_out, starting_point, starting_angle):
        self.poly_in = poly_in
        self.poly_out = poly_out
        self.starting_pos = starting_point
        self.pos = starting_point
        self.starting_ang = starting_angle
        self.angle = starting_angle
        self.tick = 0
        self.abs_actions = np.array([]) # Array of couples [absolute_speed, steering_angle]
        self.rel_actions = []   # Array of couples [delta_speed, delta_angle]
        self.actions_generator(num_act)  # Creating a new chromosome
        
    def actions_generator(self, num_act):
        spd = Car.min_spd
        ang = 0
        rel_actions = []
        for i in range(num_act):
            delta_spd = self.rnd_delta_speed(spd)
            delta_ang = self.rnd_delta_angle(ang)
            spd += delta_spd
            ang += delta_ang
            rel_actions.append([delta_spd, delta_ang])
        self.rel_actions = rel_actions
        self.update_abs_actions()

    def mute_rel_actions(self, start, end):
        if start < 5:
            start = 5
        spd = self.abs_actions[start - 1, 0]
        ang = self.abs_actions[start - 1, 1]
        for i in range(start, end):
            delta_spd = self.rnd_delta_speed(spd)
            delta_ang = self.rnd_delta_angle(ang)
            spd += delta_spd
            ang += delta_ang
            self.rel_actions[i][0] = copy.deepcopy(delta_spd)
            self.rel_actions[i][1] = copy.deepcopy(delta_ang)
        self.update_abs_actions()

    # In order to obtain the action (speed and steering angle) for every instant, it's computed a sum over the deltas
    def update_abs_actions(self):
        abs_actions = [[Car.min_spd, 0]]
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

    def rnd_delta_speed(self, spd):
        a = -3
        b = +3
        if spd + a < self.min_spd:
            a = spd - self.min_spd
        elif spd + b > self.max_spd:
            b = self.max_spd - spd
        n_spd = random.random()*(b - a) + a
        return n_spd    # n_spd will be between (spd-3) & (spd+3) and between the min and max Car allowed speeds

    def rnd_delta_angle(self, ang):
        a = -3
        b = +3
        if ang + a < self.min_ang:
            a = ang - self.min_ang
        elif ang + b > self.max_ang:
            b = self.max_ang - ang
        n_ang = random.random()*(b - a) + a
        return n_ang   # n_ang will be between (ang-3) & (ang+3) and between the min and max Car allowed steering angle
