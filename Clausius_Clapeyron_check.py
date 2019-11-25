import pickle
import numpy as np


def getMass_H2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)

