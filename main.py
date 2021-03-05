from graphical_engine import display_running, display_ending
from car import Car
import numpy as np
import shapely.geometry.polygon
from shapely.geometry import Polygon
import random
import copy
import threading


outer_border = np.array([[-150, 20], [150, 20], [150, -220], [-150, -220], [-150, 20]])
inner_border = np.array([[-110, -20], [110, -20], [110, -180], [-110, -180], [-110, -20]])
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    waypoints_array = []
    lenght_array = []
    threads = []
    for c in car_array:
        t = threading.Thread(target=c.execute())
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    for c in car_array:
        lenght_array.append(c.lenght)
        waypoints_array.append(c.waypoint)
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


def crossover(best, dim, num_act, best_lenghts):
    def heuristic_choice():
        total = int(sum(best_lenghts))
        v = random.randint(1, total)
        for j in range(len(best_lenghts)):
            if v - best_lenghts[j] <= 0:
                return best[j]
            v -= best_lenghts[j]

    population = best
    n = len(best)
    while len(population) < dim:
        new_car = copy.deepcopy(heuristic_choice())
        new_car.actions_generator(int(new_car.tick * 0.4), num_act)
        population.append(new_car)
    for i in range(n):
        population[i].actions_generator(int(population[i].tick * 0.9), num_act)
    return population


def termination(lenght_array, waypoints_array):
    for i in range(len(lenght_array)):
        if lenght_array[i] > 700:
            for p in range(int(len(waypoints_array[i])/2), len(waypoints_array[i])):
                if np.linalg.norm((waypoints_array[i][p]) - np.array([0, 0])) < 4:
                    return True, i, p
    return False, -1, -1


def main_loop(actions_num, dim):
    while True:
        population = [Car(actions_num - 1, inner_poly, outer_poly) for _ in range(dim)]
        epoch = 0
        while epoch < 180:
            lenght_array, waypoints_array = fitness_calculation(population)
            if max(lenght_array) > 700:
                t, index, point = termination(lenght_array, waypoints_array)
                if t:
                    best_car = population[index]
                    display_ending(waypoints_array[index][:point], line_in, line_out, str(epoch), best_car)
                    return best_car
            selection_arr = selection(lenght_array)
            best = [population[i] for i in selection_arr]
            best_lenghts = [lenght_array[i] for i in selection_arr]
            if epoch % 30 == 0:
                display_running(waypoints_array, line_in, line_out, str(epoch))
            population = copy.deepcopy(crossover(best, dim, actions_num - 1, best_lenghts))
            epoch += 1


time = 100
population_dim = 50
car = main_loop(time, population_dim)
print("Car steps: " + str(car.tick))
print("COMPLETE")
