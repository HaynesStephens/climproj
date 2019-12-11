import numpy as np
import matplotlib.pyplot as plt
from metpy.calc import pressure_to_height_std
from metpy.units import units


def plotLWPartition(lw_up_csv, lw_dn_csv, ts_csv, save_name):
    print(lw_up_csv)
    print(lw_dn_csv)
    print(ts_csv)
    print(save_name)
    plt.figure()
    lw_up   = np.loadtxt(lw_up_csv, delimiter = ',')
    lw_dn   = np.loadtxt(lw_dn_csv, delimiter = ',')
    ts      = np.loadtxt(ts_csv, delimiter = ',')

    lw_up_surf = lw_up[:, 0]
    lw_dn_surf = lw_dn[:, 0]
    net_lw_surf = lw_up_surf - lw_dn_surf
    sigma = 5.67 * (10**(-8))
    ts_lw_up = sigma * (ts**4)
    ts_lw_dn = (lw_dn_surf/sigma)**(1/4)
    time = np.arange(lw_up_surf.size) * 36 * 10 * 60 / (60 * 60 * 24)

    plt.plot(time, lw_up_surf, label='Up: {0:.2f}'.format(lw_up_surf[-1]))
    plt.plot(time, lw_dn_surf, label='Dn: {0:.2f}'.format(lw_dn_surf[-1]))
    plt.plot(time, ts_lw_up, '--', label='Tup: {0:.2f}'.format(ts[-1]), c='k')
    plt.plot(time, lw_dn_surf, '-.', label='Tdn: {0:.2f}'.format(ts_lw_dn[-1]), c='k')
    plt.plot(net_lw_surf, label = 'Net Up: {0:.2f}'.format(net_lw_surf[-1]))
    plt.legend()
    plt.savefig(save_name)


# LW FLUX PLOTS
base_name = '/project2/moyer/old_project/haynes/climt_files/diagnostic/tot/'
diag_var = 'T'
input_ppm_list = [100, 150, 220, 270, 540, 1080, 1215]
save_name_list = ['/home/haynes13/code/python/climproj/figures/diagnostics/tot/diagnostic_tot_{0}_input{1}_lw.png'.format(diag_var, ppm) for ppm in input_ppm_list]
run_name = ['{0}{1}/diagnostic_tot_{1}_input{2}/diagnostic_tot_{1}_input{2}'.format(base_name, diag_var, ppm) for ppm in input_ppm_list]
lw_up_csv_list = ['{0}_upwelling_longwave_flux_in_air.csv'.format(name) for name in run_name]
lw_dn_csv_list = ['{0}_downwelling_longwave_flux_in_air.csv'.format(name) for name in run_name]
ts_csv_list = ['{0}_surface_temperature.csv'.format(name) for name in run_name]
for i in range(len(ts_csv_list)):
    lw_up_csv = lw_up_csv_list[i]
    lw_dn_csv = lw_dn_csv_list[i]
    ts_csv    = ts_csv_list[i]
    save_name = save_name_list[i]
    plotLWPartition(lw_up_csv, lw_dn_csv, ts_csv, save_name)


#######################################################


def plotProfiles(csv_files, ppm_list, T_emit_list, air_pressure, save_name):
    plt.figure()
    for i in range(len(csv_files)):
        T_emit = T_emit_list[i]
        filename = csv_files[i]
        print(filename)
        label = ppm_list[i]
        time_series = np.loadtxt(filename, delimiter = ',')
        plot_pressure = air_pressure[:20]
        plot_z = pressure_to_height_std(plot_pressure * units.pascal)
        plot_T = time_series[-1].flatten()[:20]
        z_emit = np.interp(T_emit, plot_T.copy()[::-1], plot_z.copy()[::-1])
        # z_emit = pressure_to_height_std(P_emit * units.pascal)
        plt.plot(T_emit, z_emit, 'x', c='k')
        plt.plot(plot_T, plot_z,
                 '-o', markersize=1,label = '{0}: {1:.2f}'.format(label, z_emit))

    # plt.yscale('log')
    # plt.gca().invert_yaxis()
    plt.legend()
    # plt.show()
    plt.savefig(save_name)


# # PROFILE PLOTS
# base_name = '/project2/moyer/old_project/haynes/climt_files/varying_co2/320solar/'
# ppm_list    = [100, 150, 220, 270, 540, 1080, 1215]
# run_name = ['{0}i{1}_320solar/i{1}_320solar'.format(base_name, ppm) for ppm in ppm_list]
# Tair_csv_list = ['{0}_air_temperature.csv'.format(name) for name in run_name]
# air_pressure_csv = '{0}_air_pressure.csv'.format(run_name[0])
# air_pressure= np.loadtxt(air_pressure_csv, delimiter = ',')[0].flatten()
# save_name = '/home/haynes13/code/python/climproj/figures/diagnostics/tot/profiles.png'
# T_emit_list = np.array([267.90, 268.68, 269.24, 269.51, 271.11, 275.57, 275.60])
# plotProfiles(Tair_csv_list, ppm_list, T_emit_list, air_pressure, save_name)
