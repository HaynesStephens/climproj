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

store_quantities = ['air_temperature',
                    'surface_temperature',
                    'specific_humidity',
                    'eastward_wind',
                    'northward_wind',
                    'atmosphere_hybrid_sigma_pressure_a_coordinate_on_interface_levels',
                    'atmosphere_hybrid_sigma_pressure_b_coordinate_on_interface_levels',
                    'surface_air_pressure',
                    'time',
                    'air_pressure',
                    'air_pressure_on_interface_levels',
                    'longitude',
                    'latitude',
                    'height_on_ice_interface_levels',
                    'surface_specific_humidity',
                    'cloud_base_mass_flux',
                    'mole_fraction_of_ozone_in_air',
                    'mole_fraction_of_carbon_dioxide_in_air',
                    'mole_fraction_of_methane_in_air',
                    'mole_fraction_of_nitrous_oxide_in_air',
                    'mole_fraction_of_oxygen_in_air',
                    'mole_fraction_of_cfc11_in_air',
                    'mole_fraction_of_cfc12_in_air',
                    'mole_fraction_of_cfc22_in_air',
                    'mole_fraction_of_carbon_tetrachloride_in_air',
                    'surface_longwave_emissivity',
                    'longwave_optical_thickness_due_to_cloud',
                    'longwave_optical_thickness_due_to_aerosol',
                    'cloud_area_fraction_in_atmosphere_layer',
                    'mass_content_of_cloud_ice_in_atmosphere_layer',
                    'mass_content_of_cloud_liquid_water_in_atmosphere_layer',
                    'cloud_ice_particle_size',
                    'cloud_water_droplet_radius',
                    'zenith_angle',
                    'surface_albedo_for_direct_shortwave',
                    'surface_albedo_for_direct_near_infrared',
                    'surface_albedo_for_diffuse_near_infrared',
                    'surface_albedo_for_diffuse_shortwave',
                    'shortwave_optical_thickness_due_to_cloud',
                    'cloud_asymmetry_parameter',
                    'cloud_forward_scattering_fraction',
                    'single_scattering_albedo_due_to_cloud',
                    'shortwave_optical_thickness_due_to_aerosol',
                    'aerosol_asymmetry_parameter',
                    'single_scattering_albedo_due_to_aerosol',
                    'aerosol_optical_depth_at_55_micron',
                    # 'solar_cycle_fraction',
                    # 'flux_adjustment_for_earth_sun_distance',
                    'downwelling_longwave_flux_in_air',
                    'downwelling_shortwave_flux_in_air',
                    'upwelling_longwave_flux_in_air',
                    'upwelling_shortwave_flux_in_air',
                    'surface_upward_latent_heat_flux',
                    'surface_upward_sensible_heat_flux',
                    'surface_thermal_capacity',
                    'surface_material_density',
                    'upward_heat_flux_at_ground_level_in_soil',
                    'heat_flux_into_sea_water_due_to_sea_ice',
                    'area_type',
                    'soil_layer_thickness',
                    'ocean_mixed_layer_thickness',
                    'heat_capacity_of_soil',
                    'sea_water_density',
                    'upwelling_longwave_flux_in_air_assuming_clear_sky',
                    'downwelling_longwave_flux_in_air_assuming_clear_sky',
                    'air_temperature_tendency_from_longwave_assuming_clear_sky',
                    'air_temperature_tendency_from_longwave',
                    'upwelling_shortwave_flux_in_air_assuming_clear_sky',
                    'downwelling_shortwave_flux_in_air_assuming_clear_sky',
                    'air_temperature_tendency_from_shortwave_assuming_clear_sky',
                    'air_temperature_tendency_from_shortwave',
                    'depth_of_slab_surface',
                    'convective_state',
                    'convective_precipitation_rate',
                    'convective_downdraft_velocity_scale',
                    'convective_downdraft_temperature_scale',
                    'convective_downdraft_specific_humidity_scale',
                    'atmosphere_convective_available_potential_energy',
                    'air_temperature_tendency_from_convection',
                    'stratiform_precipitation_rate']

netcdf_monitor = NetCDFMonitor(nc_name, store_names=store_quantities, write_on_store=True)

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
run_days = 3
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
