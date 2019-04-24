import numpy as np
from netCDF4 import Dataset as ds
import matplotlib.pyplot as plt

def getNC(filename):
    return ds(filename, 'r+', format='NETCDF4')

def plot_time_series(filename):
    nc = getNC(filename)
    time_arr = nc['time'][:]
    lh_flux = nc['surface_upward_latent_heat_flux'][:].flatten()
    sh_flux = nc['surface_upward_sensible_heat_flux'][:].flatten()
    precip = nc['convective_precipitation_rate'][:].flatten()
    co2_ppm = nc['mole_fraction_of_carbon_dioxide_in_air'][:].flatten()[0]

    net_flux = (nc['upwelling_longwave_flux_in_air'][:] +
                nc['upwelling_shortwave_flux_in_air'][:] -
                nc['downwelling_longwave_flux_in_air'][:] -
                nc['downwelling_shortwave_flux_in_air'][:]).flatten()

    fig, axes = plt.subplots(2,2)
    ax0 = axes[0,0]
    ax0.plot(net_flux, nc['air_pressure_on_interface_levels'][:].flatten(), '-o')
    ax0.set_title('Net Flux')
    ax0.axes.invert_yaxis()
    ax0.set_xlabel('W/m^2')
    ax0.set_ylabel('Pa')
    ax0.grid()

    plt.tight_layout()
    plt.savefig('test.pdf')
    plt.show()


plot_time_series('rad_conv_eq.nc')
