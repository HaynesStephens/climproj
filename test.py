import climt
import numpy as np
import matplotlib.pyplot as plt
from sympl import (AdamsBashforth, NetCDFMonitor)
from datetime import timedelta

# Define model timestep in minutes
model_timestep = timedelta(minutes=20)

# Create some components
radiation = climt.GrayLongwaveRadiation()
convection = climt.EmanuelConvection()
boundary_layer = climt.SlabSurface()

# Get a state dictionary filled with required quantities
# for the components to run
model_state = climt.get_default_state([radiation, convection, boundary_layer])

# Create integrator
time_stepper = AdamsBashforth([radiation, convection])
monitor = NetCDFMonitor('radiative_convective.nc')

# step model forward
for step in range(10):
    bl_diagnostics, bl_new_state = boundary_layer(model_state)
    model_state.update(bl_diagnostics)
    model_state.update(bl_new_state)

    diagnostics, new_state = time_stepper(model_state, model_timestep)
    model_state.update(diagnostics)
    monitor.store(model_state)
    model_state.update(new_state)
    model_state['time'] += model_timestep
