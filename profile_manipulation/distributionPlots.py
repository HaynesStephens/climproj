import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

input_param = 'T'
input_ppm = 1080
expt_name = 'swap_profiles'

control_ppm = 270
distribution_reference  = {}
distribution_expt       = {}
distribution_names      = {'T':'air_temperature',
                           'q':'specific_humidity',
                           'co2':'mole_fraction_of_carbon_dioxide_in_air'}
air_pressure = np.array([101044.31028195, 100195.77632999,  98759.75807375,  96753.28367667,
                         94200.1457147 ,  91130.61904627,  87581.10181558,  83593.68384655,
                         79215.64754524,  74498.90722888,  69499.39352998,  64276.39017481,
                         58891.83100072,  53409.56554756,  47894.6019316 ,  42412.3359785 ,
                         37027.77575477,  31804.77068994,  26805.2544242 ,  22088.51034726,
                         17710.4685095 ,  13723.04217571,  10173.51171009,   7103.96255531,
                         4550.78198329,   2544.21105313,   1107.88404987,    256.0893821 ])
os.system('mkdir -p /home/haynes13/code/python/climproj/figures/distributionPlots/{0}'.format(expt_name))

control_base = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
               'i{0}_320solar_fullstore/i{0}_320solar_fullstore'.format(control_ppm)
input_base = '/project2/moyer/old_project/haynes/climt_files/varying_co2/320solar/' \
             'i{0}_320solar/i{0}_320solar'.format(input_ppm)
expt_dir = '/project2/moyer/old_project/haynes/climt_files/diagnostic/{0}/'.format(expt_name)

def loadProfile(file_name, dict_key):
    pkl_file = open(file_name, 'rb')
    pkl = pickle.load(pkl_file)
    profile = pkl[dict_key]
    return profile

for param in distribution_names.keys():
    key_name = distribution_names[param]
    if param == input_param:
        file_name = '{0}_pkl_eq.pkl'.format(input_base)
    else:
        file_name = '{0}_pkl_eq.pkl'.format(control_base)
    print(file_name)
    profile = loadProfile(file_name, key_name)
    distribution_reference[param] = profile

    expt_file_name = '{0}{1}/diagnostic_{2}_{1}_input{3}_pkl_eq.pkl'.format(expt_dir, param, expt_name, input_ppm)
    print(expt_file_name)
    distribution_expt[param] = loadProfile(expt_file_name, key_name)

# fig, subplots = plt.subplots(2, 3, figsize=(21,8), sharey=True)

