import numpy as np
from netCDF4 import Dataset as ds
import matplotlib.pyplot as plt


def getNC(filename):
    return ds(filename, 'r+', format='NETCDF4')


def getTimeArr(nc, timestep_minutes= 10, step_size = 100):
    time_arr_seconds = np.arange(nc['time'][:].size)* step_size * timestep_minutes *60
    time_arr_days = time_arr_seconds / (3600 * 24)
    return time_arr_days


def inEQ(data, threshold):
    return np.mean(data) < threshold


def checkEQ(nc, eq_time, eq_threshold):
    lh_flux = nc['surface_upward_latent_heat_flux'][:].flatten()
    sh_flux = nc['surface_upward_sensible_heat_flux'][:].flatten()
    net_flux = (nc['upwelling_longwave_flux_in_air'][:] +
                nc['upwelling_shortwave_flux_in_air'][:] -
                nc['downwelling_longwave_flux_in_air'][:] -
                nc['downwelling_shortwave_flux_in_air'][:])
    net_flux_surface = net_flux[:, 0, 0, 0] + sh_flux + lh_flux
    net_flux_toa = net_flux[:, -1, 0, 0]

    assert net_flux_toa.size == net_flux_surface.size
    for i in range(n[0].size - eq_time):
        if (inEQ(net_flux_surface[i:i + eq_time], eq_threshold) and
                inEQ(net_flux_toa[i:i + eq_time], eq_threshold)):
            print('SUCCESS')
            return i
    raise (ValueError, 'No equilibrium reached.')


def pullEQData(filename, var, bad_shape = False, eq_time = 15, eq_threshold = 1,
               mid_levels=28, interface_levels=29):

    nc = getNC(filename+'.nc')
    eq_index = checkEQ(nc, eq_time, eq_threshold)

    # data = nc[var][:]


pullEQData('CLTMC_270_0', var='lame')







