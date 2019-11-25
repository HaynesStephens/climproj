import pickle
import numpy as np


def getMass_H2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)

insol=320
test_dir = 'varying_co2/{0}solar/'.format(insol)
ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
job_list = ['i{0}_{1}solar'.format(ppm, insol) for ppm in ppm_list]
file_name_list = ['{0}{1}/{1}_pkl_eq.pkl'.format(test_dir, job_name) for job_name in job_list]

for file_name in file_name_list:
    file_load = open(file_name, 'rb')
    pkl = pickle.load(file_load)
    PW = getMass_H2O(pkl)
    Tsurf = pkl['surface_temperature'].flatten()
