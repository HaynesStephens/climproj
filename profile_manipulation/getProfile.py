import pickle
import numpy as np

def getMassH2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].copy().flatten()
    p_diff = np.diff(pkl['air_pressure_on_interface_levels'].copy().flatten())
    mass = (q * p_diff) / g
    return mass


file_name = '/home/haynes13/climt_files/control_fullstore/' \
                    'i270_290solar_fullstore/i270_290solar_fullstore_eq.pkl'
file_load = open(file_name, 'rb')
pkl = pickle.load(file_load)

getMassH2O(pkl)
