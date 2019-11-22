import pickle
import numpy as np

def getMassH2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)


file_name = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
                    'i270_290solar_fullstore/i270_290solar_fullstore_pkl_eq.pkl'
file_load = open(file_name, 'rb')
pkl = pickle.load(file_load)

getMassH2O(pkl)


def getMassCO2(pkl):
    g = 9.8
    co2 = pkl['mole_fraction_of_carbon_dioxide_in_air'].flatten()
    ppm = co2[0]
    p = pkl['air_pressure_on_interface_levels'].flatten()
    p0 = p[0]
    column_mass = p0 / g
    print()


mole_list = ['mole_fraction_of_ozone_in_air',
            'mole_fraction_of_carbon_dioxide_in_air',
            'mole_fraction_of_methane_in_air',
            'mole_fraction_of_nitrous_oxide_in_air',
            'mole_fraction_of_oxygen_in_air',
            'mole_fraction_of_cfc11_in_air',
            'mole_fraction_of_cfc12_in_air',
            'mole_fraction_of_cfc22_in_air',
            'mole_fraction_of_carbon_tetrachloride_in_air']

for mole in mole_list:
    print(mole_list)
    print(pkl[mole].flatten())


