import numpy as np
from netCDF4 import Dataset as ds
import matplotlib.pyplot as plt

def getNC(filename):
    return ds(filename, 'r+', format='NETCDF4')

def getLastInstance(data, levels = None):
    if levels is None:
        return data[:].flatten()[-1]
    else:
        return data[:].flatten()[-levels:]


def plot_time_series(job_name):
    base_name = '/home/haynes13/climt_files/'
    file_name = '{0}{1}/{1}.nc'.format(base_name, job_name)
    plot_name = 'saved_plots/{0}/{0}_time_series.pdf'.format(job_name)

    mid_levels = 28
    interface_levels = 29

    nc = getNC(file_name)
    time_arr = nc['time'][:]
    time_arr = np.arange(nc['time'][:].size)*100*10*60
    print(nc['time'][:].size)
    time_adj = time_arr / (3600 * 24)
    time_title = 'Days'
    lh_flux = nc['surface_upward_latent_heat_flux'][:].flatten()
    sh_flux = nc['surface_upward_sensible_heat_flux'][:].flatten()
    precip = nc['convective_precipitation_rate'][:].flatten()
    co2_ppm = nc['mole_fraction_of_carbon_dioxide_in_air'][:].flatten()[0] * (10**6)

    net_flux = (nc['upwelling_longwave_flux_in_air'][:] +
                nc['upwelling_shortwave_flux_in_air'][:] -
                nc['downwelling_longwave_flux_in_air'][:] -
                nc['downwelling_shortwave_flux_in_air'][:])

    net_flux_surface = net_flux[:, 0, 0, 0]
    net_flux_toa = net_flux[:,-1,0,0]

    fig, axes = plt.subplots(2,2)

    ax0 = axes[0,0]
    ax0.plot(getLastInstance(net_flux, interface_levels),
             getLastInstance(nc['air_pressure_on_interface_levels'], interface_levels), '-o',
             markersize=3, c='k')
    ax0.set_title('Net Rad Flux (Up is +)')
    ax0.axes.invert_yaxis()
    ax0.set_xlabel('W/m^2')
    ax0.set_ylabel('Pa')
    ax0.grid()

    ax1 = axes[0,1]
    ax1.plot(getLastInstance(nc['air_temperature'], mid_levels),
             getLastInstance(nc['air_pressure'], mid_levels), '-o', markersize=3, c='k')
    ax1.set_title('Temperature')
    ax1.axes.invert_yaxis()
    ax1.set_xlabel('K')
    ax1.set_ylabel('Pa')
    ax1.grid()

    ax2 = axes[1, 0]
    ax2.plot(time_adj, precip, '-', c='b')
    ax2.set_title('Precipitation / LH Flux')
    ax2.set_xlabel(time_title)
    ax2.set_ylabel('mm/day')

    ax2b = ax2.twinx()
    ax2b.plot(time_adj, lh_flux, '-.', c='y')
    ax2b.set_ylabel('W/m^2')

    ax2.grid()

    ax3 = axes[1, 1]
    # ax3.plot(time_adj, net_flux_surface, c = 'y', label='Rad')
    # ax3.plot(time_adj, sh_flux, c = 'r', label = 'SH')
    # ax3.plot(time_adj, lh_flux, c = 'b', label = 'LH')
    ax3.plot(time_adj, net_flux_toa, c='#d95f02', label='TOA')
    ax3.plot(time_adj, net_flux_surface + lh_flux + sh_flux, c='#7570b3', label = 'Surf')
    ax3.set_title('Boundary Fluxes (Up is +)')
    ax3.set_xlabel(time_title)
    ax3.set_ylabel('W/m^2')
    # ax3.set_ylim(-50, 250)
    ax3.legend()
    ax3.grid()

    fig.suptitle('CO$_2$: {0} ppm'.format(co2_ppm//1), fontsize = 10,
                 bbox=dict(facecolor='none', edgecolor='green'),
                 x=0.55, y=0.525)
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()

for ai in range(1,3):
    for bi in range(1,3):
        for ci in range(1,3):
            plot_time_series(job_name = 'test_a{0}_b{1}_c{2}'.format(ai, bi, ci))
