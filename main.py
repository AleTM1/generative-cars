from graphical_engine import display_running, display_ending
from track_loader import load_track
from car import Car
import numpy as np
import shapely.geometry.polygon
from shapely.geometry import Polygon
import random
import copy


track = 0

outer_border, inner_border = load_track(track)
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    PENALIZATION_PARAM = 8
    waypoints_array = []
    lenght_array = []
    fitness_array = []
    for c in car_array:
        waypoints, lenght = c.execute()
        lenght_array.append(lenght)
        fitness_array.append(lenght - PENALIZATION_PARAM * c.tick)
        waypoints_array.append(waypoints)
    return lenght_array, fitness_array, waypoints_array


def selection(fitness_array):
    population_indexes = []
    m = max(fitness_array)
    quality = 1.0
    while len(population_indexes) < int(round(0.1 * len(fitness_array))):
        population_indexes = []
        quality -= 0.05
        k = 0
        for le in fitness_array:
            if le > m * quality:
                population_indexes.append(k)
            k += 1
    return population_indexes


def crossover(best, dim, num_act, best_fitness):
    def heuristic_choice():
        total = int(sum(best_fitness))
        v = random.randint(1, total)
        for j in range(len(best_fitness)):
            if v - best_fitness[j] <= 0:
                return best[j]
            v -= best_fitness[j]

    population = best
    n = len(best)
    while len(population) < dim:
        new_car = copy.deepcopy(heuristic_choice())
        new_car.actions_generator(int(new_car.tick * 0.4), num_act)
        population.append(new_car)
    for i in range(n):
        population[i].actions_generator(int(population[i].tick * 0.9), num_act)
    return population


def termination(lenght_array, waypoints_array, end_point):
    for i in range(len(lenght_array)):
        if lenght_array[i] > 700:
            for p in range(int(len(waypoints_array[i])/2), len(waypoints_array[i])):
                if np.linalg.norm((waypoints_array[i][p]) - np.array(end_point)) < 4:
                    return True, i, p
    return False, -1, -1


def main_loop(actions_num, dim, sp_array, sa_array):
    while True:
        population = [Car(actions_num - 1, inner_poly, outer_poly, sp_array[0], sa_array[0]) for _ in range(dim)]
        epoch = 0
        while epoch < 300:
            lenght_array, fitness_array, waypoints_array = fitness_calculation(population)
            if max(lenght_array) > 700:
                t, index, point = termination(lenght_array, waypoints_array, sp_array[0])
                if t:
                    best_car = population[index]
                    display_ending(waypoints_array[index][:point], line_in, line_out, str(epoch), best_car)
                    return best_car
            selection_arr = selection(fitness_array)
            best = [population[i] for i in selection_arr]
            best_fitness = [fitness_array[i] for i in selection_arr]
            if epoch % 30 == 0:
                display_running(waypoints_array, line_in, line_out, str(epoch))
            population = copy.deepcopy(crossover(best, dim, actions_num - 1, best_fitness))
            epoch += 1


time = 100
population_dim = 50
starting_point = [[-30, 5]]
starting_angle = [170]
car = main_loop(time, population_dim, starting_point, starting_angle)
print("Car steps: " + str(car.tick))
print("COMPLETE")
