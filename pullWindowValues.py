import numpy as np
import pandas as pd

# Pulling Values from whichever window you want
# Note: Make sure the time-ends (in seconds) of your window
#       match a time in the time_array of the simulation

def getData(file_path, var_name):
    """
    Load the data from a csv file
    :param file_path:
    :param var_name: name of variable to load (check NC output)
    :return: numpy array of data
    """
    data = np.loadtxt("{0}_{1}.csv".format(file_path, var_name), delimiter = ',')
    print(var_name, ', arr length:', data.size)
    return data


def getTimeArray(file_path):
    """
    Return the time array of the simulation.
    This is used because in the simulations where state['time'] is NOT updated,
    the time array will be all zeros, which you can't index.
    We want a time array we can index.
    """
    time_step = 10 * (60)
    """SAVE STEP IS KEY"""
    save_step = 36 * time_step
    time_arr = getData(file_path, 'time')
    time_arr = np.arange(0, time_arr.size*save_step, save_step)
    return time_arr


def getTimeIndices(time_arr, start_time, end_time):
    """
    Find the indices in the time array that correspond to the start and end times identified
    :param time_arr:
    :param start_time:
    :param end_time:
    :return: indices, start and end
    """
    start_i = np.where(time_arr == start_time)[0][0]
    end_i = np.where(time_arr == end_time)[0][0]
    return start_i, end_i


def getWindow(data, start_i, end_i):
    """
    return the window of data between the time indices
    :param data:
    :param start_i:
    :param end_i:
    :return:
    """
    return data[start_i:end_i + 1]


def printWindowValues(file_path, var_name, start_time, end_time):
    """
    Print the values (Mean, Median, STD) of the chosen variable within the time window
    :param file_path:
    :param var_name:
    :param start_time:
    :param end_time:
    :return:
    """
    data = getData(file_path, var_name)
    time_arr = getTimeArray(file_path)
    start_i, end_i = getTimeIndices(time_arr, start_time, end_time)
    data_window = getWindow(data, start_i, end_i)

    print('Var:', var_name)
    print('Start:', start_time)
    print('End:', end_time)
    print('Mean:', np.mean(data_window))
    print('Median:', np.median(data_window))
    print('STD:', np.std(data_window))


def writeEQProfile(data, var_name, file_path):
    """
    Write the EQ profile of a chosen variable into a csv file as a numpy array
    :param data: EQ profile
    :param var_name:
    :param file_path:
    :return:
    """
    csv_name = '{0}_eqProfile_{1}.csv'.format(file_path, var_name)
    np.savetxt(csv_name, data, delimiter=',')
    print("EQ Profile: ", var_name)


def writeEQTable1Values(file_path, start_time, end_time, extras=None):
    """
    Write out the EQ values and profiles of the time window into various files
    :param file_path:
    :param start_time:
    :param end_time:
    :return:
    """
    def getEQValue(var_name):
        """
        Get the EQ value or profile for a chosen variable
        :param var_name:
        :return:
        """
        data = getData(file_path, var_name)
        data_window = getWindow(data, start_i, end_i)
        return np.mean(data_window, axis = 0)

    time_arr = getTimeArray(file_path)
    start_i, end_i = getTimeIndices(time_arr, start_time, end_time)

    lw_up = getEQValue('upwelling_longwave_flux_in_air')
    lw_dn = getEQValue('downwelling_longwave_flux_in_air')
    sw_up = getEQValue('upwelling_shortwave_flux_in_air')
    sw_dn = getEQValue('downwelling_shortwave_flux_in_air')
    t_surf = getEQValue('surface_temperature')
    conv_prec = getEQValue('convective_precipitation_rate')
    strat_prec = getEQValue('stratiform_precipitation_rate')
    lh = getEQValue('surface_upward_latent_heat_flux')
    sh = getEQValue('surface_upward_sensible_heat_flux')

    net_lw = lw_up - lw_dn
    net_sw = sw_up - sw_dn
    net_rad = net_lw + net_sw
    net_toa = net_rad[-1]
    net_surf = net_rad[0] + lh + sh

    t_air = getEQValue('air_temperature')
    writeEQProfile(t_air, 'air_temperature', file_path)
    writeEQProfile(net_rad, 'net_radiation', file_path)

    str_list = ['STARTtime', 'ENDtime', 'NETtoa', 'NETsurf', 'SWtoa',
                'LWtoa', 'SWsurf', 'LWsurf', 'LH', 'SH', 'Ts', 'ConvPrec', 'StratPrec']
    val_list = [start_time, end_time, net_toa, net_surf, net_sw[-1],
                net_lw[-1], net_sw[0], net_lw[0], lh, sh, t_surf, conv_prec, strat_prec]
    assert len(str_list) == len(val_list), "Not the same length of strings and values."
    df = pd.DataFrame(columns = str_list, data = [val_list])

    if extras != None:
        df_ex = pd.DataFrame([extras], columns=extras.keys())
        df = pd.concat([df, df_ex], axis =1)

    df.to_csv('{0}_eqTable1Values.csv'.format(file_path), index=False)
    print('EQ Values written to csv.')

    return df


# ### INDIVIDUAL EXECUTION. ###
# # Parameters
# base_path = '/project2/moyer/old_project/haynes/climt_files/'
# test_dir = 'varying_co2_cst_q_rad/' # Needs to end in an '/'
# print('TEST:', test_dir)
#
# ppm = 270
# insol = 320
# job_name = 'i{0}_{1}solar_cst_q_rad'.format(ppm, insol)
# print('JOB:', job_name)
#
# file_path = '{0}{1}{2}/{2}'.format(base_path, test_dir, job_name)
# start_day = 9950
# end_day = 10950 - 1
# start_time = np.float(start_day * (24 * 60 * 60))
# end_time = np.float(end_day * (24 * 60 * 60))
# extras = {'ppm':ppm, 'insol':insol}
#
# # Procedures
# df = writeEQTable1Values(file_path, start_time, end_time, extras=extras)
