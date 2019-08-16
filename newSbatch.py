import os

home_dir = '/home/haynes13/climt_runs/'
job_name = 'test_a2_b1_c1_270i_939solar_dryconv_usurf_noseason'

def createJob(home_dir, job_name): #order input variables by use order, duh
    job_dir = home_dir + job_name
    os.system('mkdir {0}'.format(job_dir))
    os.system('mkdir /home/haynes13/code/python/climproj/saved_plots/{0}'.format(job_name))
    os.system('mkdir /home/haynes13/climt_files/{0}'.format(job_name))
    sbatch_filename = job_dir + '/' + job_name + '.sbatch'
    sbatch_file = open(sbatch_filename, 'w')

    sbatch_file.write('#!/bin/bash\n')
    sbatch_file.write('\n')
    sbatch_file.write('#SBATCH --job-name={0}\n'.format(job_name))
    sbatch_file.write('#SBATCH --output={0}.out\n'.format(job_name))
    sbatch_file.write('#SBATCH --error={0}.err\n'.format(job_name))
    sbatch_file.write('#SBATCH --ntasks=1\n')
    sbatch_file.write('#SBATCH --partition=broadwl\n')
    sbatch_file.write('#SBATCH --cpus-per-task=1\n')
    sbatch_file.write('#SBATCH --time=36:00:00\n')
    sbatch_file.write('#SBATCH --mem-per-cpu=32000\n')
    sbatch_file.write('#SBATCH --mail-type=ALL\n')
    sbatch_file.write('#SBATCH --mail-user=haynes13@uchicago.edu\n')
    sbatch_file.write('\n')
    sbatch_file.write('module load python/3.5.2\n')
    sbatch_file.write('\n')
    sbatch_file.write('python /home/haynes13/code/python/climproj/climt_scripts/{0}.py'.format(job_name))

    sbatch_file.close()

createJob(home_dir, job_name)
