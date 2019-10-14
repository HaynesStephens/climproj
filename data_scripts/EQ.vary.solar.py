import pandas as pd
import numpy as np

basepath = '/project2/moyer/old_project/haynes/climt_files/varying_solar/'
insol_list = np.sort(np.array([200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
                               270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]))
job_list = ['i270_{0}solar'.format(insol) for insol in insol_list]
eq_list = ['{0}{1}/{1}_eqTable1Values.csv'.format(basepath, job) for job in job_list]

def get_EQ_batch(filelist):
    df0 = pd.read_csv(filelist[0])
    for i in range(1, len(filelist)):
        df_i = pd.read_csv(filelist[i])
        df0 = pd.concat([df0, df_i])
    return df0

# print('Loading control.')
# control_eq_file = '/project2/moyer/old_project/haynes/climt_files/varying_solar/' \
#                   'i270_290solar/i270_290solar_eqTable1Values.csv'
# control_df = pd.read_csv(control_eq_file)

print('Loading & combining dataframes.')
df = get_EQ_batch(eq_list)

outpath = '/home/haynes13/code/python/climproj/data_calculated/EQ.vary.solar.csv'
f = open(outpath, 'w')
comments = ['# This is a dataframe of the used to calculate anomalies for the varying-solar group. Used for:\n',
            '# - ??\n']
print('Writing comments:')
[print(comment) for comment in comments]
[f.write(comment) for comment in comments]
print('Writing dataframe to:\n' + outpath)
df.to_csv(f, index=False)
f.close()
