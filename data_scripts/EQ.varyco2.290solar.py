import pandas as pd
import numpy as np
import pickle

basepath = '/project2/moyer/old_project/haynes/climt_files/varying_co2/290solar/'
ppm_list = np.array([2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215])
job_list = ['i{0}_290solar'.format(ppm) for ppm in ppm_list]
eq_list = ['{0}{1}/{1}.eq.pkl'.format(basepath, job) for job in job_list]


def get_EQ_df(fname):
    pkl         = pickle.load(open(fname, 'rb'))
    sw_up       = pkl['upwelling_shortwave_flux_in_air']
    sw_dn       = pkl['downwelling_shortwave_flux_in_air']
    sw_surf     = (sw_up - sw_dn)[0, 0]
    sw_toa      = (sw_up - sw_dn)[-1, 0]
    lw_up       = pkl['upwelling_longwave_flux_in_air']
    lw_dn       = pkl['downwelling_longwave_flux_in_air']
    lw_surf     = (lw_up - lw_dn)[0, 0]
    lw_toa      = (lw_up - lw_dn)[-1, 0]
    net_surf    = lw_surf + sw_surf
    net_toa     = lw_toa + sw_toa
    t_surf      = pkl['surface_temperature'][0]
    lh          = pkl['surface_upward_latent_heat_flux'][0]
    sh          = pkl['surface_upward_sensible_heat_flux'][0]
    conv_prec   = pkl['convective_precipitation_rate'][0]
    strat_prec  = pkl['stratiform_precipitation_rate'][0]
    ppm         = np.round(pkl['mole_fraction_of_carbon_dioxide_in_air'][0,0]*10**6)
    df          = pd.DataFrame({'NETsurf'    : net_surf,
                                'NETtoa'     : net_toa,
                                'SWsurf'     : sw_surf,
                                'SWtoa'      : sw_toa,
                                'LWsurf'     : lw_surf,
                                'LWtoa'      : lw_toa,
                                'LH'         : lh,
                                'SH'         : sh,
                                'Ts'         : t_surf,
                                'ConvPrec'   : conv_prec,
                                'StratPrec'  : strat_prec,
                                'ppm'        : ppm,
                                'insol'      : [290]})
    return df


def get_EQ_batch(filelist):
    df0 = get_EQ_df(filelist[0])
    for i in range(1, len(filelist)):
        df_i = get_EQ_df(filelist[i])
        df0 = pd.concat([df0, df_i])
    return df0


print('Loading & combining dataframes.')
df = get_EQ_batch(eq_list)

outpath = '/home/haynes13/code/python/climproj/data_calculated/EQ.varyco2.290solar.csv'
f = open(outpath, 'w')
comments = ['# This is a dataframe of the used to calculate anomalies \n',
            '# for the 290solar varing-co2 group. Used for:\n',
            '# - ??\n']
print('Writing comments:')
[print(comment) for comment in comments]
[f.write(comment) for comment in comments]
print('Writing dataframe to:\n' + outpath)
df.to_csv(f, index=False)
f.close()
