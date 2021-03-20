from graphical_engine import display_running, display_ending
from track_loader import load_track
from car import Car
import shapely.geometry.polygon
from shapely.geometry import Polygon, Point
import random
import copy
import numpy as np


"""
ALLOWED TRACKS:
- Mexico_track (x100) # fixed
- Bowtie_track (x100)
- canada_race (x100)
- Canada_Training (x100)
- London_Loop_Train (x100)
- New_York_Track (x100)
- Oval_Track (x100)
"""

track = "Mexico_track"

center_line, outer_border, inner_border, starting_angle = load_track(track)
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    PROGRESS_BONUS = 15
    waypoints_array = []
    fitness_array = []
    for c in car_array:
        waypoints = c.execute()
        waypoints_array.append(waypoints)
        best_index = 0
        dist = 9999999
        for i in range(len(center_line)):
            d = np.linalg.norm(waypoints[-1] - center_line[i])
            if d < dist:
                dist = d
                best_index = i
        fitness_array.append((best_index**2) * PROGRESS_BONUS - c.tick ** 2)
    return fitness_array, waypoints_array


def selection(fitness_array):
    population_indexes = []
    m = max(fitness_array)
    quality = 1.0
    while len(population_indexes) < int(round(0.06 * len(fitness_array))):
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
        filter_best = [x for x in best_fitness if x > 0]
        total = int(sum(filter_best))
        v = random.randint(1, total)
        for j in range(len(filter_best)):
            if v - filter_best[j] <= 0:
                return best[j]
            v -= filter_best[j]

    population = best
    n = len(best)
    while len(population) < dim:
        new_car = copy.deepcopy(heuristic_choice())
        new_car.actions_generator(new_car.tick - 15, num_act)
        population.append(new_car)
    for i in range(n):
        population[i].actions_generator(population[i].tick - 7, num_act)
    return population


def termination(waypoints_array, ending_point):
    end_point = Point(ending_point[0], ending_point[1])
    for i in range(len(waypoints_array)):
        if len(waypoints_array[i]) > 50:
            for p in range(int(len(waypoints_array[i])/2), len(waypoints_array[i]) - 1):
                point2 = Point(waypoints_array[i][p])
                if point2.distance(end_point) < 15:
                    return True, i, p + 1
    return False, -1, -1


def main_loop(actions_num, dim, sp, sa, sspd):
    def init_population(start_p, ang, start_spd):
        return [Car(actions_num - 1, inner_poly, outer_poly, start_p, ang, start_spd) for _ in range(dim)]

    population = init_population(sp, sa, sspd)
    solution = []
    epoch = 0
    while True:
        epoch += 1
        fitness_array, waypoints_array = fitness_calculation(population)
        if False or epoch % 10 == 1:
            display_running(waypoints_array, line_in, line_out, str(epoch))
        if max([len(path) for path in waypoints_array]) > 100:
            test, index, point = termination(waypoints_array, sp)
            if test:
                best_car = population[index]
                solution.append([copy.deepcopy(waypoints_array[index][:point]), copy.deepcopy(best_car)])
                # display_ending(solution, line_in, line_out, sectors, epoch)
                return solution, epoch
        selection_arr = selection(fitness_array)
        best = [population[i] for i in selection_arr]
        best_fitness = [fitness_array[i] for i in selection_arr]
        population = copy.deepcopy(crossover(best, dim, actions_num - 1, best_fitness))


max_actions = 400
population_dim = 50
starting_point = center_line[0]
sol, ep = main_loop(max_actions, population_dim, starting_point, starting_angle, 0)
display_ending(sol, line_in, line_out, ep)
print("COMPLETED in " + str(ep) + " generations")
