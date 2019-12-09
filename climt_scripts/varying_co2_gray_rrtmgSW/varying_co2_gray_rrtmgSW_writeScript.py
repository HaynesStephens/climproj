import os
import newSbatch


def createRun(co2_ppm, irradiance, insol, template_py):
    job_name = 'i{0}_{1}solar'.format(co2_ppm, insol)

    template_path = '/home/haynes13/code/python/climproj/climt_scripts/varying_co2_gray_rrtmgSW/' + template_py
    job_path = '/home/haynes13/code/python/climproj/climt_scripts/varying_co2_gray_rrtmgSW/{0}solar/{1}.py'.format(insol, job_name)
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

    base_dir = '/project2/moyer/old_project/haynes/'
    test_dir = 'varying_co2_gray_rrtmgSW/{0}solar/'.format(insol) # Needs to end in an '/'
    job_dir, sbatch_filename = newSbatch.newSbatch(base_dir, test_dir, job_name)
    return job_dir, sbatch_filename

# os.system('mkdir -p /home/haynes13/code/python/climproj/climt_scripts/varying_co2_gray_rrtmgSW/290solar')
os.system('mkdir -p /home/haynes13/code/python/climproj/climt_scripts/varying_co2_gray_rrtmgSW/320solar')
# TRIAL RUN ONLY USING 2 PPM
co2_ppm_list = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
irradiance_list = [1036]
insol_list = [320]
insol_template_list = ['varying_co2_gray_rrtmgSW_template_320solar.py']

for i in range(len(co2_ppm_list)):
    co2_ppm = co2_ppm_list[i]

    for j in range(len(irradiance_list)):
        irradiance = irradiance_list[j]
        insol = insol_list[j]
        template_py = insol_template_list[j]

        job_dir, sbatch_filename = createRun(co2_ppm, irradiance, insol, template_py)
        os.chdir(job_dir)
        os.system('sbatch {0}'.format(sbatch_filename))



