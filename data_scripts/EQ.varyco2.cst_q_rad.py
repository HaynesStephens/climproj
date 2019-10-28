import pandas as pd
import numpy as np

basepath = '/project2/moyer/old_project/haynes/climt_files/varying_co2_cst_q_rad/'
ppm_list = np.array([2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215])
job_list = ['i{0}_320solar_cst_q_rad'.format(ppm) for ppm in ppm_list]
eq_list = ['{0}{1}/{1}_eqTable1Values.csv'.format(basepath, job) for job in job_list]

def get_EQ_batch(filelist):
    df0 = pd.read_csv(filelist[0])
    for i in range(1, len(filelist)):
        df_i = pd.read_csv(filelist[i])
        df0 = pd.concat([df0, df_i])
    return df0

# print('Loading control.')
# control_eq_file = '/Users/haynesstephens1/uchi/research/climproj/climt_files/' \
#                   'varying_co2/290solar/i270_290solar/i270_290solar_eqTable1Values.csv'
# control_df = pd.read_csv(control_eq_file)

print('Loading & combining dataframes.')
df = get_EQ_batch(eq_list)

outpath = '/home/haynes13/code/python/climproj/data_calculated/EQ.varyco2.cst_q_rad.csv'
f = open(outpath, 'w')
comments = ['# This is a dataframe of the used to calculate anomalies for the 320solar varing-co2 cst-q-rad group. Used for:\n',
            '# - ??\n']
print('Writing comments:')
[print(comment) for comment in comments]
[f.write(comment) for comment in comments]
print('Writing dataframe to:\n' + outpath)
df.to_csv(f, index=False)
f.close()
