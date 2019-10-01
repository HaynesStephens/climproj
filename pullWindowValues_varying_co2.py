from pullWindowValues import *

co2_ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol_list = [290, 320]

start_day = 9950
end_day = 10950 - 1
start_time = np.float(start_day * (24 * 60 * 60))
end_time = np.float(end_day * (24 * 60 * 60))

for i in range(len(co2_ppm_list)):
    co2_ppm = co2_ppm_list[i]

    for j in range(len(insol_list)):
        insol = insol_list[j]
        # Parameters
        base_path = '/project/moyer/haynes/climt_files/'
        test_dir = 'varying_co2/{0}solar/'.format(insol)  # Needs to end in an '/'
        print('TEST:', test_dir)

        job_name = 'i{0}_{1}solar'.format(co2_ppm, insol)
        print('JOB:', job_name)

        file_path = '{0}{1}{2}/{2}'.format(base_path, test_dir, job_name)
        extras = {'ppm': co2_ppm, 'insol': insol}

        # Procedures
        writeEQTable1Values(file_path, start_time, end_time, extras=extras)
