from sympl import (
    PlotFunctionMonitor, AdamsBashforth, NetCDFMonitor
)
from climt import SimplePhysics, get_default_state
import numpy as np
from datetime import timedelta

from climt import EmanuelConvection, RRTMGShortwave, RRTMGLongwave, SlabSurface
import matplotlib.pyplot as plt

import pandas as pd
from netCDF4 import Dataset as ds


def plot_function(fig, state):
    ax = fig.add_subplot(2, 2, 1)
    ax.plot(
        state['air_temperature_tendency_from_convection'].to_units(
            'degK day^-1').values.flatten(),
        state['air_pressure'].to_units('mbar').values.flatten(), '-o')
    ax.set_title('Conv. heating rate')
    ax.set_xlabel('K/day')
    ax.set_ylabel('millibar')
    ax.grid()
    ax.axes.invert_yaxis()

    ax = fig.add_subplot(2, 2, 2)
    ax.plot(
        state['air_temperature'].values.flatten(),
        state['air_pressure'].to_units('mbar').values.flatten(), '-o')
    ax.set_title('Air temperature')
    ax.axes.invert_yaxis()
    ax.set_xlabel('K')
    ax.grid()

    ax = fig.add_subplot(2, 2, 3)
    ax.plot(
        state['air_temperature_tendency_from_longwave'].values.flatten(),
        state['air_pressure'].to_units('mbar').values.flatten(), '-o',
        label='LW')
    ax.plot(
        state['air_temperature_tendency_from_shortwave'].values.flatten(),
        state['air_pressure'].to_units('mbar').values.flatten(), '-o',
        label='SW')
    ax.set_title('LW and SW Heating rates')
    ax.legend()
    ax.axes.invert_yaxis()
    ax.set_xlabel('K/day')
    ax.grid()
    ax.set_ylabel('millibar')

    ax = fig.add_subplot(2, 2, 4)
    net_flux = (state['upwelling_longwave_flux_in_air'] +
                state['upwelling_shortwave_flux_in_air'] -
                state['downwelling_longwave_flux_in_air'] -
                state['downwelling_shortwave_flux_in_air'])
    ax.plot(
        net_flux.values.flatten(),
        state['air_pressure_on_interface_levels'].to_units(
            'mbar').values.flatten(), '-o')
    ax.set_title('Net Flux')
    ax.axes.invert_yaxis()
    ax.set_xlabel('W/m^2')
    ax.grid()
    plt.tight_layout()


monitor = PlotFunctionMonitor(plot_function, interactive=True)

timestep = timedelta(minutes=5)

convection = EmanuelConvection()
radiation_sw = RRTMGShortwave()
radiation_lw = RRTMGLongwave()
slab = SlabSurface()
simple_physics = SimplePhysics()

store_quantities = ['air_temperature',
                    'surface_temperature',
                    'air_pressure',
                    'specific_humidity',
                    'air_pressure_on_interface_levels',
                    'air_temperature_tendency_from_convection',
                    'air_temperature_tendency_from_longwave',
                    'air_temperature_tendency_from_shortwave',
                    'mole_fraction_of_carbon_dioxide_in_air',
                    'convective_precipitation_rate',
                    'surface_upward_sensible_heat_flux',
                    'surface_upward_latent_heat_flux',
                    'upwelling_longwave_flux_in_air',
                    'upwelling_shortwave_flux_in_air',
                    'downwelling_longwave_flux_in_air',
                    'downwelling_shortwave_flux_in_air']

co2_ppm = 270
run_num = 1
nc_name = 'rad_conv_eq_'+str(co2_ppm)+'_'+str(run_num)+'.nc'

netcdf_monitor = NetCDFMonitor(nc_name,
                               store_names=store_quantities,
                               write_on_store=True)
convection.current_time_step = timestep


state = get_default_state([simple_physics, convection,
                           radiation_lw, radiation_sw, slab])

def getAirTempInitial(type, temp=0, filename=None):
    if type == 'profile':
        return pd.read_csv('TProfile.csv').Kelvin[::-1].values.reshape(28, 1, 1)
    elif type == 'isothermal':
        return temp
    elif type == 'last':
        nc = ds(filename, 'r+', format='NETCDF4')
        return nc['air_temperature'][:][-1]


# air_temp_filename = 'rad_conv_eq_'+str(co2_ppm)+'_'+str(run_num-2)+'.nc'
air_temp_i = getAirTempInitial('isothermal', temp=274)

state['air_temperature'].values[:]                         = air_temp_i
state['surface_albedo_for_direct_shortwave'].values[:]     = 0.06
state['surface_albedo_for_direct_near_infrared'].values[:] = 0.06
state['surface_albedo_for_diffuse_shortwave'].values[:]    = 0.06
state['zenith_angle'].values[:]                            = np.pi/2.5
state['surface_temperature'].values[:]                     = state['air_temperature'].values[0,0,0]
state['ocean_mixed_layer_thickness'].values[:]             = 0.01
state['area_type'].values[:]                               = 'sea'

state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(co2_ppm) * 10**(-6)
state['flux_adjustment_for_earth_sun_distance'].values     = 1.0

time_stepper = AdamsBashforth([convection, radiation_lw, radiation_sw, slab])

for i in range(500000):
    convection.current_time_step = timestep
    diagnostics, state = time_stepper(state, timestep)
    state.update(diagnostics)
    diagnostics, new_state = simple_physics(state, timestep)
    state.update(diagnostics)
    if (i) % 100 == 0:
        monitor.store(state)
        netcdf_monitor.store(state)
        net_flux = (state['upwelling_longwave_flux_in_air'] +
                    state['upwelling_shortwave_flux_in_air'] -
                    state['downwelling_longwave_flux_in_air'] -
                    state['downwelling_shortwave_flux_in_air'])
        net_flux_surface = net_flux.values[0, 0, 0]
        net_flux_toa = net_flux.values[-1, 0, 0]
        print(i)
        print('AIR TEMP:')
        print(state['surface_temperature'].values[0,0])
        print('TOA FLUX')
        print(net_flux_toa)
        print('SURFACE FLUX (incl. LH & SH)')
        print(net_flux_surface +
              state['surface_upward_sensible_heat_flux'].values +
              state['surface_upward_latent_heat_flux'].values)

    state.update(new_state)
    state['time'] += timestep
    state['eastward_wind'].values[:] = 3.
