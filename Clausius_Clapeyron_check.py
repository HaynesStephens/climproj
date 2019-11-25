import pickle
import numpy as np


def getMass_H2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)

def getPKLvals(file_name):
    file_load = open(file_name, 'rb')
    pkl = pickle.load(file_load)
    pw = getMass_H2O(pkl)
    tsurf = pkl['surface_temperature'][0]
    return pw, tsurf

insol=320
test_dir = '/project2/moyer/old_project/haynes/climt_files/varying_co2/{0}solar/'.format(insol)
ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
job_list = ['i{0}_{1}solar'.format(ppm, insol) for ppm in ppm_list]
file_name_list = ['{0}{1}/{1}_pkl_eq.pkl'.format(test_dir, job_name) for job_name in job_list]

pkl_vals = [getPKLvals(file_name) for file_name in file_name_list]

