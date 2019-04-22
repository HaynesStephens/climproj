import climt
import numpy as np
import matplotlib.pyplot as plt
from sympl import (AdamsBashforth, TendencyStepper, NetCDFMonitor)
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

diagnostics, new_state = convection(model_state, model_timestep)
print(diagnostics.keys())
