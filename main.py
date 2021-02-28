from graphical_engine import display
from car import Car
import numpy as np
import shapely.geometry.polygon
from shapely.geometry import Polygon
import random
import copy


outer_border = np.array([[-150, 20], [150, 20], [150, -220], [-150, -220], [-150, 20]])
inner_border = np.array([[-110, -20], [110, -20], [110, -180], [-110, -180], [-110, -20]])
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    waypoints_array = []
    lenght_array = []
    for car in car_array:
        waypoints, tick, lenght = car.execute()
        lenght_array.append(lenght)
        waypoints_array.append(waypoints)
    return lenght_array, waypoints_array


def selection(lenght_array):
    population_indexes = []
    m = max(lenght_array)
    quality = 1.0
    while len(population_indexes) < int(round(0.1 * len(lenght_array))):
        population_indexes = []
        quality -= 0.05
        k = 0
        for le in lenght_array:
            if le > m * quality:
                population_indexes.append(k)
            k += 1
    return population_indexes


def crossover(best, dim, num_act):
    population = best
    n = len(best)
    while len(population) < dim:
        new_car = copy.deepcopy(random.choice(best))
        new_car.actions_generator(int(new_car.tick * 0.6), num_act)
        population.append(new_car)
    for i in range(n):
        population[i].actions_generator(int(population[i].tick * 0.9), num_act)
    return population


def main_loop(actions_num, dim):
    population = [Car(actions_num - 1, inner_poly, outer_poly) for _ in range(dim)]
    epoch = 0
    while True:
        lenght_array, waypoints_array = fitness_calculation(population)
        if max(lenght_array) > 700:
            index = 0
            for w in waypoints_array:
                if np.linalg.norm(np.array((0, 0)) - w[-1]) < 5:
                    display([waypoints_array[index]], line_in, line_out, str(epoch) + "_COMPLETE")
                    return 0
                index += 1
        selection_arr = selection(lenght_array)
        best = [population[i] for i in selection_arr]
        if epoch % 15 == 0:
            display(waypoints_array, line_in, line_out, str(epoch))
        population = copy.deepcopy(crossover(best, dim, actions_num - 1))
        epoch += 1


time = 100
population_dim = 20
main_loop(time, population_dim)
print("COMPLETE")
