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
    time = var_dict['time'].copy()
    var = var_dict[var].copy()
    years_back = 10
    days_back = years_back * 365.25
    time_last = time[-1]
    avg_since_day = time_last - days_back
    avg_index = np.where(time > avg_since_day)
    print(avg_index)
    avg_var_dict = copy.deepcopy(var_dict)
    avg_var_dict['time'] = time[avg_index]
    avg_var_dict[var] = var[avg_index]
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

ts_dict = getNCdict(ts_file, 'ts')
ts_avg_dict = EQavg(ts_dict, 'ts')



