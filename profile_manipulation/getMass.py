import pickle
import numpy as np


def getMass_H2O(q, pressure):
    """
    Get the column mass of precipitable water given the
    specific humidity profile and the interface pressure values
    :param q_flat:
    :param p_flat:
    :return: column mass of PW
    """
    g = 9.8
    q = q.flatten()
    pressure = pressure.flatten()
    p_diff = np.abs(np.diff(pressure))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)


def getMass_CO2(co2, pressure):
    """
    Get the column mass of CO2 given the pickle file
    which has gas profiles and the interface pressure levels needed for surface pressure
    :param pkl:
    :return:
    """
    g = 9.8
    co2 = co2.flatten()
    print('Is CO2 distribution constant? STD:', np.std(co2))
    ppm = co2[0]
    m_co2 = 0.044
    o3 = np.array([[3.113259024899186e-08, 3.133811056573404e-08, 3.170203478522222e-08, 3.224090896787597e-08,
                    3.296946650003885e-08, 3.389426148115974e-08, 3.5029531675952504e-08, 3.6433705587285916e-08,
                    3.8290287245223625e-08, 4.089393101471438e-08, 4.403573110818462e-08, 4.785125347060774e-08,
                    5.2517316999728584e-08, 5.8546829898145407e-08, 6.717734425929425e-08, 7.976676671728224e-08,
                    9.477495103343174e-08,1.1579490817554896e-07, 1.5261466007068122e-07, 2.1258307813935096e-07,
                    3.3021073014258835e-07, 4.93174665161799e-07, 6.707685755724308e-07, 1.3459010337532174e-06,
                    2.9031844345252494e-06, 3.854862595874254e-06, 3.7850347039090137e-06, 3.2771223731093804e-06]])
    m_o3 = 0.048
    o2 = np.ones(28) * 0.21000000000001118
    m_o2 = 0.032
    n2 = np.ones(28) - co2 - o3 - o2
    m_n2 = 0.028
    m_air = (co2 * m_co2) + (o3 * m_o3) + (o2 * m_o2) + (n2 * m_n2)
    m_air_mean = np.mean(m_air)
    pressure = pressure.flatten()
    p0 = pressure[0]
    column_mass = p0 / g
    total_mass_co2 = column_mass * (m_co2 / m_air_mean) * ppm
    print('CO2 Mass (kg)', np.sum(total_mass_co2))
    return total_mass_co2


def fitCstProfile_H20(q_mass, pressure):
    print('FITTING Q PROFILE')
    test_q = np.zeros(28)
    test_mass = 0
    i = 0
    while (np.abs(test_mass - q_mass) / q_mass) > 0.10:
        test_q = test_q + 0.0001
        test_mass = getMass_H2O(test_q, pressure)
        i += 1
        if i > 50:
            raise ArithmeticError('Profile with matching mass not found.')
    j = 0
    while (np.abs(test_mass - q_mass) / q_mass) > 0.01:
        if ((test_mass - q_mass) / q_mass) < 0:
            test_q = test_q + 0.00001
            test_mass = getMass_H2O(test_q, pressure)
        else:
            test_q = test_q - 0.00001
            test_mass = getMass_H2O(test_q, pressure)
        j += 1
        if j > 50:
            raise ArithmeticError('Profile with matching mass not found.')
    test_q = np.reshape(test_q, (28, 1, 1))
    return test_q, test_mass


def fitCstProfile_CO2(co2_mass, pressure):
    print('FITTING CO2 PROFILE')
    test_co2 = np.zeros(28)
    test_mass = 0
    i = 0
    while (np.abs(test_mass - co2_mass) / co2_mass) > 0.10:
        test_co2 = test_co2 + 0.0001
        test_mass = getMass_CO2(test_co2, pressure)
        i += 1
        if i > 50:
            raise ArithmeticError('Profile with matching mass not found.')
    j = 0
    while (np.abs(test_mass - co2_mass) / co2_mass) > 0.01:
        if ((test_mass - co2_mass) / co2_mass) < 0:
            test_co2 = test_co2 + 0.00001
            test_mass = getMass_CO2(test_co2, pressure)
        else:
            test_co2 = test_co2 - 0.00001
            test_mass = getMass_CO2(test_co2, pressure)
        j += 1
        if j > 50:
            raise ArithmeticError('Profile with matching mass not found.')
    return test_co2, test_mass


### PROCEDURE ###
file_name = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
                    'i270_290solar_fullstore/i270_290solar_fullstore_pkl_eq.pkl'
# file_name = '/project2/moyer/old_project/haynes/climt_files/varying_co2/290solar/' \
#             'i270_290solar/i270_290solar_pkl_eq.pkl'
file_load = open(file_name, 'rb')
pkl = pickle.load(file_load)
q = pkl['specific_humidity']
pressure = pkl['air_pressure_on_interface_levels']
co2 = pkl['mole_fraction_of_carbon_dioxide_in_air']

q_mass      = getMass_H2O(q, pressure)
co2_mass    = getMass_CO2(co2, pressure)

test_q, test_mass = fitCstProfile_H20(q_mass, pressure)

print(q.flatten())
print(test_q)
