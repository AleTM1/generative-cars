import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as mcm
from car import Car


def create_unique_raceline(solution):
    x = []
    y = []
    colors = []
    for (waypoints, car) in solution:
        print(car.rel_actions)
        print(car.abs_actions)
        for i in range(len(waypoints)):
            x.append(waypoints[i, 0])
            y.append(waypoints[i, 1])
            colors.append(car.abs_actions[i, 0])
    return x, y, colors


def display_running(waypoints_array, line_in, line_out, epoch):
    fig = plt.figure(1, figsize=(24, 14))
    ax = fig.add_subplot(111, facecolor='black')

    def print_frame():
        def plot_border(ob, col):
            x, y = ob.xy
            ax.plot(x, y, color=col, alpha=0.9, linewidth=3, solid_capstyle='round', zorder=2)

        def plot_sectors(segments_coords, col):
            for segment in segments_coords:
                ax.plot(segment[:2], segment[2:4], color=col, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

        def plot_raceline():
            x = []
            y = []
            for waypoints in waypoints_array:
                for p in waypoints:
                    x.append(p[0])
                    y.append(p[1])
                ax.scatter(x, y, c='red', marker='.')
        plot_border(line_in, "cyan")
        plot_border(line_out, "cyan")
        plot_raceline()

    print_frame()
    plt.title("Epoch number: " + epoch)
    plt.show()
    # fig.savefig('saves/' + epoch + '.png')


def display_ending(solution, line_in, line_out, epoch):
    fig = plt.figure(1, figsize=(24, 16))
    ax = fig.add_subplot(111, facecolor='black')

    def print_frame():
        def plot_border(ob, col):
            x, y = ob.xy
            ax.plot(x, y, color=col, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

        def plot_sectors(segments_coords):
            c = 1
            for seg in segments_coords:
                if c == len(segments_coords):
                    ax.plot(seg[:2], seg[2:4], color='green', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
                else:
                    ax.plot(seg[:2], seg[2:4], color='white', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
                c += 1

        def plot_raceline():
            x, y, colors = create_unique_raceline(solution)
            col = np.subtract(1, np.subtract(np.array(colors), Car.min_spd) / Car.max_spd)
            ax.scatter(x, y, marker='.', s=50, linewidths=4, c=col, cmap=mcm.RdYlBu, zorder=4)

        plot_border(line_in, "cyan")
        plot_border(line_out, "cyan")
        plot_raceline()

    print_frame()
    plt.title("Total generation needed: " + str(epoch))
    plt.show()
    # fig.savefig('saves/' + epoch + '_complete.png')
