from graphical_engine import display
from car import Car
import numpy as np
import shapely.geometry.polygon
from shapely.geometry import Polygon


outer_border = np.array([[-150, 20], [150, 20], [150, -220], [-150, -220], [-150, 20]])
inner_border = np.array([[-110, -20], [110, -20], [110, -180], [-110, -180], [-110, -20]])
line_in = shapely.geometry.polygon.LineString(inner_border)
line_out = shapely.geometry.polygon.LineString(outer_border)
inner_poly = Polygon(line_in)
outer_poly = Polygon(line_out)


def start_simulation(car_array):
    waypoints_array = []
    tick_lenght_array = []
    for car in car_array:
        waypoints, tick, lenght = car.execute()
        tick_lenght_array.append([tick, lenght])
        waypoints_array.append(waypoints)
    display(waypoints_array, line_in, line_out)


def main_loop(actions_num, dim):
    population = [Car(actions_num - 1, inner_poly, outer_poly) for _ in range(dim)]
    start_simulation(population)


time = 40
population_dim = 20

main_loop(time, population_dim)

