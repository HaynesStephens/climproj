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
    o3 = np.array([[3.113259024899186e-08, 3.133811056573404e-08, 3.170203478522222e-08, 3.224090896787597e-08,
                    3.296946650003885e-08, 3.389426148115974e-08, 3.5029531675952504e-08, 3.6433705587285916e-08,
                    3.8290287245223625e-08, 4.089393101471438e-08, 4.403573110818462e-08, 4.785125347060774e-08,
                    5.2517316999728584e-08, 5.8546829898145407e-08, 6.717734425929425e-08, 7.976676671728224e-08,
                    9.477495103343174e-08,1.1579490817554896e-07, 1.5261466007068122e-07, 2.1258307813935096e-07,
                    3.3021073014258835e-07, 4.93174665161799e-07, 6.707685755724308e-07, 1.3459010337532174e-06,
                    2.9031844345252494e-06, 3.854862595874254e-06, 3.7850347039090137e-06, 3.2771223731093804e-06]])
    o2 = np.ones(28) * 0.21000000000001118
    n2 = np.ones(28) - co2 - o3 - o2
    print(co2)
    print(o3)
    print(o2)
    print(n2)
    p = pkl['air_pressure_on_interface_levels'].flatten()
    p0 = p[0]
    column_mass = p0 / g


file_name = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
                    'i270_290solar_fullstore/i270_290solar_fullstore_pkl_eq.pkl'
# file_name = '/project2/moyer/old_project/haynes/climt_files/varying_co2/320solar/' \
#             'i1080_320solar/i1080_320solar.eq.pkl'
file_load = open(file_name, 'rb')
pkl = pickle.load(file_load)

getMass_H2O(pkl)
getMass_CO2(pkl)
