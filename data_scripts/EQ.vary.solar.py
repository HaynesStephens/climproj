import pandas as pd
import numpy as np

basepath    = '/project2/moyer/old_project/haynes/climt_files/varying_solar/'
insol_list  = np.sort(np.array([200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
                               270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]))
job_list    = ['i270_{0}solar'.format(insol) for insol in insol_list]
eq_list     = ['{0}{1}/{1}.eq.pkl'.format(basepath, job) for job in job_list]


def get_EQ_df(fname, insol):
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
                                'ppm'        : [270],
                                'insol'      : [insol]})
    return df


def get_EQ_batch(filelist, insol_list):
    df0 = get_EQ_df(filelist[0], insol_list[0])
    for i in range(1, len(filelist)):
        df_i = get_EQ_df(filelist[i], insol_list[i])
        df0 = pd.concat([df0, df_i])
    return df0


print('Loading & combining dataframes.')
df = get_EQ_batch(eq_list, insol_list)

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
