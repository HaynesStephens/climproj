import numpy as np
import matplotlib.pyplot as plt


# def plotProfile(csv_file):
#     time_series = np.loadtxt(csv_file, delimiter = ',')
#     for i in range(len(time_series)):
#         if i == 0:
#             initial_profile = time_series[i].flatten()
#         profile_i = time_series[i].flatten()


def plotLWPartition(lw_up_csv, lw_dn_csv, ts_csv, save_name):
    lw_up   = np.loadtxt(lw_up_csv, delimiter = ',')
    lw_dn   = np.loadtxt(lw_dn_csv, delimiter = ',')
    ts      = np.loadtxt(ts_csv, delimiter = ',')

    lw_up_surf = lw_up[:, 0]
    lw_dn_surf = lw_dn[:, 0]
    sigma = 5.67 * (10**(-8))
    ts_lw = sigma * (ts**4)
    time = np.arange(lw_up_surf.size)

    plt.plot(time, lw_up_surf, label='Up')
    plt.plot(time, lw_dn_surf, label='Dn')
    plt.plot(time, ts_lw, '--', label = 'Ts', c = 'k')
    plt.legend()
    plt.savefig(save_name)

base_name = '/project2/moyer/old_project/haynes/climt_files/diagnostic/tot/'
diag_var = 'T'
input_ppm_list = [100]#, 150, 220, 270, 540, 1080, 1215]
save_name = ['/home/haynes13/code/python/climproj/figures/diagnostics/tot/diagnostic_tot_{0}_input{1}'.format(diag_var, ppm) for ppm in input_ppm_list]']
run_name = ['{0}{1}/diagnostic_tot_{1}_input{2}/diagnostic_tot_{1}_input{2}'.format(base_name, diag_var, ppm) for ppm in input_ppm_list]
lw_up_csv_list = ['{0}_upwelling_longwave_flux_in_air.csv'.format(name) for name in run_name]
lw_dn_csv_list = ['{0}_downwelling_longwave_flux_in_air.csv'.format(name) for name in run_name]
ts_csv_list = ['{0}_surface_temperature.csv'.format(name) for name in run_name]
for i in range(len(ts_csv_list)):
    lw_up_csv = lw_up_csv_list[i]
    lw_dn_csv = lw_dn_csv_list[i]
    ts_csv    = ts_csv_list[i]
    plotLWPartition(lw_up_csv, lw_dn_csv, ts_csv)

