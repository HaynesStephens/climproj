### UNIQUE VALUES ###
irradiance = 939
#insol = 290
co2_ppm = 270
nc_name = 'scratch_270_290.nc'
#####################
from sympl import (
    DataArray, AdamsBashforth, get_constant, set_constant, NetCDFMonitor, PlotFunctionMonitor
)
import numpy as np
from datetime import timedelta
from climt import (
    EmanuelConvection, DryConvectiveAdjustment, RRTMGShortwave, RRTMGLongwave,
    SlabSurface, SimplePhysics, get_default_state
)

set_constant('stellar_irradiance', value=irradiance, units='W m^-2')

netcdf_monitor = NetCDFMonitor(nc_name, write_on_store=True)

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
state['air_temperature'].values[:]                          = 283.15
state['surface_albedo_for_direct_shortwave'].values[:]      = 0.07
state['surface_albedo_for_direct_near_infrared'].values[:]  = 0.07
state['surface_albedo_for_diffuse_shortwave'].values[:]     = 0.07
state['surface_albedo_for_diffuse_near_infrared'].values[:] = 0.07
state['zenith_angle'].values[:]                             = (2 * np.pi) / 5
state['surface_temperature'].values[:]                      = state['air_temperature'].values[0,0,0]
state['area_type'].values[:]                                = 'sea'
state['eastward_wind'].values[0]                            = 5.0

state['mole_fraction_of_carbon_dioxide_in_air'].values[:]  = float(co2_ppm) * 10**(-6)


time_stepper = AdamsBashforth([radiation_lw, radiation_sw, slab, moist_convection])

# Day length to match Shanshan
run_days = 1
run_length = int((run_days * 24 * 60) / dt_minutes)

for i in range(run_length):
    diagnostics, state = time_stepper(state, timestep)
    state.update(diagnostics)

    diagnostics, new_state = simple_physics(state, timestep)
    state.update(diagnostics)

    state.update(new_state)  #Update new simple_physics state   # These lines included w/
                                                                # the Dry Convective Scheme,
    diagnostics, new_state = dry_convection(state, timestep)    # Introduced for
    state.update(diagnostics)                                   # More realistic temperature profile

    if (i % 36 == 0):
        print(list(state.keys()))
        netcdf_monitor.store(state)

    state.update(new_state)
    state['time'] += timestep
    state['eastward_wind'].values[0] = 5.0
    # ^default value of old climt turbulence that Shanshan didn't seem to change
