from pullWindowValues import *

co2_ppm = 270
# insol_list      = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
#                    270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]
insol_list      = [250, 255, 260, 265, 270, 275, 280, 285, 290,
                   295, 300, 305, 310, 315, 320, 325, 330, 335]

start_day = 9950
end_day = 10950 - 1
start_time = np.float(start_day * (24 * 60 * 60))
end_time = np.float(end_day * (24 * 60 * 60))

for j in range(len(insol_list)):
    insol = insol_list[j]
    # Parameters
    base_path = '/project2/moyer/old_project/haynes/climt_files/'
    test_dir = 'varying_solar/'.format(insol)  # Needs to end in an '/'
    print('TEST:', test_dir)

    job_name = 'i{0}_{1}solar'.format(co2_ppm, insol)
    print('JOB:', job_name)

    file_path = '{0}{1}{2}/{2}'.format(base_path, test_dir, job_name)
    extras = {'ppm': co2_ppm, 'insol': insol}

    # Procedures
    writeEQTable1Values(file_path, start_time, end_time, extras=extras)
