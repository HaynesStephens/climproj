import pandas as pd

def get_EQ_file(filename, ppm, insol):
    df = pd.read_csv(filename, delimiter = ':', header=None).transpose()
    df.columns = df.loc[0]
    df = df.drop(0, axis=0)
    df['ppm'] = ppm
    df['insol'] = insol
    return df
