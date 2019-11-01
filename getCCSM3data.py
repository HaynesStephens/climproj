import numpy as np
from netCDF4 import Dataset as ds
import pandas as pd
import copy


def loadLatLonGrid():
    lat = np.array([-87.1590945558629, -83.4789366693172, -79.7770456548256,
    -76.0702444625451, -72.3615810293448, -68.6520167895175,
    -64.9419494887575, -61.2315731880771, -57.52099379797, -53.8102740319414,
    -50.0994534129868, -46.3885581116054, -42.6776061726049,
    -38.966610469454, -35.2555804613682, -31.5445232840217,
    -27.8334444519932, -24.122348326088, -20.4112384335678,
    -16.7001176938427, -12.9889885820881, -9.27785325150786,
    -5.56671362791359, -1.85557148599326, 1.85557148599326, 5.56671362791359,
    9.27785325150786, 12.9889885820881, 16.7001176938427, 20.4112384335678,
    24.122348326088, 27.8334444519932, 31.5445232840217, 35.2555804613682,
    38.966610469454, 42.6776061726049, 46.3885581116054, 50.0994534129868,
    53.8102740319414, 57.52099379797, 61.2315731880771, 64.9419494887575,
    68.6520167895175, 72.3615810293448, 76.0702444625451, 79.7770456548256,
    83.4789366693172, 87.1590945558629])

    lon = np.array([0, 3.75, 7.5, 11.25, 15, 18.75, 22.5, 26.25, 30, 33.75, 37.5, 41.25,
    45, 48.75, 52.5, 56.25, 60, 63.75, 67.5, 71.25, 75, 78.75, 82.5, 86.25,
    90, 93.75, 97.5, 101.25, 105, 108.75, 112.5, 116.25, 120, 123.75, 127.5,
    131.25, 135, 138.75, 142.5, 146.25, 150, 153.75, 157.5, 161.25, 165,
    168.75, 172.5, 176.25, 180, 183.75, 187.5, 191.25, 195, 198.75, 202.5,
    206.25, 210, 213.75, 217.5, 221.25, 225, 228.75, 232.5, 236.25, 240,
    243.75, 247.5, 251.25, 255, 258.75, 262.5, 266.25, 270, 273.75, 277.5,
    281.25, 285, 288.75, 292.5, 296.25, 300, 303.75, 307.5, 311.25, 315,
    318.75, 322.5, 326.25, 330, 333.75, 337.5, 341.25, 345, 348.75, 352.5,
    356.25])

    save_path = '/project2/moyer/old_project/haynes/ccsm3_maps/'
    np.savetxt(save_path + 'Grid.lat.csv', lat, delimiter=',')
    np.savetxt(save_path + 'Grid.lon.csv', lon, delimiter=',')


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
    print('AVERAGING: ', var)
    print('TIME SHAPE: ', avg_var_dict['time'].shape)
    avg_var_dict[var] = var_array[avg_index]
    print('VAR SHAPE: ', avg_var_dict[var].shape)
    avg_var_dict[var+'_avg'] = np.mean(avg_var_dict[var].copy(), axis=0)
    return avg_var_dict


def EQAvgMaps():
    base_path = '/project2/moyer/old_project/climate_data/RDCEP_CCSM3/'
    control_filenames = ['hfls_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'hfss_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'pr1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'pr2_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'psl_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rls_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rlut_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rlutcs_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsds_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsdt_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsus1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsut1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsutcs1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'tas_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'ts_Amon_CCSM3_II_Control_LongRunMIP_3805']
    abrupt700_filenames = ['hfls_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'hfss_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'pr1_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'pr2_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'psl_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rls_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rlut_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rlutcs_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rsds_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rsdt_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rsus1_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rsut1_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'rsutcs1_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'tas_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701',
                        'ts_Amon_CCSM3_II_abrupt700ppm_LongRunMIP_3701']
    abrupt1400_filenames = ['hfls_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'hfss_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'pr1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'pr2_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'psl_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rls_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rlut_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rlutcs_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsds_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsdt_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsus1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsut1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'rsutcs1_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'tas_Amon_CCSM3_II_Control_LongRunMIP_3805',
                        'ts_Amon_CCSM3_II_Control_LongRunMIP_3805']

    filenames = control_filenames + abrupt700_filenames + abrupt1400_filenames
    filepaths = [base_path + name for name in filenames]
    vars = [name.split('_')[0] for name in filenames]

    def getNCdict(filepath, var):
        var_dict = {}
        var_nc = openNC(filepath)
        var_dict[var] = var_nc[var][:]
        var_dict['time'] = var_nc['time'][:]
        return var_dict

    var_dicts = [getNCdict(filepath, var) for filepath,var in zip(filepaths,vars)]
    avg_var_dicts = [EQavg(var_dict, var) for var_dict,var in zip(var_dicts, vars)]
    avg_var_maps = [avg_var_dict[var+'_avg'] for avg_var_dict,var in zip(avg_var_dicts, vars)]
    save_path = '/home/haynes13/ccsm3_maps/'
    save_filepaths = [save_path + name + '.avgMap.csv' for name in filenames]
    save_avg_var_maps = [np.savetxt(name, data, delimiter=',') for name,data in zip(save_filepaths, avg_var_maps)]
    print_names = [print(name) for name in save_filepaths]
    return avg_var_maps





def ShanshanEQFig4():
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





