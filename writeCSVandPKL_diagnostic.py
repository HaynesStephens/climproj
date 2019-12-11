from writeCSVandPKL import *

# List of saved quantities, sorted by dimension
store_quantities_0D = load_quantities_0D()
store_quantities_1D = load_quantities_1D()

input_ppm_list = [100, 150, 220, 270, 540, 1080, 1215]
fixed_list = ['q', 'T', 'co2']
run_type_list = ['short_swap']


for run_type in run_type_list:
    for input_ppm in input_ppm_list:
        for fixed_prof in fixed_list:
            # Parameters
            test_dir = 'diagnostic/{0}/{1}/'.format(run_type, fixed_prof) # Needs to end in an '/'
            print('TEST:', test_dir)

            job_name    = 'diagnostic_{0}_{1}_input{2}'.format(run_type, fixed_prof, input_ppm)
            print('Job:', job_name)

            nc_path     = '/project2/moyer/old_project/haynes/climt_runs/{0}{1}/{1}'.format(test_dir, job_name)
            nc = openNC(nc_path)
            save_path   = '/project2/moyer/old_project/haynes/climt_files/{0}{1}/{1}'.format(test_dir, job_name)

            # Procedure
            saveEQpkl(save_path, nc)
            saveTranspkl(save_path, nc)
            for var_name in store_quantities_0D:
                saveTimeSeriesDim(nc, var_name, save_path, dim=0)
            for var_name in store_quantities_1D:
                saveTimeSeriesDim(nc, var_name, save_path, dim=1)
