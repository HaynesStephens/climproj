import numpy as np
from netCDF4 import Dataset as ds
import matplotlib.pyplot as plt

def getNC(filename):
    return ds(filename, 'r+', format='NETCDF4')

def plot_time_series(filename):
    mid_levels = 28
    interface_levels = 29
    def getLastInstance(data, levels = None):
        if levels is None:
            return data[:].flatten()[-1]
        else:
            return data[:].flatten()[-levels:]

    nc = getNC(filename)
    time_arr = nc['time'][:]
    lh_flux = nc['surface_upward_latent_heat_flux'][:].flatten()
    sh_flux = nc['surface_upward_sensible_heat_flux'][:].flatten()
    precip = nc['convective_precipitation_rate'][:].flatten()
    co2_ppm = nc['mole_fraction_of_carbon_dioxide_in_air'][:].flatten()[0] * (10**6)

    net_flux = (getLastInstance(nc['upwelling_longwave_flux_in_air'], interface_levels) +
                getLastInstance(nc['upwelling_shortwave_flux_in_air'], interface_levels) -
                getLastInstance(nc['downwelling_longwave_flux_in_air'], interface_levels) -
                getLastInstance(nc['downwelling_shortwave_flux_in_air'], interface_levels))

    fig, axes = plt.subplots(2,2)

    ax0 = axes[0,0]
    ax0.plot(net_flux, getLastInstance(nc['air_pressure_on_interface_levels'], interface_levels), '-')
    ax0.set_title('Net Flux')
    ax0.axes.invert_yaxis()
    ax0.set_xlabel('W/m^2')
    ax0.set_ylabel('Pa')
    ax0.grid()

    ax1 = axes[0, 1]
    ax1.plot(time_arr/60, precip, '-')
    ax1.set_title('Precipitation')
    ax1.set_xlabel('Minutes')
    ax1.set_ylabel('mm/day')
    ax1.grid()

    ax2 = axes[1, 0]
    ax2.plot(time_arr/60, lh_flux, '-')
    ax2.set_title('Latent Heat Flux')
    ax2.set_xlabel('Minutes')
    ax2.set_ylabel('W/m^2')
    ax2.grid()

    ax3 = axes[1, 1]
    ax3.plot(time_arr/60, sh_flux, '-')
    ax3.set_title('Sensible Heat Flux')
    ax3.set_xlabel('Minutes')
    ax3.set_ylabel('W/m^2')
    ax3.grid()

    fig.suptitle('CO$_2$: {0} ppm'.format(co2_ppm//1), fontsize = 10,
                 bbox=dict(facecolor='none', edgecolor='green'))
    plt.tight_layout()
    plt.savefig('test_800.pdf')
    plt.show()


plot_time_series('rad_conv_eq_800.nc')
