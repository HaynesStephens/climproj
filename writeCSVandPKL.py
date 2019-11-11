# This is a script to write the appropriate values from an nc file into a smaller csv file
# to be added to the github repo so that I can download it to my computer
# without having to lug a brick of data on my harddrive.

import numpy as np
from netCDF4 import Dataset as ds
import pickle

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

def load_var_list():
    return ['air_temperature',
            'surface_temperature',
            'specific_humidity',
            'eastward_wind',
            'northward_wind',
            'atmosphere_hybrid_sigma_pressure_a_coordinate_on_interface_levels',
            'atmosphere_hybrid_sigma_pressure_b_coordinate_on_interface_levels',
            'surface_air_pressure',
            'time',
            'air_pressure',
            'air_pressure_on_interface_levels',
            'longitude',
            'latitude',
            'height_on_ice_interface_levels',
            'surface_specific_humidity',
            'cloud_base_mass_flux',
            'mole_fraction_of_ozone_in_air',
            'mole_fraction_of_carbon_dioxide_in_air',
            'mole_fraction_of_methane_in_air',
            'mole_fraction_of_nitrous_oxide_in_air',
            'mole_fraction_of_oxygen_in_air',
            'mole_fraction_of_cfc11_in_air',
            'mole_fraction_of_cfc12_in_air',
            'mole_fraction_of_cfc22_in_air',
            'mole_fraction_of_carbon_tetrachloride_in_air',
            'surface_longwave_emissivity',
            'longwave_optical_thickness_due_to_cloud',
            'longwave_optical_thickness_due_to_aerosol',
            'cloud_area_fraction_in_atmosphere_layer',
            'mass_content_of_cloud_ice_in_atmosphere_layer',
            'mass_content_of_cloud_liquid_water_in_atmosphere_layer',
            'cloud_ice_particle_size',
            'cloud_water_droplet_radius',
            'zenith_angle',
            'surface_albedo_for_direct_shortwave',
            'surface_albedo_for_direct_near_infrared',
            'surface_albedo_for_diffuse_near_infrared',
            'surface_albedo_for_diffuse_shortwave',
            'shortwave_optical_thickness_due_to_cloud',
            'cloud_asymmetry_parameter',
            'cloud_forward_scattering_fraction',
            'single_scattering_albedo_due_to_cloud',
            'shortwave_optical_thickness_due_to_aerosol',
            'aerosol_asymmetry_parameter',
            'single_scattering_albedo_due_to_aerosol',
            'aerosol_optical_depth_at_55_micron',
            'downwelling_longwave_flux_in_air',
            'downwelling_shortwave_flux_in_air',
            'upwelling_longwave_flux_in_air',
            'upwelling_shortwave_flux_in_air',
            'surface_upward_latent_heat_flux',
            'surface_upward_sensible_heat_flux',
            'surface_thermal_capacity',
            'surface_material_density',
            'upward_heat_flux_at_ground_level_in_soil',
            'heat_flux_into_sea_water_due_to_sea_ice',
            'soil_layer_thickness',
            'ocean_mixed_layer_thickness',
            'heat_capacity_of_soil',
            'sea_water_density',
            'upwelling_longwave_flux_in_air_assuming_clear_sky',
            'downwelling_longwave_flux_in_air_assuming_clear_sky',
            'air_temperature_tendency_from_longwave_assuming_clear_sky',
            'air_temperature_tendency_from_longwave',
            'upwelling_shortwave_flux_in_air_assuming_clear_sky',
            'downwelling_shortwave_flux_in_air_assuming_clear_sky',
            'air_temperature_tendency_from_shortwave_assuming_clear_sky',
            'air_temperature_tendency_from_shortwave',
            'depth_of_slab_surface',
            'convective_state',
            'convective_precipitation_rate',
            'convective_downdraft_velocity_scale',
            'convective_downdraft_temperature_scale',
            'convective_downdraft_specific_humidity_scale',
            'atmosphere_convective_available_potential_energy',
            'air_temperature_tendency_from_convection',
            'stratiform_precipitation_rate']

def load_skip_list():
    return ['solar_cycle_fraction',
            'flux_adjustment_for_earth_sun_distance',
            'area_type']


def saveTimeSeriesDim(nc, var_name, save_path, dim):
    if dim==0:
        data = getTimeSeries0D(nc, var_name)
    elif dim==1:
        data = getTimeSeries1D(nc, var_name)
    else:
        raise(ValueError, "WRONG DIMENSION GIVEN")
    saveData(data, save_path, var_name)
    print('Saved:', var_name)


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


def saveMoistEnthalpy(nc, save_path):
    var_name = 'moist_enthalpy'
    data = calcMoistEnthalpySeries(nc)
    saveData(data, save_path, var_name)
    print('Saved:', var_name)


def saveEQpkl(save_path, nc, years_back = 3):
    skip_list = load_skip_list()
    print('Saving EQ Pickle!')
    eq_pkl = {}
    seconds_back = years_back*365.25*24*60*60
    time_array = nc['time'][:].copy()
    t_final = time_array[-1]
    eq_index = np.where(time_array > (t_final - seconds_back))

    for var in list(nc.variables):
        if var not in skip_list:
            print('pkl,', var)
            nc_var = nc[var][:].copy()
            var_eq_val = np.mean(nc_var[eq_index], axis=0)
            eq_pkl[var] = var_eq_val

    file_name = save_path + '.eq.pkl'
    f = open(file_name, 'wb')
    pickle.dump(eq_pkl, f)
    f.close()
    print('EQ Pickle Saved!')
    return eq_pkl

def saveTranspkl(save_path, nc):
    skip_list = load_skip_list()
    print('Saving Transient Pickle!')
    trans_pkl = {}

    for var in list(nc.variables):
        if var not in skip_list:
            print('pkl,', var)
            nc_var = nc[var][:].copy()
            var_trans_arr = nc_var[:5]
            trans_pkl[var] = var_trans_arr

    file_name = save_path + '.trans.pkl'
    f = open(file_name, 'wb')
    pickle.dump(trans_pkl, f)
    f.close()
    print('Transient Pickle Saved!')
    return trans_pkl




### INDIVIDUAL EXECUTION. ###
# List of saved quantities, sorted by dimension
store_quantities_0D = load_quantities_0D()
store_quantities_1D = load_quantities_1D()

# Parameters
test_dir = 'varying_co2_cst_q_rad/' # Needs to end in an '/'
print('TEST:', test_dir)

job_name    = 'i270_320solar_cst_q_rad_restart_test'
print('Job:', job_name)

nc_path     = '/home/haynes13/climt_runs/{0}{1}/{1}'.format(test_dir, job_name)
nc = openNC(nc_path)
save_path   = '/home/haynes13/climt_files/{0}{1}/{1}'.format(test_dir, job_name)

# Procedure
saveEQpkl(save_path, nc)
saveTranspkl(save_path, nc)
for var_name in store_quantities_0D:
    saveTimeSeriesDim(nc, var_name, save_path, dim=0)
for var_name in store_quantities_1D:
    saveTimeSeriesDim(nc, var_name, save_path, dim=1)


