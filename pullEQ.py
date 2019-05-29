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
    arr_size = net_flux_surface.size
    for i in range(arr_size - eq_time):
        if (inEQ(net_flux_surface[i:i + eq_time], eq_threshold) and
                inEQ(net_flux_toa[i:i + eq_time], eq_threshold)):
            print('SUCCESS')
            return i
    raise (ValueError, 'No equilibrium reached.')


def pullEQData(filename, var, eq_time = 15, eq_threshold = 1):
    nc = getNC(filename)
    eq_index = checkEQ(nc, eq_time, eq_threshold)
    return nc[var][:][eq_index: eq_index+eq_time]


# PLOTS
filename150 = 'CLTMC_150_0.nc'
filename270 = 'CLTMC_270_0.nc'
filename600 = 'CLTMC_600_0.nc'
air_pressure = getNC(filename150)['air_pressure'][:][0].flatten()

def plotProfile(var, xlabel):
    var_150 = np.mean(pullEQData(filename150, var), axis=0).flatten()
    var_270 = np.mean(pullEQData(filename270, var), axis=0).flatten()
    var_600 = np.mean(pullEQData(filename600, var), axis=0).flatten()
    fig, ax = plt.subplots(figsize=(4,5))
    ax.plot(var_150, air_pressure, '-o', markersize=1, label = '150 ppm')
    ax.plot(var_270, air_pressure, '-o', markersize=1, label = '270 ppm')
    ax.plot(var_600, air_pressure, '-o', markersize=1, label = '600 ppm')
    ax.set_xlabel(xlabel)

    if var == 'air_temperature':
        Tsurf = var_150[0]
        z, T_dry = getAdiabat(Tsurf, 'dry')
        z, T_moist = getAdiabat(Tsurf, 'moist')
        ax.plot(T_dry, air_pressure, '-.', label = 'dry', c = 'k')
        ax.plot(T_moist, air_pressure, '--', label='moist', c = 'k')
        ax.set_xlim(190,290)

    ax.set_ylabel('Pressure [Pa]')
    ax.set_yscale('log')
    ax.invert_yaxis()
    ax.legend()
    plt.tight_layout()
    plt.savefig('plots/profile_{0}.pdf'.format(var))
    plt.show()


def getAVG(var, units):
    var_150 = np.mean(pullEQData(filename150, var), axis=0)
    var_270 = np.mean(pullEQData(filename270, var), axis=0)
    var_600 = np.mean(pullEQData(filename600, var), axis=0)
    print('150 ppm: {0} {1}'.format(var_150, units))
    print('270 ppm: {0} {1}'.format(var_270, units))
    print('600 ppm: {0} {1}'.format(var_600, units))

def plotProfile2(var1 = 'air_temperature',
                 xlabel1 = '[K]',
                 var2 = 'specific_humidity',
                 xlabel2 = '[kg/kg]'):

    fig, axes = plt.subplots(1, 2, figsize=(10,5))


    T_150 = np.mean(pullEQData(filename150, var1), axis=0).flatten()
    T_270 = np.mean(pullEQData(filename270, var1), axis=0).flatten()
    T_600 = np.mean(pullEQData(filename600, var1), axis=0).flatten()
    ax1 = axes[0]
    ax1.plot(T_150, air_pressure, '-o', markersize=3, label = '150 ppm')
    ax1.plot(T_270, air_pressure, '-o', markersize=3, label = '270 ppm')
    ax1.plot(T_600, air_pressure, '-o', markersize=3, label = '600 ppm')
    ax1.set_ylabel('Pressure [Pa]')
    ax1.set_xlabel(xlabel1)
    ax1.set_yscale('log')
    ax1.invert_yaxis()
    ax1.legend()

    q_150 = np.mean(pullEQData(filename150, var2), axis=0).flatten()
    q_270 = np.mean(pullEQData(filename270, var2), axis=0).flatten()
    q_600 = np.mean(pullEQData(filename600, var2), axis=0).flatten()
    ax2 = axes[1]
    ax2.plot(q_150, air_pressure, '-o', markersize=3, label = '150 ppm')
    ax2.plot(q_270, air_pressure, '-o', markersize=3, label = '270 ppm')
    ax2.plot(q_600, air_pressure, '-o', markersize=3, label = '600 ppm')
    # ax2.set_ylabel('Pressure [Pa]')
    ax2.set_xlabel(xlabel2)
    ax2.invert_yaxis()

    plt.tight_layout()
    plt.savefig('plots/profile2.pdf')
    plt.show()


def getAdiabat(Tsurf, type = 'dry'):
    z = []
    H = 8.5 #scale height in km
    P0 = air_pressure[0]
    for P in air_pressure:
        height = -H*np.log(P/P0)
        z.append(height)
    z = np.array(z)
    if type == 'dry':
        gamma = 9.8 #K/km
    elif type == 'moist':
        gamma = 5 #K/km
    T_profile = [Tsurf]
    for i in range(1,z.size):
        height = z[i]
        T_profile.append(Tsurf - (height*gamma))
    T_profile = np.array(T_profile)
    return z, T_profile


plotProfile('air_temperature', '[K]')





