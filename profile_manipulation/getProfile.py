from metpy.calc import pressure_to_height_std
from metpy.units import units

def getMoleProfileCO2(co2_ppm, air_pressure, air_pressure_on_interface_levels, air_temperature):
    interface_heights = pressure_to_height_std(air_pressure_on_interface_levels.copy() * units('Pa'))
    volumes = interface_heights[1:] - interface_heights[:-1]
    R = 8.31446261815324 # J K^-1 mol^-1

    n_co2 = ((air_pressure * volumes) / (R * air_temperature)) * (co2_ppm / (1 - co2_ppm))
    return n_co2

