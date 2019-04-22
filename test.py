import climt

# Create some components
radiation = climt.GrayLongwaveRadiation()
surface = climt.SlabSurface()

# Get a state dictionary filled with required quantities
# for the components to run
state = climt.get_default_state([radiation, surface])

# Run components
tendencies, diagnostics = radiation(state)

# See output
print(tendencies.keys())
