import numpy as np
from netCDF4 import Dataset as ds
import pandas as pd
import copy

def openNC(filepath):
    """
    Open the nc file
    :param filepath: name of the nc file w/o the '.nc' extension
    :return: the opened nc file
    """
    nc_name = filepath + '.nc'
    return ds(nc_name, 'r+', format='NETCDF4')

def EQavg(var_dict, var):
    """
    Average over the past 10 years
    :param var_dict:
    :return: a dictionary of the average values
    """
    time_array = var_dict['time'].copy()
    var_array = var_dict[var].copy()
    years_back = 10
    days_back = years_back * 365.25
    time_last = time_array[-1]

    avg_since_day = time_last - days_back
    avg_index = np.where(time_array > avg_since_day)

    avg_var_dict = copy.deepcopy(var_dict)
    avg_var_dict['time'] = time_array[avg_index]
    print(avg_var_dict['time'].shape)
    avg_var_dict[var] = var_array[avg_index]
    print(avg_var_dict[var].shape)
    avg_var_dict[var+'_avg'] = np.mean(avg_var_dict[var].copy(), axis=0)
    return avg_var_dict

# def ShanshanEQFig4():
"""
Get the CCSM3 output to be used in Fig 4 of Shanshan's EQ paper.
Pre-industrial run. Net surface LW for Ts over 285 K.
Need to average over last 10 years.
:return:
Net surface LW for both total and T>285 batches
"""
base_path = '/project2/moyer/old_project/climate_data/RDCEP_CCSM3/'
rls_file = base_path + 'rls_Amon_CCSM3_II_Control_LongRunMIP_3805'
ts_file = base_path + 'ts_Amon_CCSM3_II_Control_LongRunMIP_3805'

def getNCdict(filepath, var):
    var_dict = {}
    var_nc = openNC(filepath)
    var_dict[var] = var_nc[var][:]
    var_dict['lat'] = var_nc['lat'][:]
    var_dict['time'] = var_nc['time'][:]
    return var_dict

rls_dict = getNCdict(rls_file, 'rls')
rls_avg_dict = EQavg(rls_dict, 'rls')
rls_avg = rls_avg_dict['rls'+'_avg']
print(rls_avg.shape)

ts_dict = getNCdict(ts_file, 'ts')
ts_avg_dict = EQavg(ts_dict, 'ts')
ts_avg = ts_avg_dict['ts'+'_avg']
print(ts_avg.shape)

ts_flat = ts_avg.flatten()
rls_flat = rls_avg.flatten()
ts_above_285 = np.where(ts_flat >= 285.0)
ts_final = ts_flat[ts_above_285]
rls_final = rls_flat[ts_above_285]

import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.scatter(ts_final, rls_final, c='k', s=4)
plt.xlim(284, 304)
plt.xticks(np.arange(284,305,4))
plt.ylim(55, 125)
plt.yticks(np.arange(60,121,20))
plt.show()




