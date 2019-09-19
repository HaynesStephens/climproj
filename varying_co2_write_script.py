import os
import newSbatch


def createRun(co2_ppm, irradiance, insol):
    job_name = 'i{0}_{1}solar'.format(co2_ppm, insol)

    template_path = '/home/haynes13/code/python/climproj/climt_scripts/varying_co2_template.py'
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

    base_dir = '/home/haynes13/climt_runs/'
    test_dir = 'varying_co2/{0}solar/'.format(insol) # Needs to end in an '/'
    sbatch_filename = newSbatch.newSbatch(base_dir, test_dir, job_name)
    return sbatch_filename

# TRIAL RUN ONLY USING 2 PPM
co2_ppm_list = [2]  # , 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
irradiance_list = [939, 1036]
insol_list = [290, 320]

for i in range(len(co2_ppm_list)):
    co2_ppm = co2_ppm_list[i]

    for j in range(len(irradiance_list)):
        irradiance = irradiance_list[j]
        insol = insol_list[j]

        sbatch_filename = createRun(co2_ppm, irradiance, insol)
        os.system('sbatch {0}'.format(sbatch_filename))



