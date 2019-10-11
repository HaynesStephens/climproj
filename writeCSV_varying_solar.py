from writeCSV import *

# List of saved quantities, sorted by dimension
store_quantities_0D = load_quantities_0D()
store_quantities_1D = load_quantities_1D()

# insol_list      = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
#                    270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]
insol_list      = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245]

co2_ppm = 270
for j in range(len(insol_list)):
    insol = insol_list[j]

    # Parameters
    test_dir = 'varying_solar/' # Needs to end in an '/'
    print('TEST:', test_dir)

    job_name    = 'i{0}_{1}solar'.format(co2_ppm, insol)
    print('Job:', job_name)

    nc_path     = '/project2/moyer/old_project/haynes/climt_runs/{0}{1}/{1}'.format(test_dir, job_name)
    nc = openNC(nc_path)
    save_path   = '/project2/moyer/old_project/haynes/climt_files/{0}{1}/{1}'.format(test_dir, job_name)

    # Procedure
    for var_name in store_quantities_0D:
        saveTimeSeriesDim(nc, var_name, save_path, dim=0)
    for var_name in store_quantities_1D:
        saveTimeSeriesDim(nc, var_name, save_path, dim=1)
    saveMoistEnthalpy(nc, save_path)
