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
- Mexico_track (x100) 
- Bowtie_track (x100)
- canada_race (x100)
"""

plot_inter_results = False
track = "Bowtie_track"

center_line, outer_border, inner_border, starting_angle = load_track(track)
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    PROGRESS_BONUS = 10
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


def crossover(best, dim, best_fitness):
    def heuristic_choice(num_choices):
        best_exemplars = []
        best_values_copy = copy.deepcopy(best_fitness)
        for _ in range(num_choices):
            total = int(sum(best_values_copy))
            v = random.randint(1, total)
            for j in range(len(best_values_copy)):
                if v - best_values_copy[j] <= 0:
                    best_exemplars.append(best[j])
                    best_values_copy.pop(j)
                    break
                v -= best_values_copy[j]
        if best_exemplars[0].tick < best_exemplars[1].tick:
            best_exemplars = [best_exemplars[1], best_exemplars[0]]     # parent 0 is better than parent 1
        return best_exemplars

    population = best
    while len(population) < dim:
        parents = heuristic_choice(2)
        new_car = copy.deepcopy(parents[0])
        part = int((random.random() * 0.5 + 0.25) * (new_car.tick - 1)) + 1  # crossover between 25% and 75%
        for i in range(len(new_car.rel_actions)):
            if i < part:
                new_car.rel_actions[i] = copy.deepcopy(parents[1].rel_actions[i])
        new_car.update_abs_actions()
        population.append(new_car)
    return population


def mutation(population):
    for p in population:
        p.mute_rel_actions(p.tick - 10, p.tick + 10)
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
        if plot_inter_results and epoch % 10 == 1:
            display_running(waypoints_array, line_in, line_out, str(epoch))
        if max([len(path) for path in waypoints_array]) > 100:
            test, index, point = termination(waypoints_array, sp)
            if test:
                best_car = population[index]
                solution.append([copy.deepcopy(waypoints_array[index][:point]), copy.deepcopy(best_car)])
                return solution, epoch
        selection_arr = selection(fitness_array)
        best = [population[i] for i in selection_arr]
        best_fitness = [fitness_array[i] for i in selection_arr]
        population = copy.deepcopy(crossover(best, dim, best_fitness))
        population = copy.deepcopy(mutation(population))


max_actions = 300
population_dim = 40
starting_point = center_line[0]
sol, ep = main_loop(max_actions, population_dim, starting_point, starting_angle, Car.min_spd)
display_ending(sol, line_in, line_out, ep)
print("COMPLETED in " + str(ep) + " generations")
