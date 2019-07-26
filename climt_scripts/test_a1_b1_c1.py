from sympl import (
    DataArray, AdamsBashforth, get_constant, set_constant, NetCDFMonitor
)
import numpy as np
from datetime import timedelta

from climt import (
    EmanuelConvection, RRTMGShortwave, RRTMGLongwave,
    SlabSurface, SimplePhysics, get_default_state
)
# a1 = State[‘time’] gets updated
# b1 = Time_stepper before sympl_physics
# c1 = Diagnostics updated before state
#############################
# PARAMETERS/NAMES TO ALTER #
#############################
co2_ppm = 270
nc_name = 'test_a1_b1_c1.nc'
set_constant('stellar_irradiance', value=290, units='W m^-2')
#############################


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

netcdf_monitor = NetCDFMonitor(nc_name,
                               store_names=store_quantities,
                               write_on_store=True)

dt_minutes = 10
timestep = timedelta(minutes=dt_minutes)

radiation_sw = RRTMGShortwave()
radiation_lw = RRTMGLongwave()
slab = SlabSurface()
simple_physics = SimplePhysics()
moist_convection = EmanuelConvection()

state = get_default_state([simple_physics, moist_convection,
                           radiation_lw, radiation_sw, slab])


state['air_temperature'].values[:]                          = 283.15
state['surface_albedo_for_direct_shortwave'].values[:]      = 0.07
state['surface_albedo_for_direct_near_infrared'].values[:]  = 0.07
state['surface_albedo_for_diffuse_shortwave'].values[:]     = 0.07
state['surface_albedo_for_diffuse_near_infrared'].values[:] = 0.07
state['zenith_angle'].values[:]                             = (2 * np.pi) / 5
state['surface_temperature'].values[:]                      = state['air_temperature'].values[0,0,0]
state['area_type'].values[:]                                = 'sea'

state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(co2_ppm) * 10**(-6)


time_stepper = AdamsBashforth([radiation_lw, radiation_sw, slab, moist_convection])
old_enthalpy = calc_moist_enthalpy(state)

run_days = 10950
run_length = int((run_days * 24 * 60) / dt_minutes)

for i in range(run_length):
    diagnostics, state = time_stepper(state, timestep)
    state.update(diagnostics)

    diagnostics, new_state = simple_physics(state, timestep)
    state.update(diagnostics)

    if (i % 100 == 0) or (i == run_length - 1):
        netcdf_monitor.store(state)

        surf_flux_to_col = -(state['downwelling_shortwave_flux_in_air'][0] +
                             state['downwelling_longwave_flux_in_air'][0] -
                             state['upwelling_shortwave_flux_in_air'][0] -
                             state['upwelling_longwave_flux_in_air'][0] -
                             state['surface_upward_sensible_heat_flux'] -
                             state['surface_upward_latent_heat_flux']).values

        toa_flux_to_col = (state['downwelling_shortwave_flux_in_air'][-1] -
                           state['upwelling_shortwave_flux_in_air'][-1] -
                           state['upwelling_longwave_flux_in_air'][-1]).values

        total_heat_gain = surf_flux_to_col + toa_flux_to_col
        current_enthalpy = calc_moist_enthalpy(state)
        enthalpy_gain = current_enthalpy - old_enthalpy
        old_enthalpy = current_enthalpy

        print(i)
        print('Forcing and Column integral: ', total_heat_gain, enthalpy_gain / timestep.total_seconds())
        print('TOA flux:', toa_flux_to_col)
        print('Surf flux:', surf_flux_to_col)

    state.update(new_state)
    state['time'] += timestep
    state['eastward_wind'].values[:] = 5.
