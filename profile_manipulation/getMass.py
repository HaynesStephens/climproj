import pickle
import numpy as np

def getMassH2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].copy().flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].copy().flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)


file_name = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
                    'i270_290solar_fullstore/i270_290solar_fullstore_pkl_eq.pkl'
file_load = open(file_name, 'rb')
pkl = pickle.load(file_load)

getMassH2O(pkl)


def getMassCO2(pkl):
    co2 = pkl['mole_fraction_of_carbon_dioxide_in_air']
