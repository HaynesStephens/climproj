import pandas as pd
import numpy as np
from data_scripts.getControl import *

basepath = '/project/moyer/haynes/climt_files/varying_co2/320solar/'
ppm_list = np.sort(np.array([100, 1080, 150, 20, 2, 405, 5, 675, 10, 1215, 190, 220, 270, 50, 540, 756]))
job_list = ['i{0}_320solar'.format(ppm) for ppm in ppm_list]
eq_list = ['{0}{1}/{1}_eqTable1Values.txt'.format(basepath, job) for job in job_list]

control_df = get_EQ_file(control_eq_file, 270, 290)

def get_EQ_batch(filelist, ppm_list):
    df0 = get_EQ_file(filelist[0], ppm_list[0], 320)
    for i in range(1, len(filelist)):
        df_i = get_EQ_file(filelist[i], ppm_list[i], 320)
        df0 = pd.concat([df0, df_i])
    return df0

df = get_EQ_batch(eq_list, ppm_list)

anomaly_df = df - control_df
