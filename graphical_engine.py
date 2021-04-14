import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as mcm
from car import Car


def extract_solution_features(solution):
    x = []
    y = []
    colors = []
    (waypoints, car) = solution
    print(len(waypoints))
    for i in range(len(waypoints)):
        x.append(waypoints[i, 0])
        y.append(waypoints[i, 1])
        colors.append(car.abs_actions[i, 0])
    return x, y, colors


def plot_borders(line_in, line_out, ax):
    x, y = line_in.xy
    ax.plot(x, y, color="cyan", alpha=1, linewidth=3, solid_capstyle='round', zorder=2)
    x, y = line_out.xy
    ax.plot(x, y, color="cyan", alpha=1, linewidth=3, solid_capstyle='round', zorder=2)


# Display all the explored racelines
def display_running(waypoints_array, line_in, line_out, epoch):
    fig = plt.figure(1, figsize=(24, 14))
    ax = fig.add_subplot(111, facecolor='black')
    plot_borders(line_in, line_out, ax)

    def plot_racelines():
        x = []
        y = []
        for waypoints in waypoints_array:
            for p in waypoints:
                x.append(p[0])
                y.append(p[1])
            ax.scatter(x, y, c='red', marker='.')

    plot_racelines()
    plt.title("Epoch number: " + epoch)
    plt.show()
    # fig.savefig('saves/' + generation + '.png')


# Display the solution
def display_ending(solution, line_in, line_out, generation):
    fig = plt.figure(1, figsize=(24, 16))
    ax = fig.add_subplot(111, facecolor='black')
    plot_borders(line_in, line_out, ax)

    def plot_raceline():
        x, y, colors = extract_solution_features(solution)
        ax.scatter(x[0], y[0], color='green', alpha=1, linewidth=45, marker='o')
        col = np.subtract(1, np.array(colors) / Car.max_spd)  # normalize colors
        ax.scatter(x, y, marker='.', s=50, linewidths=4, c=col, cmap=mcm.RdYlBu, zorder=4)

    plot_raceline()
    plt.title("Total generation needed: " + str(generation))
    plt.show()
    # fig.savefig('saves/' + str(generation) + '_complete.png')
