from sympl import (
    DataArray, AdamsBashforth, get_constant, set_constant, NetCDFMonitor
)
import numpy as np
from datetime import timedelta

from climt import (
    EmanuelConvection, DryConvectiveAdjustment, RRTMGShortwave, RRTMGLongwave,
    SlabSurface, SimplePhysics, get_default_state
)

import pickle

#############################
# PARAMETERS/NAMES TO ALTER #
#############################
nc_name = 'test.nc'
co2_ppm = 270
set_constant('stellar_irradiance', value=939, units='W m^-2')
# Solar insolation set to 939 and zenith angle kept to default,
#           to match the earlier 'solin' value of 290 that Shanshan used.
#############################

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

### RESTART VALUES GIVEN FROM THE CONTROL RUN
restart_file_name = '/home/haynes13/climt_files/control/i270_290solar/i270_290solar/i270_290solar_restart_state.pkl'
restart_file = open(restart_file_name, 'rb')
restart_state = pickle.load(restart_file)

def setInitValues(state, restart_state, var):
    try:
        init_val = restart_state[var]
        state[var].values[:] = init_val
    except:
        print("No Dice:", var)



# These values are set to match the default values that Shanshan included in her simulations
# state['air_temperature'].values[:]                          = restart_state['air_temperature'].reshape(28, 1, 1)
state['surface_albedo_for_direct_shortwave'].values[:]      = 0.07
state['surface_albedo_for_direct_near_infrared'].values[:]  = 0.07
state['surface_albedo_for_diffuse_shortwave'].values[:]     = 0.07
state['surface_albedo_for_diffuse_near_infrared'].values[:] = 0.07
state['zenith_angle'].values[:]                             = (2 * np.pi) / 5
# state['surface_temperature'].values[:]                      = state['air_temperature'].values[0,0,0]
state['area_type'].values[:]                                = 'sea'
# only the surface layer is given a zonal wind to spur convection
state['eastward_wind'].values[0]                            = 5.0

state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(co2_ppm) * 10**(-6)

for var in store_quantities:
    print('Setting', var)
    setInitValues(state, restart_state, var)
