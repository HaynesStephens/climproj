from netCDF4 import Dataset
import copy


def makeRestartFile(control_file_path, restart_file_path):
    dset = Dataset(control_file_path, mode='r', format="NETCDF4")
    restart_nc = Dataset(restart_file_path, mode='w', format="NETCDF4")
    for var in dset.variables:
        data = dset[var]
        variable = restart_nc.createVariable(varname = data.name,
                                             datatype = data.datatype,
                                             dimensions = data.dimensions)
        variable.units = data.units
        restart_nc[var][:] = restart_nc[var][:][-1]
    dset.close()
    restart_nc.close()


def loadRestartFile(state, restart_file_path):
    new_state = copy.deepcopy(state)
    dset = Dataset(restart_file_path, mode='r', format="NETCDF4")
    for var in dset.variables:
        new_state[var].values = dset[var][:]
    dset.close()
    return new_state


control_file_path = '/home/haynes13/code/python/climproj/climt_scripts/scratch_270_290.nc'
restart_file_path = '/home/haynes13/code/python/climproj/climt_scripts/scratch_restart.nc'
makeRestartFile(control_file_path, restart_file_path)
