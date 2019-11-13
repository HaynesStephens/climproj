from writeCSVandPKL import *

# List of saved quantities, sorted by dimension
store_quantities_0D = load_quantities_0D()
store_quantities_1D = load_quantities_1D()

co2_ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
stepper_list = ['fixed_stepper', 'multi_stepper']
insol = 320

for i in range(len(co2_ppm_list)):
    co2_ppm = co2_ppm_list[i]

    for j in range(len(stepper_list)):
        stepper = stepper_list[j]

        # Parameters
        test_dir = 'varying_co2_cst_q_rad/{0}/'.format(stepper) # Needs to end in an '/'
        print('TEST:', test_dir)

        job_name    = 'i{0}_{1}solar_cst_q_rad_{2}'.format(co2_ppm, insol, stepper)
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
