import copy
from sympl import (
    DataArray, AdamsBashforth, get_constant, set_constant, NetCDFMonitor
)
import numpy as np
from datetime import timedelta
from climt import (
    EmanuelConvection, DryConvectiveAdjustment, GrayLongwaveRadiation,
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

good_quanitites = ['surface_air_pressure',
                   'air_pressure',
                   'air_pressure_on_interface_levels',
                   'air_temperature',
                   'surface_temperature',
                   'specific_humidity',
                   'surface_specific_humidity',
                   'cloud_base_mass_flux',
                   'longwave_optical_depth_on_interface_levels',
                   'downwelling_longwave_flux_in_air',
                   'downwelling_shortwave_flux_in_air',
                   'upwelling_longwave_flux_in_air',
                   'upwelling_shortwave_flux_in_air',
                   'surface_upward_latent_heat_flux',
                   'surface_upward_sensible_heat_flux',
                   'surface_thermal_capacity',
                   'sea_water_density']

netcdf_monitor = NetCDFMonitor(nc_name,
                               store_names=store_quantities,
                               write_on_store=True)

radiation = GrayLongwaveRadiation()
slab = SlabSurface()
simple_physics = SimplePhysics()
moist_convection = EmanuelConvection()
dry_convection = DryConvectiveAdjustment()

state = get_default_state([simple_physics, moist_convection, dry_convection,
                           radiation, slab])

### RESTART VALUES GIVEN FROM THE CONTROL RUN
restart_file_name = '/home/haynes13/climt_files/control_fullstore/' \
                    'i270_320solar_fullstore/i270_320solar_fullstore.eq.pkl'
restart_file = open(restart_file_name, 'rb')
restart_state = pickle.load(restart_file)
control_q = restart_state['specific_humidity'].copy()
control_T = restart_state['air_temperature'].copy()

restart_quantities =  list(restart_state.keys())
print(restart_quantities)

# BECAUSE GRAY RADIATION NEEDS AND DOESN'T ACCEPT DIFFERENT PARAMETERS THAN RRTMG,
# SWITCHING FROM SKIPPING QUANTITIES TO EXCLUSIVELY ADDING THEM BASED ON STORE_QUANTITIES
def setInitValues(state, restart_state, var):
    if var in store_quantities:
        init_val = restart_state[var]
        try:
            state[var].values[:] = init_val
        except:
            print(var)

for var in restart_quantities:
    # print('Setting', var)
    setInitValues(state, restart_state, var)
############################################

# These values are set to match the default values that Shanshan included in her simulations
# state['surface_albedo_for_direct_shortwave'].values[:]      = 0.07
# state['surface_albedo_for_direct_near_infrared'].values[:]  = 0.07
# state['surface_albedo_for_diffuse_shortwave'].values[:]     = 0.07
# state['surface_albedo_for_diffuse_near_infrared'].values[:] = 0.07
# state['zenith_angle'].values[:]                             = (2 * np.pi) / 5
state['area_type'].values[:]                                = 'sea'
# only the surface layer is given a zonal wind to spur convection
state['eastward_wind'].values[0]                            = 5.0
# state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(input_ppm) * 10**(-6)

### FIXED STATE TO UPDATE CONSTANT PROFILES ###
fixed_state = {
    'specific_humidity': copy.deepcopy(state['specific_humidity']),
    'air_temperature': copy.deepcopy(state['air_temperature'])
}
fixed_state['specific_humidity'].values[:] = control_q.copy()
fixed_state['air_temperature'].values[:] = control_T.copy()
state.update(copy.deepcopy(fixed_state))
######################################
time_stepper = AdamsBashforth([radiation, slab, moist_convection])


# Set timestep at 10 minutes
dt_minutes = 10
timestep = timedelta(minutes=dt_minutes)
# Day length to match Shanshan
run_days = 10950
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
