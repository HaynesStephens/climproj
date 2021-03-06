# This is a script to write the appropriate values from an nc file into a smaller csv file
# to be added to the github repo so that I can download it to my computer
# without having to lug a brick of data on my harddrive.

import numpy as np
from netCDF4 import Dataset as ds

def saveData(data, file_path, var_name):
    """
    Save the data array to a csv file
    :param data: numpy array to be saved
    :param file_path: name of the file to save w/o the '.csv' extension
    :param var_name: name of var to be saved, usually the variable name or a calculated quantity
    :return: save the csv file
    """
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

    air_pressure_on_interface_levels = getTimeSeries1D(nc, 'air_pressure_on_interface_levels')
    specific_humidity = getTimeSeries1D(nc, 'specific_humidity')
    air_temperature = getTimeSeries1D(nc, 'air_temperature')
    def calcMoistEnthalpy(nc, i):
        dp = (air_pressure_on_interface_levels[i, :-1] - air_pressure_on_interface_levels[i, 1:])
        specific_humidity_i = specific_humidity[i]
        C_tot = heat_capacity(specific_humidity_i)
        return np.sum((C_tot * air_temperature[i] + Lv * specific_humidity_i) * dp / g) / 1000

    moist_enthalpy_arr = []
    time = getTimeSeries0D(nc, 'time')
    for i in range(time.size):
        moist_enthalpy_arr.append(calcMoistEnthalpy(nc, i))
    return np.array(moist_enthalpy_arr)


def load_quantities_0D():
    return ['time',
            'surface_temperature',
            'convective_precipitation_rate',
            'stratiform_precipitation_rate',
            'surface_upward_sensible_heat_flux',
            'surface_upward_latent_heat_flux']


def load_quantities_1D():
    return ['air_temperature',
            'air_pressure',
            'specific_humidity',
            'air_pressure_on_interface_levels',
            'air_temperature_tendency_from_convection',
            'air_temperature_tendency_from_longwave',
            'air_temperature_tendency_from_shortwave',
            'mole_fraction_of_carbon_dioxide_in_air',
            'upwelling_longwave_flux_in_air',
            'upwelling_shortwave_flux_in_air',
            'downwelling_longwave_flux_in_air',
            'downwelling_shortwave_flux_in_air']


def saveTimeSeriesDim(nc, var_name, save_path, dim):
    if dim==0:
        data = getTimeSeries0D(nc, var_name)
    elif dim==1:
        data = getTimeSeries1D(nc, var_name)
    else:
        raise(ValueError, "WRONG DIMENSION GIVEN")
    saveData(data, save_path, var_name)
    print('Saved:', var_name)


def saveMoistEnthalpy(nc, save_path):
    var_name = 'moist_enthalpy'
    data = calcMoistEnthalpySeries(nc)
    saveData(data, save_path, var_name)
    print('Saved:', var_name)

# ### INDIVIDUAL EXECUTION. ###
# # List of saved quantities, sorted by dimension
# store_quantities_0D = load_quantities_0D()
# store_quantities_1D = load_quantities_1D()
#
# # Parameters
# test_dir = 'control/' # Needs to end in an '/'
# print('TEST:', test_dir)
#
# job_name    = 'i270_290solar'
# print('Job:', job_name)
#
# nc_path     = '/project2/moyer/old_project/haynes/climt_runs/{0}{1}/{1}'.format(test_dir, job_name)
# nc = openNC(nc_path)
# save_path   = '/project2/moyer/old_project/haynes/climt_files/{0}{1}/{1}'.format(test_dir, job_name)
#
# # Procedure
# for var_name in store_quantities_0D:
#     saveTimeSeriesDim(nc, var_name, save_path, dim=0)
# for var_name in store_quantities_1D:
#     saveTimeSeriesDim(nc, var_name, save_path, dim=1)
# saveMoistEnthalpy(nc, save_path)

