import climt
from datetime import timedelta

# Define model timestep in minutes
model_timestep = timedelta(minutes=20)

# Create some components
lw_radiation = climt.RRTMGLongwave()
sw_radiation = climt.RRTMGShortwave()
convection = climt.EmanuelConvection()
boundary_layer = climt.SlabSurface()

# Get a state dictionary filled with required quantities
# for the components to run
model_state = climt.get_default_state([lw_radiation, sw_radiation, convection, boundary_layer])

diagnostics, new_state = radiation(model_state)
print(diagnostics.keys())
