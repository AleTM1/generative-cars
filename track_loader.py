import numpy as np

STARTING_ANGLE_LIST = {"Mexico_track": 180, "Bowtie_track": 30, "canada_race": 90}


# return np.center, np.outer, np.inner, starting_angle
def load_track(name):
    TRACK_NAME = name
    points = np.load("./tracks/%s.npy" % TRACK_NAME)
    angle = STARTING_ANGLE_LIST[name]

    center_line = 100 * np.array(points[:, 0:2])
    inner_border = 100 * np.array(points[:, 2:4])
    outer_border = 100 * np.array(points[:, 4:6])

    return center_line, outer_border, inner_border, angle
