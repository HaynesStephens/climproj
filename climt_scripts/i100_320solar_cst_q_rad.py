### UNIQUE VALUES ###
irradiance = 1036
#insol = 320
co2_ppm = 100
nc_name = 'i100_320solar_cst_q_rad.nc'
#####################
import copy
from sympl import (
    DataArray, AdamsBashforth, get_constant, set_constant, NetCDFMonitor, PlotFunctionMonitor
)
import numpy as np
from datetime import timedelta
from climt import (
    EmanuelConvection, DryConvectiveAdjustment, RRTMGShortwave, RRTMGLongwave,
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

# Set timestep at 10 minutes
dt_minutes = 10
timestep = timedelta(minutes=dt_minutes)

radiation_sw = RRTMGShortwave(ignore_day_of_year=True)
radiation_lw = RRTMGLongwave()
slab = SlabSurface()
simple_physics = SimplePhysics()
moist_convection = EmanuelConvection()
dry_convection = DryConvectiveAdjustment()

state = get_default_state([simple_physics, moist_convection, dry_convection,
                           radiation_lw, radiation_sw, slab])

# These values are set to match the default values that Shanshan included in her simulations
state['surface_albedo_for_direct_shortwave'].values[:]      = 0.07
state['surface_albedo_for_direct_near_infrared'].values[:]  = 0.07
state['surface_albedo_for_diffuse_shortwave'].values[:]     = 0.07
state['surface_albedo_for_diffuse_near_infrared'].values[:] = 0.07
state['zenith_angle'].values[:]                             = (2 * np.pi) / 5
state['area_type'].values[:]                                = 'sea'
# only the surface layer is given a zonal wind to spur convection
state['eastward_wind'].values[0]                            = 5.0
state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(co2_ppm) * 10**(-6)

### RESTART VALUES GIVEN FROM THE CONTROL RUN
restart_file_name = '/project2/moyer/old_project/haynes/climt_files/control/' \
                    'i270_290solar/i270_290solar_restart_state.pkl'
restart_file = open(restart_file_name, 'rb')
restart_state = pickle.load(restart_file)
control_q = restart_state['specific_humidity'].copy()

restart_quantities =    ['air_temperature',
                        'surface_temperature',
                        'air_pressure',
                        'specific_humidity',
                        'air_pressure_on_interface_levels',
                        'surface_upward_sensible_heat_flux',
                        'surface_upward_latent_heat_flux',
                        'upwelling_longwave_flux_in_air',
                        'upwelling_shortwave_flux_in_air',
                        'downwelling_longwave_flux_in_air',
                        'downwelling_shortwave_flux_in_air']

def setInitValues(state, restart_state, var):
    init_val = restart_state[var].copy()
    state[var].values[:] = init_val

for var in restart_quantities:
    print('Setting', var)
    setInitValues(state, restart_state, var)

time_stepper_phys = AdamsBashforth([slab, moist_convection])
time_stepper_rad = AdamsBashforth([radiation_lw, radiation_sw])

# Day length to match Shanshan
run_days = 10950
run_length = int((run_days * 24 * 60) / dt_minutes)

for i in range(run_length):
    rad_state_fixed_q = copy.deepcopy(state)
    phys_unfixed_q = rad_state_fixed_q['specific_humidity'].values[:].copy()
    rad_state_fixed_q['specific_humidity'].values[:] = control_q.copy()
    diagnostics, state = time_stepper_rad(rad_state_fixed_q, timestep)
    state['specific_humidity'].values[:] = phys_unfixed_q.copy()
    state.update(diagnostics)

    diagnostics, state = time_stepper_phys(state, timestep)
    state.update(diagnostics)

    diagnostics, new_state = simple_physics(state, timestep)
    state.update(diagnostics)
    state.update(new_state)  #Update new simple_physics state   # These lines included w/
                                                                # the Dry Convective Scheme,
    diagnostics, new_state = dry_convection(state, timestep)    # Introduced for
    state.update(diagnostics)                                   # More realistic temperature profile

    if (i % 36 == 0):
        netcdf_monitor.store(state)

    state.update(new_state)
    state['time'] += timestep
    state['eastward_wind'].values[0] = 5.0
    #^ default value of old climt turbulence that Shanshan didn't seem to change
