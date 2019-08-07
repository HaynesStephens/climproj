import numpy as np
from netCDF4 import Dataset as ds


# Pulling Values from whichever window you want
# Note: Make sure the time-ends (in seconds) of your window
#       match a time in the time_array of the simulation

def getData(file_path, var_name):
    return np.loadtxt("{0}_{1}.csv".format(file_path, var_name), delimiter = ',')


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
    time_arr = np.arange(time_arr.size*save_step, save_step)
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


# Parameters
base_path = '/home/haynes13/climt_files'
job_name = 'test_a1_b1_c1_zen_32'
file_path = '{0}/{1}/{1}'.format(base_path, job_name)
var_name = 'convective_precipitation_rate'
start_time = 6000 * (24 * 60 * 60)
end_time = 10000 * (24 * 60 * 60)

# Procedures
printWindowValues(file_path, var_name, start_time, end_time)













