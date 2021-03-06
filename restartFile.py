import numpy as np
import pickle

# base_path = '/project2/moyer/old_project/haynes/climt_files/'
# restart_dir = 'varying_co2/320solar/'
# job_name = 'i270_320solar'
# restart_file = '{0}{1}{2}/{2}'.format(base_path, restart_dir, job_name)


def OLD_loadTXT(restart_file, var_name):
    """

    :param restart_file:
    :param var_name: name of state/diagnostic variable that you want to load
    :return: the last instance of that variable in the time series, as a numpy array
    """
    csv_file = "{0}_{1}.csv".format(restart_file, var_name)
    last_state = np.loadtxt(csv_file, delimiter = ',')[-1]
    if last_state.size == 1:
        return last_state
    elif last_state.size > 1:
        return last_state.reshape(last_state.size, 1, 1)
    else:
        raise (AssertionError, "Initial Quantity Has a Size Less Than 1.")

def OLD_setInstance(restart_file, restart_state, var_name):
    """
    Set the key of the state dictionary to the last instance in the restart file,
        for a given variable
    :param restart_file:
    :param restart_state:
    :param var_name:
    :return: Nothing, just change the dictionary
    """
    print('Loading:', var_name)
    restart_state[var_name] = loadTXT(restart_file, var_name)


def OLD_loadRestartState(restart_file):
    """
    Load quantities from the last instance in the restart file to make a restart state
    :param restart_file:
    :return: dictionary of the last instance for various variables
    """
    restart_state = {} # initialize restart state as an empty dictionary

    state_names = ['air_pressure',
                   'air_pressure_on_interface_levels',
                   'air_temperature',
                   'downwelling_longwave_flux_in_air',
                   'downwelling_shortwave_flux_in_air',
                   'upwelling_longwave_flux_in_air',
                   'upwelling_shortwave_flux_in_air',
                   'specific_humidity',
                   'surface_temperature',
                   'surface_upward_latent_heat_flux',
                   'surface_upward_sensible_heat_flux']


    for var_i in state_names:
        setInstance(restart_file, restart_state, var_i)

    file_name = restart_file + '_restart_state.pkl'
    f = open(file_name, 'wb')
    pickle.dump(restart_state, f)
    f.close()

    return restart_state
