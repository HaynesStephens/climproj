import pandas as pd
import pickle

run_type = 'tot'
diag_var = 'T'
basepath = '/project2/moyer/old_project/haynes/climt_files/diagnostic/{0}/{1}/'.format(run_type, diag_var)
input_ppm_list = [100, 150, 220, 270, 540, 1080, 1215]
job_list = ['diagnostic_{0}_{1}_input{2}'.format(run_type, diag_var, ppm) for ppm in input_ppm_list]
file_list = ['{0}{1}/{1}_pkl_eq.pkl'.format(basepath, job) for job in job_list]


def get_df(fname, input_ppm):
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
                                'ppm'        : [input_ppm],
                                'insol'      : [320]})
    return df


def get_ds_batch(file_list):
    df0 = get_df(file_list[0], input_ppm_list[0])
    for i in range(1, len(file_list)):
        df_i = get_df(file_list[i], input_ppm_list[i])
        df0 = pd.concat([df0, df_i])
    return df0


print('Loading & combining dataframes.')
df = get_ds_batch(file_list)

outpath = '/home/haynes13/code/python/climproj/' \
          'data_calculated/diagnostic_{0}_{1}_eq.csv'.format(run_type, diag_var)
f = open(outpath, 'w')
comments = ['# This is a dataframe of the used to calculate anomalies \n',
            '# for the diagnostic group,\n',
            '# for varying {0} profiles. Used for:\n'.format(diag_var),
            '# \n']
print('Writing comments:')
[print(comment) for comment in comments]
[f.write(comment) for comment in comments]
print('Writing dataframe to:\n' + outpath)
df.to_csv(f, index=False)
f.close()
