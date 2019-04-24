import numpy as np
from netCDF4 import Dataset as ds
import matplotlib.pyplot as plt

def getNC(filename):
    return ds(filename, 'r+', format='NETCDF4')

def plot_time_series(filename):
    nc = getNC(filename)
    time_arr = nc['time'][:]
    ax0, fig = plt.subplots((1,1))
    ax0.plot(time_arr, nc['surface_upward_latent_heat_flux'][:].flatten())
    plt.savefig('test.pdf')
    plt.show()


plot_time_series('rad_conv_eq.nc')
