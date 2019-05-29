from sympl import (
    DataArray, PlotFunctionMonitor,
    AdamsBashforth, get_constant, NetCDFMonitor
)
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt

from climt import (
    EmanuelConvection, RRTMGShortwave, RRTMGLongwave, SlabSurface,
    DryConvectiveAdjustment, SimplePhysics, get_default_state
)


Cpd = get_constant('heat_capacity_of_dry_air_at_constant_pressure', 'J/kg/degK')
Cvap = get_constant('heat_capacity_of_vapor_phase', 'J/kg/K')
g = get_constant('gravitational_acceleration', 'm/s^2')
Lv = get_constant('latent_heat_of_condensation', 'J/kg')


def heat_capacity(q):
    return Cpd * (1 - q) + Cvap * q


def calc_moist_enthalpy(state):
    dp = (state['air_pressure_on_interface_levels'][:-1] - state['air_pressure_on_interface_levels'][1:]).rename(
        dict(interface_levels='mid_levels'))

    C_tot = heat_capacity(state['specific_humidity'])

    return ((C_tot * state['air_temperature'] + Lv * state['specific_humidity']) * dp / g).sum().values


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

store_quantities = ['air_temperature',
                    'stratiform_precipitation_rate', #!!!!
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

netcdf_monitor = NetCDFMonitor('CLTMC_300_last.nc',
                               store_names=store_quantities,
                               write_on_store=True)

timestep = timedelta(minutes=10)

radiation_sw = RRTMGShortwave()
radiation_lw = RRTMGLongwave()
slab = SlabSurface()
simple_physics = SimplePhysics()
dry_convection = DryConvectiveAdjustment()
moist_convection = EmanuelConvection()

state = get_default_state(
    [simple_physics, dry_convection, moist_convection,
     radiation_lw, radiation_sw, slab]
)


state['surface_temperature'].values[:] = 268.

state['air_temperature'].values[:] = 260
state['surface_albedo_for_direct_shortwave'].values[:] = 0.4
state['surface_albedo_for_direct_near_infrared'].values[:] = 0.4
state['surface_albedo_for_diffuse_shortwave'].values[:] = 0.4
# Changing of default
state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(300) * 10**(-6)

state['zenith_angle'].values[:] = np.pi / 2.45

state['ocean_mixed_layer_thickness'].values[:] = .01
state['area_type'].values[:] = 'sea'

time_stepper = AdamsBashforth([radiation_lw, radiation_sw, slab, moist_convection])

old_enthalpy = calc_moist_enthalpy(state)

for i in range(100000):
    diagnostics, new_state = simple_physics(state, timestep)
    state.update(diagnostics)
    state.update(new_state)

    diagnostics, state = time_stepper(state, timestep)
    state.update(diagnostics)

    diagnostics, new_state = dry_convection(state, timestep)
    state.update(diagnostics)
    state.update(new_state)

    surf_flux_to_col = -(state['downwelling_shortwave_flux_in_air'][0] +
                         state['downwelling_longwave_flux_in_air'][0] -
                         state['upwelling_shortwave_flux_in_air'][0] -
                         state['upwelling_longwave_flux_in_air'][0] -
                         state['surface_upward_sensible_heat_flux'] -
                         state['surface_upward_latent_heat_flux']).values

    toa_flux_to_col = (state['downwelling_shortwave_flux_in_air'][-1] +
                         state['downwelling_longwave_flux_in_air'][-1] -
                         state['upwelling_shortwave_flux_in_air'][-1] -
                         state['upwelling_longwave_flux_in_air'][-1]).values

    # print('TOA flux:', toa_flux_to_col)
    # print('Surf flux:', surf_flux_to_col)

    total_heat_gain = surf_flux_to_col + toa_flux_to_col
    current_enthalpy = calc_moist_enthalpy(state)
    enthalpy_gain = current_enthalpy - old_enthalpy
    old_enthalpy = current_enthalpy

    if i % 100 == 0:
        monitor.store(state)
        netcdf_monitor.store(state)

        print(i)
        print('Forcing and Column integral: ', total_heat_gain, enthalpy_gain / timestep.total_seconds())
        print('TOA flux:', toa_flux_to_col)
        print('Surf flux:', surf_flux_to_col)

    state.update(new_state)
    # state['time'] += timestep
    state['eastward_wind'].values[:] = 3.
