import numpy as np

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


def writeEQTable1Values(file_path, start_time, end_time):
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

    lwflx   = getEQValue('lwflx')
    swflx   = getEQValue('swflx')
    LwToa   = getEQValue('LwToa')
    SwToa   = getEQValue('SwToa')
    SwSrf   = getEQValue('SwSrf')
    LwSrf   = getEQValue('LwSrf')


    Ts        = getEQValue('Ts')
    precc     = getEQValue('precc')
    SrfLatFlx = getEQValue('SrfLatFlx')
    SrfSenFlx = getEQValue('SrfSenFlx')

    net_rad  = lwflx + swflx
    net_toa  = SwToa + LwToa
    net_surf = SwSrf + LwSrf + SrfLatFlx + SrfSenFlx

    t_air = getEQValue('T')
    writeEQProfile(t_air, 'air_temperature', file_path)
    writeEQProfile(net_rad, 'net_radiation', file_path)

    str_list = ['STARTtime', 'ENDtime', 'NETtoa', 'NETsurf', 'SWtoa',
                'LWtoa', 'SWsurf', 'LWsurf', 'LH', 'SH', 'Ts', 'Prec']
    val_list = [start_time, end_time, net_toa, net_surf, SwToa,
                LwToa, SwSrf, LwSrf, SrfLatFlx, SrfSenFlx, Ts, precc]
    txt_file = open('{0}_eqTable1Values.txt'.format(file_path), 'w')

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

job_name = 'shanshan_control'
print('JOB:', job_name)
file_path = '{0}/{1}/{1}'.format(base_path, job_name)
start_day = 9950
end_day = 10950 - 1
start_time = np.float(start_day * (24 * 60 * 60))
end_time = np.float((end_day) * (24 * 60 * 60))

# Procedures
writeEQTable1Values(file_path, start_time, end_time)
