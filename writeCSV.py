# This is a script to write the appropriate values from an nc file into a smaller csv file
# to be added to the github repo so that I can download it to my computer
# without having to lug a brick of data on my harddrive.

import numpy as np
from netCDF4 import Dataset as ds

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
                    'surface_upward_sensible_heat_flux',
                    'surface_upward_latent_heat_flux',
                    'upwelling_longwave_flux_in_air',
                    'upwelling_shortwave_flux_in_air',
                    'downwelling_longwave_flux_in_air',
                    'downwelling_shortwave_flux_in_air']


np.savetxt('%s_%s_iwd_6C_em.csv'%(model, crop), b, delimiter=',')


