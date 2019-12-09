import os
import newSbatch


def createRun(input_ppm):
    irradiance = 1036
    insol = 320
    job_name = 'diagnostic_gray_rrtmgSW_uniform_q_input{0}'.format(input_ppm)

    template_path = '/home/haynes13/code/python/climproj/climt_scripts/diagnostic/gray_rrtmgSW_uniform/diagnostic_gray_rrtmgSW_uniform_q_template.py'
    job_path = '/home/haynes13/code/python/climproj/climt_scripts/diagnostic/gray_rrtmgSW_uniform/q/{0}.py'.format(job_name)
    print(job_path)


    with open(template_path, 'r') as fin, open(job_path, 'w') as fout:
        fout.write('### UNIQUE VALUES ###\n')
        fout.write('irradiance = {0}\n'.format(irradiance))
        fout.write('#insol = {0}\n'.format(insol))
        fout.write('input_ppm = {0}\n'.format(input_ppm))
        fout.write("nc_name = '{0}.nc'\n".format(job_name))
        fout.write('#####################\n')

        for line in fin.readlines():
            fout.write(line)

    base_dir = '/project2/moyer/old_project/haynes/' # Needs to end in an '/'
    test_dir = 'diagnostic/gray_rrtmgSW_uniform/q/' # Needs to end in an '/'
    job_dir, sbatch_filename = newSbatch.newSbatch(base_dir, test_dir, job_name)
    return job_dir, sbatch_filename

os.system('mkdir -p /home/haynes13/code/python/climproj/climt_scripts/diagnostic/gray_rrtmgSW_uniform/q/')

# TEMPLATE, ENTIRE LIST:
input_ppm_list = [100, 150, 220, 270, 540, 1080, 1215]

for input_ppm in input_ppm_list:
    job_dir, sbatch_filename = createRun(input_ppm)
    os.chdir(job_dir)
    os.system('sbatch {0}'.format(sbatch_filename))
