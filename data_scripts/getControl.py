import pandas as pd

control_eq_file = '/project/moyer/haynes/climt_files/control/i270_290solar/i270_290solar_eqTable1Values.txt'

def get_EQ_file(filename):
    df = pd.read_csv(filename, delimiter = ':', header=None).transpose()
    df.columns = df.loc[0]
    df = df.drop(0, axis=0)
    return df
