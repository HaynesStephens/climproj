import climt
import numpy as np
import matplotlib.pyplot as plt

# Create some components
radiation = climt.GrayLongwaveRadiation()
convection = climt.EmanuelConvection()
surface = climt.SlabSurface()

# Get a state dictionary filled with required quantities
# for the components to run
state = climt.get_default_state([radiation, convection, surface])

# Run components
tendencies, diagnostics = convection(state)

# See output
print(tendencies.keys())
