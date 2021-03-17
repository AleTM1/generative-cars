import numpy as np

STARTING_ANGLE_LIST = {"Mexico_track": 180, "Bowtie_track": 330, "canada_race": 240, "Canada_Training": 160,
                       "London_Loop_Train": 350, "New_York_Track": 5, "Oval_Track": 0}


# sector = [x0, x1, y0, y1]
# return np.outer, np.inner, sectors, starting_angle
def load_track(name):
    TRACK_NAME = name
    points = np.load("./tracks/%s.npy" % TRACK_NAME)
    angle = STARTING_ANGLE_LIST[name]

    inner_border = 100 * np.array(points[:, 2:4])
    outer_border = 100 * np.array(points[:, 4:6])

    sectors = []
    for i in range(20, len(inner_border), 20):
        ref_point = np.array([outer_border[i, 0], outer_border[i, 1]])
        dest_point = np.array([inner_border[i, 0], inner_border[i, 1]])
        dist = np.linalg.norm(ref_point - dest_point)
        for j in range(len(inner_border)):
            d = np.linalg.norm(ref_point - np.array([inner_border[j, 0], inner_border[j, 1]]))
            if d < dist:
                dist = d
                dest_point = np.array([inner_border[j, 0], inner_border[j, 1]])
        sectors.append([ref_point[0], dest_point[0], ref_point[1], dest_point[1]])

    return outer_border, inner_border, sectors, angle
