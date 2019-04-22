import climt
from datetime import timedelta

# Define model timestep in minutes
model_timestep = timedelta(minutes=20)

# Create some components
radiation = climt.GrayLongwaveRadiation()
radiation = climt.radiation(scheme='ccm3')
convection = climt.EmanuelConvection()
boundary_layer = climt.SlabSurface()

# Get a state dictionary filled with required quantities
# for the components to run
model_state = climt.get_default_state([radiation, convection, boundary_layer])

diagnostics, new_state = radiation(model_state)
print(diagnostics.keys())
