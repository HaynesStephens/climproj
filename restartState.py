from netCDF4 import Dataset
import copy


def makeRestartFile(control_file_path, restart_file_path):
    dset = Dataset(control_file_path, mode='r', format="NETCDF4")
    restart_nc = Dataset(restart_file_path, mode='w', format="NETCDF4")
    for var in dset.variables:
        restart_nc[var] = dset[var]
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

