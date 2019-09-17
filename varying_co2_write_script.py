import os
import newSbatch

co2_ppm = 330
job_name = 'i{0}_290solar'.format(co2_ppm)
nc_name = job_name + '.nc'

template_path = '/home/haynes13/code/python/climproj/climt_scripts/varying_co2_template.py'
job_path = '/home/haynes13/code/python/climproj/climt_scripts/{0}.py'.format(job_name)
print(job_path)


with open(template_path, 'r') as fin, open(job_path, 'w') as fout:
    fout.write('### UNIQUE VALUES ###\n')
    fout.write('co2_ppm = np.float({0})\n'.format(co2_ppm))
    fout.write('nc_name = {0}.nc\n'.format(job_name))
    fout.write('#####################\n')

    for line in fin.readlines():
        fout.write(line)

base_dir = '/home/haynes13/climt_runs/'
test_dir = 'varying_co2/' # Needs to end in an '/'
newSbatch.newSbatch(base_dir, test_dir, job_name)






