import os
import newSbatch


def createRun(co2_ppm, irradiance, insol):
    job_name = 'i{0}_{1}solar'.format(co2_ppm, insol)

    template_path = '/home/haynes13/code/python/climproj/climt_scripts/varying_solar_template.py'
    job_path = '/home/haynes13/code/python/climproj/climt_scripts/{0}.py'.format(job_name)
    print(job_path)


    with open(template_path, 'r') as fin, open(job_path, 'w') as fout:
        fout.write('### UNIQUE VALUES ###\n')
        fout.write('irradiance = {0}\n'.format(irradiance))
        fout.write('#insol = {0}\n'.format(insol))
        fout.write('co2_ppm = {0}\n'.format(co2_ppm))
        fout.write("nc_name = '{0}.nc'\n".format(job_name))
        fout.write('#####################\n')

        for line in fin.readlines():
            fout.write(line)

    base_dir = '/project2/moyer/old_project/haynes/climt_runs/'
    test_dir = 'varying_solar/' # Needs to end in an '/'
    job_dir, sbatch_filename = newSbatch.newSbatch(base_dir, test_dir, job_name)
    return job_dir, sbatch_filename

co2_ppm_list = [270]
# insol_list      = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
#                    270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]
# irradiance_list = [647, 663, 680, 696, 712, 728, 744, 760, 777, 793, 809, 825, 841, 858,
#                    874, 890, 906, 922, 939, 955, 971, 987, 1003, 1019, 1036, 1052, 1068, 1084]
insol_list      = [250, 255, 260, 265, 270, 275, 280, 285, 290,
                   295, 300, 305, 310, 315, 320, 325, 330, 335]
irradiance_list = [809, 825, 841, 858, 874, 890, 906, 922, 939,
                   955, 971, 987, 1003, 1019, 1036, 1052, 1068, 1084]

for i in range(len(co2_ppm_list)):
    co2_ppm = co2_ppm_list[i]

    for j in range(len(irradiance_list)):
        irradiance = irradiance_list[j]
        insol = insol_list[j]

        job_dir, sbatch_filename = createRun(co2_ppm, irradiance, insol)
        os.chdir(job_dir)
        os.system('sbatch {0}'.format(sbatch_filename))



