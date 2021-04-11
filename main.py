from graphical_engine import display_running, display_ending
from track_loader import load_track
from car import Car
import shapely.geometry.polygon
from shapely.geometry import Polygon, Point
import random
import copy
import numpy as np


"""
AVALIBLES TRACKS:
- Mexico_track (x100) 
- canada_race (x100)
- Bowtie_track (x100)
"""

plot_inter_results = True
track = "Bowtie_track"

center_line, outer_border, inner_border, starting_angle = load_track(track)
starting_point = center_line[0]
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    PROGRESS_BONUS = 10     # Larger the value, smaller the speed bonus
    waypoints_array = []
    fitness_array = []
    for c in car_array:  # Each exemplar is actually tested and evaluated according to its progress
        waypoints = c.execute()
        waypoints_array.append(waypoints)
        best_index = 0
        dist = 9999999
        for i in range(len(center_line)): # Computing the closest point on the central line reached by the individual
            d = np.linalg.norm(waypoints[-1] - center_line[i])
            if d < dist:
                dist = d
                best_index = i
        fitness_array.append((best_index ** 2) * PROGRESS_BONUS - c.tick ** 2)
    return fitness_array, waypoints_array


def selection(fitness_array):
    copy_fitness_array = copy.deepcopy(fitness_array)
    fittest_individuals_indexes = []
    FITTEST_PERCENTAGE = 0.1    # Looking for the fittest individuals of current generation
    for _ in range(int(round(FITTEST_PERCENTAGE * len(fitness_array)))):
        index = copy_fitness_array.index(max(copy_fitness_array))
        fittest_individuals_indexes.append(index)
        copy_fitness_array.pop(index)
    return fittest_individuals_indexes


def crossover(best, dim, best_fitness):
    def heuristic_choice():  # Better solutions have better chance to be chosen as parents
        best_individuals = []
        best_fitness_copy = copy.deepcopy(best_fitness)
        for _ in range(2):  # select 2 parents
            total = int(sum(best_fitness_copy))
            v = random.randint(1, total)
            for j in range(len(best_fitness_copy)):
                if v - best_fitness_copy[j] <= 0:
                    best_individuals.append(best[j])
                    best_fitness_copy.pop(j)
                    break
                v -= best_fitness_copy[j]
        if best_individuals[0].tick < best_individuals[1].tick:
            best_individuals = [best_individuals[1], best_individuals[0]]     # parent 0 is fitter than parent 1
        return best_individuals

    population = best   # Parents are kept in the new generation
    while len(population) < dim:    # Until a new population is generated, it's started a new crossover procedure
        parents = heuristic_choice()
        new_car = copy.deepcopy(parents[0])
        threshold = int((random.random() * 0.5 + 0.25) * len(new_car.rel_actions))
        # Percentage of chromosome inherited from both parents is between .25 and .75
        for i in range(len(new_car.rel_actions)):
            if i < threshold:
                new_car.rel_actions[i] = copy.deepcopy(parents[1].rel_actions[i])
        new_car.update_abs_actions()
        population.append(new_car)
    return population


def mutation(population):
    for p in population:    # Part of mutations are concentrated around the crash moment (happend at p.tick)
        p.mute_rel_actions(p.tick - 10, p.tick + 10)

    MUTATION_PROBABILITY = 0.03
    for p in population:    # Random mutation all over the chromosome
        for i in range(5, len(p.rel_actions) - 5, 10):
            if random.random() < MUTATION_PROBABILITY:
                p.mute_rel_actions(i, i + 5)
    return population


def termination(waypoints_array, ending_point):
    end_point = Point(ending_point[0], ending_point[1])
    for i in range(len(waypoints_array)):
        if len(waypoints_array[i]) > 100:   # check only path which are long enough
            for p in range(int(len(waypoints_array[i])/2), len(waypoints_array[i]) - 1):
                point2 = Point(waypoints_array[i][p])
                if point2.distance(end_point) < 25:  # check if at least one point is close to the ending point
                    return True, i, p + 1   # return individual's index and its last useful path point
    return False, -1, -1


def main_loop(actions_num, dim, sp, sa):
    population = [Car(actions_num - 1, inner_poly, outer_poly, sp, sa) for _ in range(dim)]  # initialize population

    generation = 0
    while True:
        generation += 1
        fitness_array, waypoints_array = fitness_calculation(population)
        if plot_inter_results and generation % 5 == 1:
            display_running(waypoints_array, line_in, line_out, str(generation))
        if max([len(path) for path in waypoints_array]) > 100:
            test, index, point = termination(waypoints_array, sp)
            if test:    # true only if a solution has been found
                best_car = population[index]
                solution = [waypoints_array[index][:point], best_car]
                return solution, generation
        fittest_individuals_indexes = selection(fitness_array)
        best = [population[i] for i in fittest_individuals_indexes] # extracting best individuals given the indexes
        best_fitness = [fitness_array[i] for i in fittest_individuals_indexes] # extracting correlated fitness values
        population = crossover(best, dim, best_fitness)
        population = mutation(population)


max_actions = 200   # chromosome lenght
population_dim = 70     # number of individuals for each generation
sol, gen = main_loop(max_actions, population_dim, starting_point, starting_angle)

display_ending(sol, line_in, line_out, gen)
print("COMPLETED in " + str(gen) + " generations")
