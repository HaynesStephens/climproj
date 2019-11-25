import pickle
import numpy as np


def getMass_H2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)

test_dir = 'varying_co2/'
insol = 320
ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
file_name_list = []

for file_name in file_name_list:
    file_load = open(file_name, 'rb')
    pkl = pickle.load(file_load)
    PW = getMass_H2O(pkl)
    Tsurf = pkl['surface_temperature'].flatten()
