import numpy as np
import matplotlib.pyplot as plt
import os

distributions = {'T':'', 'q':'', 'co2':''}
control_ppm = 270
input_ppm = 1080
expt_name = 'swap_profiles'
os.system('mkdir -p /home/haynes13/code/python/climproj/figures/distributionPlots/{0}'.format(expt_name))


control_file = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/i{0}_320solar_fullstore'.format(control_ppm)
expt_dir = ''
kl
