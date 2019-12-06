import numpy as np
import matplotlib.pyplot as plt
import os

input_param = 'T'
input_ppm = 1080
expt_name = 'swap_profiles'

control_ppm = 270
distributions = {'T':'', 'q':'', 'co2':''}
os.system('mkdir -p /home/haynes13/code/python/climproj/figures/distributionPlots/{0}'.format(expt_name))

control_file = '/project2/moyer/old_project/haynes/climt_files/control_fullstore/i{0}_320solar_fullstore'.format(control_ppm)
input_dir = '/project'
expt_dir = '/project2/moyer/old_project/haynes/climt_files/diagnostic/{0}/'.format(expt_name)

fig, subplots = plt.subplots(2, 3, figsize=(21,8), sharey=True)


