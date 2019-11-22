import pickle
import numpy as np


def getMass_H2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)


def getMass_CO2(pkl):
    g = 9.8
    co2 = pkl['mole_fraction_of_carbon_dioxide_in_air'].flatten()
    o3 = pkl['mole_fraction_of_ozone_in_air'].flatten()
    o2 = pkl['mole_fraction_of_oxygen_in_air'].flatten()
    ppm = co2[0]
    p = pkl['air_pressure_on_interface_levels'].flatten()
    p0 = p[0]
    column_mass = p0 / g


# file_name = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
#                     'i270_290solar_fullstore/i270_290solar_fullstore_pkl_eq.pkl'
file_name = '/project2/moyer/old_project/haynes/climt_files/varying_co2/320solar/' \
            'i1080_320solar/i1080_320solar.eq.pkl'
file_load = open(file_name, 'rb')
pkl = pickle.load(file_load)

getMass_H2O(pkl)
getMass_CO2(pkl)
