import pandas as pd
import numpy as np

basepath = '/Users/haynesstephens1/uchi/research/climproj/climt_files/varying_co2/320solar/'
ppm_list = np.sort(np.array([100, 1080, 150, 20, 2, 405, 5, 675, 10, 1215, 190, 220, 270, 50, 540, 756]))
job_list = ['i{0}_320solar'.format(ppm) for ppm in ppm_list]
eq_list = ['{0}{1}/{1}_eqTable1Values.csv'.format(basepath, job) for job in job_list]

def get_EQ_batch(filelist):
    df0 = pd.read_csv(filelist[0])
    for i in range(1, len(filelist)):
        df_i = pd.read_csv(filelist[i])
        df0 = pd.concat([df0, df_i])
    return df0

print('Loading control.')
control_eq_file = '/Users/haynesstephens1/uchi/research/climproj/climt_files/varying_co2/320solar/i270_320solar/i270_320solar_eqTable1Values.csv'
control_df = pd.read_csv(control_eq_file)

print('Loading & combining dataframes.')
df = get_EQ_batch(eq_list)

outpath = '/Users/haynesstephens1/uchi/research/climproj/climproj/data_calculated/EQ.varyco2.320solar.anomalies.csv'
f = open(outpath, 'a')
comments = ['# This is a dataframe of the used to calculate anomalies for the 320solar varing-co2 group. Used for:\n',
            '# - Shanshan EQ Fig 6.\n']
print('Writing comments:')
[print(comment) for comment in comments]
[f.write(comment) for comment in comments]
print('Writing dataframe to:\n' + outpath)
df.to_csv(f, index = False)
f.close()
