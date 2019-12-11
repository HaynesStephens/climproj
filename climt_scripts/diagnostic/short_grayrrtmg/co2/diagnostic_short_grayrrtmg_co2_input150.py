### UNIQUE VALUES ###
irradiance = 1036
#insol = 320
input_ppm = 150
nc_name = 'diagnostic_short_grayrrtmg_co2_input150.nc'
#####################
import copy
from sympl import (
    DataArray, AdamsBashforth, get_constant, set_constant, NetCDFMonitor
)
import numpy as np
from datetime import timedelta
from climt import (
    EmanuelConvection, DryConvectiveAdjustment, RRTMGShortwave, GrayLongwaveRadiation,
    SlabSurface, SimplePhysics, get_default_state
)
import pickle

set_constant('stellar_irradiance', value=irradiance, units='W m^-2')
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
                    'stratiform_precipitation_rate',
                    'surface_upward_sensible_heat_flux',
                    'surface_upward_latent_heat_flux',
                    'upwelling_longwave_flux_in_air',
                    'upwelling_shortwave_flux_in_air',
                    'downwelling_longwave_flux_in_air',
                    'downwelling_shortwave_flux_in_air']

netcdf_monitor = NetCDFMonitor(nc_name,
                               store_names=store_quantities,
                               write_on_store=True)

radiation_sw = RRTMGShortwave(ignore_day_of_year=True)
radiation_lw = GrayLongwaveRadiation()
slab = SlabSurface()
simple_physics = SimplePhysics()
moist_convection = EmanuelConvection()
dry_convection = DryConvectiveAdjustment()

state = get_default_state([simple_physics, moist_convection, dry_convection,
                           radiation_lw, radiation_sw, slab])

### RESTART VALUES GIVEN FROM THE CONTROL RUN
restart_file_name = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/' \
                    'i270_320solar_fullstore/i270_320solar_fullstore_pkl_eq.pkl'
restart_file = open(restart_file_name, 'rb')
restart_state = pickle.load(restart_file)
control_q = restart_state['specific_humidity'].copy()
control_T = restart_state['air_temperature'].copy()
control_Tsurf = restart_state['surface_temperature'].copy()

restart_quantities =  list(restart_state.keys())
print(restart_quantities)
skip_quantities = ['convective_downdraft_specific_humidity_scale',
                   'time',
                   'upwelling_longwave_flux_in_air_assuming_clear_sky',
                   'downwelling_longwave_flux_in_air_assuming_clear_sky',
                   'air_temperature_tendency_from_longwave_assuming_clear_sky',
                   'air_temperature_tendency_from_longwave',
                   'upwelling_shortwave_flux_in_air_assuming_clear_sky',
                   'downwelling_shortwave_flux_in_air_assuming_clear_sky',
                   'air_temperature_tendency_from_shortwave_assuming_clear_sky',
                   'air_temperature_tendency_from_shortwave',
                   'depth_of_slab_surface',
                   'convective_state',
                   'convective_precipitation_rate',
                   'convective_downdraft_velocity_scale',
                   'convective_downdraft_temperature_scale',
                   'atmosphere_convective_available_potential_energy',
                   'air_temperature_tendency_from_convection',
                   'stratiform_precipitation_rate',
                   'surface_longwave_emissivity',
                   'mole_fraction_of_cfc22_in_air',
                   'mole_fraction_of_carbon_tetrachloride_in_air',
                   'mole_fraction_of_cfc12_in_air',
                   'longwave_optical_thickness_due_to_aerosol',
                   'longwave_optical_thickness_due_to_cloud',
                   'mole_fraction_of_cfc11_in_air']

def setInitValues(state, restart_state, var):
    if var not in skip_quantities:
        init_val = restart_state[var]
        state[var].values[:] = init_val

for var in restart_quantities:
    print('Setting', var)
    setInitValues(state, restart_state, var)
############################################

# These values are set to match the default values that Shanshan included in her simulations
state['surface_albedo_for_direct_shortwave'].values[:]      = 0.07
state['surface_albedo_for_direct_near_infrared'].values[:]  = 0.07
state['surface_albedo_for_diffuse_shortwave'].values[:]     = 0.07
state['surface_albedo_for_diffuse_near_infrared'].values[:] = 0.07
state['zenith_angle'].values[:]                             = (2 * np.pi) / 5
state['area_type'].values[:]                                = 'sea'
# only the surface layer is given a zonal wind to spur convection
state['eastward_wind'].values[0]                            = 5.0
state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(input_ppm) * 10**(-6)

### FIXED STATE TO UPDATE CONSTANT PROFILES ###
fixed_state = {
    'specific_humidity': copy.deepcopy(state['specific_humidity']),
    'air_temperature': copy.deepcopy(state['air_temperature']),
    'surface_temperature': copy.deepcopy(state['surface_temperature'])
}
fixed_state['specific_humidity'].values[:] = control_q
fixed_state['air_temperature'].values[:] = control_T
fixed_state['surface_temperature'].values[:] = control_Tsurf
state.update(copy.deepcopy(fixed_state))
######################################
time_stepper = AdamsBashforth([radiation_lw, radiation_sw, slab, moist_convection])


# Set timestep at 10 minutes
dt_minutes = 10
timestep = timedelta(minutes=dt_minutes)
# Day length to match Shanshan
run_days = 1000
run_length = int((run_days * 24 * 60) / dt_minutes)

for i in range(run_length):
    diagnostics, state = time_stepper(state, timestep)
    state.update(diagnostics)
    state.update(copy.deepcopy(fixed_state))

    diagnostics, new_state = simple_physics(state, timestep)
    state.update(diagnostics)
    state.update(copy.deepcopy(fixed_state))

    state.update(new_state)  #Update new simple_physics state   # These lines included w/
    state.update(copy.deepcopy(fixed_state))                    # the Dry Convective Scheme,

    diagnostics, new_state = dry_convection(state, timestep)    # Introduced for
    state.update(diagnostics)                                   # More realistic temperature profile
    state.update(copy.deepcopy(fixed_state))

    if (i % 36 == 0):
        netcdf_monitor.store(state)

    state.update(new_state)
    state['time'] += timestep
    state['eastward_wind'].values[0] = 5.0 # default value of old climt turbulence that Shanshan didn't seem to change
