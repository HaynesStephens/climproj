import netCDF4 as nc
import copy


def makeRestartFile(control_file_path, restart_file_path):
    def create_file_from_source(src_file, trg_file):
        src = nc.Dataset(src_file)
        trg = nc.Dataset(trg_file, mode='w')
        # Create the dimensions of the file
        for name, dim in src.dimensions.items():
            trg.createDimension(name, len(dim) if not dim.isunlimited() else None)
        # Copy the global attributes
        trg.setncatts({a: src.getncattr(a) for a in src.ncattrs()})
        # Create the variables in the file
        for name, var in src.variables.items():
            trg.createVariable(name, var.dtype, var.dimensions)
            # Copy the variable attributes
            trg.variables[name].setncatts({a: var.getncattr(a) for a in var.ncattrs()})
            # Copy the variables values (as 'f4' eventually)
            trg.variables[name][:] = src.variables[name][:]
        return trg

    restart_nc = create_file_from_source(control_file_path, restart_file_path)
    for var in list(restart_nc.variables):
        last_instance = restart_nc[var][-1].copy()
        last_instance = last_instance.reshape(tuple([1] + list(last_instance.shape)))
        restart_nc[var] = last_instance


def loadRestartFile(state, restart_file_path):
    new_state = copy.deepcopy(state)
    dset = Dataset(restart_file_path, mode='r', format="NETCDF4")
    for var in list(dset.variables):
        new_state[var].values = dset[var][:]
    dset.close()
    return new_state


control_file_path = '/home/haynes13/code/python/climproj/climt_scripts/scratch_270_290.nc'
restart_file_path = '/home/haynes13/code/python/climproj/climt_scripts/restart.nc'
makeRestartFile(control_file_path, restart_file_path)
