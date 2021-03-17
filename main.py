from graphical_engine import display_running, display_ending
from track_loader import load_track
from car import Car
import shapely.geometry.polygon
from shapely.geometry import Polygon, LineString, Point
import random
import copy


"""
ALLOWED TRACKS:
- Mexico_track (x100)
- Bowtie_track (x100)
- canada_race (x100)
- Canada_Training (x100)
- London_Loop_Train (x100)
- New_York_Track (x100)
- Oval_Track (x100)
"""

track = "Canada_Training"

outer_border, inner_border, sectors, starting_angle = load_track(track)
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def fitness_calculation(car_array):
    PENALIZATION_PARAM = 6
    waypoints_array = []
    fitness_array = []
    for c in car_array:
        waypoints, lenght = c.execute()
        fitness_array.append(lenght - PENALIZATION_PARAM * c.tick)
        waypoints_array.append(waypoints)
    return fitness_array, waypoints_array


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
        new_car.actions_generator(int(new_car.tick * 0.4), num_act)
        population.append(new_car)
    for i in range(n):
        population[i].actions_generator(int(population[i].tick * 0.9), num_act)
    return population


def termination(waypoints_array, sector_line):
    line = LineString([Point(sector_line[0], sector_line[2]), Point(sector_line[1], sector_line[3])])
    for i in range(len(waypoints_array)):
        for p in range(int(len(waypoints_array[i])/2), len(waypoints_array[i]) - 1):
            point1 = Point(waypoints_array[i][p-1])
            point2 = Point(waypoints_array[i][p])
            dist1 = point1.distance(line)
            dist2 = point2.distance(line)
            intra_dist = point1.distance(point2)
            if point2.distance(line) < 10 and abs(dist2 - dist1)/intra_dist > 0.7:
                return True, i, p + 1
            break
    return False, -1, -1


def main_loop(actions_num, dim, sp, sa, sspd):
    def init_population(start_p, ang, start_spd):
        return [Car(actions_num - 1, inner_poly, outer_poly, start_p, ang, start_spd) for _ in range(dim)]

    population = init_population(sp, sa, sspd)
    solution = []
    epoch = 0
    j = 0
    while True:
        k = 0
        while True:
            epoch += 1
            sector = sectors[j]
            fitness_array, waypoints_array = fitness_calculation(population)
            if False or epoch == 1:
                display_running(waypoints_array, line_in, line_out, sectors, str(epoch))
            if max(fitness_array) > 1:
                test, index, point = termination(waypoints_array, sector)
                if test:
                    best_car = population[index]
                    solution.append([copy.deepcopy(waypoints_array[index][:point]), copy.deepcopy(best_car)])
                    display_ending(solution, line_in, line_out, sectors, epoch)
                    if j == len(sectors) - 1:
                        return solution, epoch
                    population = init_population(waypoints_array[index][point], best_car.get_angle(point), best_car.actions[point, 0])
                    break
            selection_arr = selection(fitness_array)
            best = [population[i] for i in selection_arr]
            best_fitness = [fitness_array[i] for i in selection_arr]
            if k > 0 and k % 20 == 0 and j > 0:
                print("RESET")
                j -= 1
                if j > 0:
                    last_wp = solution[j-1][0]
                    last_best_car = solution[j-1][1]
                    population = init_population(last_wp[-1], last_best_car.get_angle(len(last_wp) - 1), last_best_car.actions[len(last_wp) - 1, 0])
                else:
                    population = init_population(sp, sa, sspd)
                solution.pop()
            else:
                population = copy.deepcopy(crossover(best, dim, actions_num - 1, best_fitness))
            k += 1
        j += 1


max_actions = 80
population_dim = 30
starting_point = [(sectors[-1][0] + sectors[-1][1])/2, (sectors[-1][2] + sectors[-1][3])/2]
sol, ep = main_loop(max_actions, population_dim, starting_point, starting_angle, 0)
display_ending(sol, line_in, line_out, sectors, ep)
print("COMPLETED in " + str(ep) + " generations")
