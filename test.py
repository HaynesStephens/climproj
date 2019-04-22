import climt
import numpy as np
import matplotlib.pyplot as plt

# Create some components
radiation = climt.GrayLongwaveRadiation()
convection = climt.EmanuelConvection()
surface = climt.SlabSurface()

# Get a state dictionary filled with required quantities
# for the components to run
state = climt.get_default_state([radiation, surface, convection])

# Run components
tendencies, diagnostics = radiation(state)

# See output
print(tendencies.keys())
