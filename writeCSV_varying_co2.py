from writeCSV import *

# List of saved quantities, sorted by dimension
store_quantities_0D = load_quantities_0D()
store_quantities_1D = load_quantities_1D()

co2_ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol_list = [290, 320]

for i in range(len(co2_ppm_list)):
    co2_ppm = co2_ppm_list[i]

    for j in range(len(insol_list)):
        insol = insol_list[j]

        # Parameters
        test_dir = 'varying_co2/{0}solar/'.format(insol) # Needs to end in an '/'
        print('TEST:', test_dir)

        job_name    = 'i{0}_{1}solar'.format(co2_ppm, insol)
        print('Job:', job_name)

        nc_path     = '/home/haynes13/climt_runs/{0}{1}/{1}'.format(test_dir, job_name)
        nc = openNC(nc_path)
        save_path   = '/home/haynes13/climt_files/{0}{1}/{1}'.format(test_dir, job_name)

        # Procedure
        for var_name in store_quantities_0D:
            saveTimeSeriesDim(nc, var_name, save_path, dim=0)
        for var_name in store_quantities_1D:
            saveTimeSeriesDim(nc, var_name, save_path, dim=1)
        saveMoistEnthalpy(nc, save_path)
