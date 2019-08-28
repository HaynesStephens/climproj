# This is a script to write the appropriate values from an nc file into a smaller csv file
# to be added to the github repo so that I can download it to my computer
# without having to lug a brick of data on my harddrive.

import numpy as np
from netCDF4 import Dataset as ds

def saveData(data, file_path, var_name, eq_file = False):
    """
    Save the data array to a csv file
    :param data: numpy array to be saved
    :param file_path: name of the file to save w/o the '.csv' extension
    :param var_name: name of var to be saved, usually the variable name or a calculated quantity
    :return: save the csv file
    """
    if eq_file:
        var_name = 'eq_'+var_name
    csv_name = '{0}_{1}.csv'.format(file_path, var_name)
    np.savetxt(csv_name, data, delimiter=',')


def openNC(file_path):
    """
    Open the nc file
    :param file_path: name of the nc file w/o the '.nc' extension
    :return: the opened nc file
    """
    nc_name = file_path + '.nc'
    return ds(nc_name, 'r+', format='NETCDF4')


def getTimeSeries0D(nc, var_name):
    """
    Return the time series of a zero-dimensional quantity
    :param nc: nc file
    :param var_name: name of zero-dimensional variable
    :return: time series numpy array
    """
    data = nc[var_name][:].flatten()
    return data


def getTimeSeries1D(nc, var_name):
    """
    Return the time series of a one-dimensional quantity:
    :param nc: nc file
    :param var_name: name of the one-dimensional variable
    :return: time series numpy array
    """
    data = nc[var_name][:]
    print(data.shape)
    if var_name == 'air_temperature_tendency_from_convection':
        data = np.reshape(data, (data.shape[0], data.shape[-1]))
    else:
        data = np.reshape(data, (data.shape[0], data.shape[1]))
    return data


def calcMoistEnthalpySeries(nc):
    """
    Return a time series of the atmospheric moist enthalpy
    :param nc: nc file
    :return: numpy array (0D) time series
    """
    from sympl import get_constant
    Cpd = get_constant('heat_capacity_of_dry_air_at_constant_pressure', 'J/kg/degK')
    Cvap = get_constant('heat_capacity_of_vapor_phase', 'J/kg/K')
    g = get_constant('gravitational_acceleration', 'm/s^2')
    Lv = get_constant('latent_heat_of_condensation', 'J/kg')
    def heat_capacity(q):
        return Cpd * (1 - q) + Cvap * q

    def calcMoistEnthalpy(nc, i):
        dp = (nc['p'][i, :-1] - nc['p'][i, 1:])
        specific_humidity_i = nc['q'][i, :-1]
        C_tot = heat_capacity(specific_humidity_i)
        return np.sum((C_tot * nc['T'][i, :-1] + Lv * specific_humidity_i) * dp / g) / 1000

    moist_enthalpy_arr = []
    for i in range(nc['time'].size):
        moist_enthalpy_arr.append(calcMoistEnthalpy(nc, i))
    return np.array(moist_enthalpy_arr)


# List of saved quantities, sorted by dimension
store_quantities_0D =   ['time',
                        'Ts',
                        'precc',
                        'SrfSenFlx',
                        'SrfLatFlx',
                        'LwToa',
                        'SwToa',
                        'SwSrf',
                        'LwSrf']

store_quantities_1D =   ['T',
                        'p',
                        'q',
                        'lwflx',
                        'swflx']


# Parameters
job_name    = 'shanshan_control'
print('Job:', job_name)
nc_path     = '/home/haynes13/climt_runs/{0}/{0}'.format(job_name)
save_path   = '/home/haynes13/climt_files/{0}/{0}'.format(job_name)

# Procedure
nc = openNC(nc_path)

for var_name in store_quantities_0D:
    data = getTimeSeries0D(nc, var_name)
    saveData(data, save_path, var_name)
    print('Saved:', var_name)

for var_name in store_quantities_1D:
    data = getTimeSeries1D(nc, var_name)
    saveData(data, save_path, var_name)
    print('Saved:', var_name)

var_name = 'moist_enthalpy'
data = calcMoistEnthalpySeries(nc)
saveData(data, save_path, var_name)
print('Saved:', var_name)
