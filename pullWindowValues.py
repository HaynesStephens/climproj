import numpy as np

# Pulling Values from whichever window you want
# Note: Make sure the time-ends (in seconds) of your window
#       match a time in the time_array of the simulation

def getData(file_path, var_name):
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
    save_step = 100 * time_step
    time_arr = getData(file_path, 'time')
    time_arr = np.arange(0, time_arr.size*save_step, save_step)
    return time_arr


def getTimeIndices(time_arr, start_time, end_time):
    start_i = np.where(time_arr == start_time)[0][0]
    end_i = np.where(time_arr == end_time)[0][0]
    return start_i, end_i


def getWindow(data, start_i, end_i):
    return data[start_i:end_i + 1]


def printWindowValues(file_path, var_name, start_time, end_time):
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


def writeEQTable1Values(file_path, start_time, end_time):
    def getEQValue(var_name):
        data = getData(file_path, var_name)
        time_arr = getTimeArray(file_path)
        start_i, end_i = getTimeIndices(time_arr, start_time, end_time)
        data_window = getWindow(data, start_i, end_i)
        return np.mean(data_window, axis = 0)

    lw_up = getEQValue('upwelling_longwave_flux_in_air')
    lw_dn = getEQValue('downwelling_longwave_flux_in_air')
    sw_up = getEQValue('upwelling_shortwave_flux_in_air')
    sw_dn = getEQValue('downwelling_shortwave_flux_in_air')
    t_surf = getEQValue('surface_temperature')
    prec = getEQValue('convective_precipitation_rate')
    lh = getEQValue('surface_upward_latent_heat_flux')
    sh = getEQValue('surface_upward_sensible_heat_flux')

    net_lw = lw_up - lw_dn
    net_sw = sw_up - sw_dn
    net_rad = net_lw + net_sw
    net_toa = net_rad[-1]
    net_surf = net_rad[0] + lh + sh

    str_list = ['STARTtime', 'ENDtime', 'NETtoa', 'NETsurf', 'SWtoa',
                'LWtoa', 'SWsurf', 'LWsurf', 'LH', 'SH', 'Ts', 'Prec']
    val_list = [start_time, end_time, net_toa, net_surf, net_sw[-1],
                net_lw[-1], net_sw[0], net_lw[0], lh, sh, t_surf, prec]
    txt_file = open('{0}_EQTable1Values.txt'.format(file_path), 'w')

    assert len(str_list) == len(val_list), "Not the same length of strings and values."
    for i in range(len(str_list)):
        str_i = str_list[i]
        val_i = val_list[i]
        out_statement = '{0}: {1}'.format(str_i, val_i)
        print(out_statement)
        txt_file.write(out_statement + '\n')

    return str_list, val_list


# Parameters
base_path = '/home/haynes13/climt_files'
job_name = 'test_a1_b1_c1_270i_939solar_dryconv_usurf_noseason'
print('JOB:', job_name)
file_path = '{0}/{1}/{1}'.format(base_path, job_name)
start_time = np.float(9950 * (24 * 60 * 60))
end_time = np.float(10950 * (24 * 60 * 60))

# Procedures
writeEQTable1Values(file_path, start_time, end_time)
