import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd


def getDF(job_name, test_dir=''):
    base_name = '/project2/moyer/old_project/haynes/climt_files/'
    file_name = '{0}{1}{2}/{2}'.format(base_name, test_dir, job_name)

    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    time_arr = loadData(file_name, 'time')
    lh_flux = loadData(file_name, 'surface_upward_latent_heat_flux')
    sh_flux = loadData(file_name, 'surface_upward_sensible_heat_flux')

    tsurf = loadData(file_name, 'surface_temperature')

    lw_up       = loadData(file_name, 'upwelling_longwave_flux_in_air')
    sw_up       = loadData(file_name, 'upwelling_shortwave_flux_in_air')
    lw_dn       = loadData(file_name, 'downwelling_longwave_flux_in_air')
    sw_dn       = loadData(file_name, 'downwelling_shortwave_flux_in_air')

    data = {'time':time_arr,
            'tsurf': tsurf,
            'lh': lh_flux,
            'sh': sh_flux,
            'lw_up_surf': lw_up[:, 0],
            'lw_dn_surf': lw_dn[:, 0],
            'sw_up_surf': sw_up[:, 0],
            'sw_dn_surf': sw_dn[:, 0],
            'lw_up_toa': lw_up[:, -1],
            'lw_dn_toa': lw_dn[:, -1],
            'sw_up_toa': sw_up[:, -1],
            'sw_dn_toa': sw_dn[:, -1],}
    df = pd.DataFrame(data, index=time_arr)
    df['net_toa'] = (df['lw_up_toa'] + df['sw_up_toa']) - (df['lw_dn_toa'] + df['sw_dn_toa'])
    df['net_surf'] = (df['lw_up_surf'] + df['sw_up_surf']) - (df['lw_dn_surf'] + df['sw_dn_surf']) + df['lh'] + df['sh']
    return df


def plotSeries(df, job_name, test_dir='', ppm = None):
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'eqCheck/', test_dir, 'eq')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_eqCheck.png'.format(plot_dir, job_name)
    print(plot_name)

    yrs_back = 3600 * 24 * 365 * 0.3
    time_max = df.time.max() - yrs_back
    mean_df = df[df.time > time_max]

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 10))

    def plotVal(ax, val):
        mean_val = mean_df[val].mean()
        ax.plot(df.time, df[val] - mean_val, label = '{0}:{1:.2f}'.format(val, mean_val))
        ax.set_ylim(-1, 1)

    ax0 = axes[0]
    plotVal(ax0, 'lw_up_surf')
    plotVal(ax0, 'lw_dn_surf')
    plotVal(ax0, 'sw_up_surf')
    plotVal(ax0, 'sw_dn_surf')
    ax0.legend()

    ax1 = axes[1]
    plotVal(ax1, 'lw_up_toa')
    plotVal(ax1, 'lw_dn_toa')
    plotVal(ax1, 'sw_up_toa')
    plotVal(ax1, 'sw_dn_toa')
    ax1.legend()

    ax2 = axes[2]
    plotVal(ax2, 'lh')
    plotVal(ax2, 'sh')
    ax2.legend()

    ax0.set_title('CO$_2$: {0} ppm'.format(ppm // 1))
    plt.tight_layout()
    # plt.show()
    plt.savefig(plot_name)


def plotRolling(df, job_name, test_dir='', ppm = None):
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'eqCheck/', test_dir, 'eq')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_eqCheck.png'.format(plot_dir, job_name)
    print(plot_name)

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 10))
    ax0, ax1, ax2 = axes


    ax0.set_title('CO$_2$: {0} ppm'.format(ppm // 1))
    plt.tight_layout()
    # plt.show()
    plt.savefig(plot_name)


# # Vary co2 run
# co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
# insol_list      = [290, 320]
# for insol in insol_list:
#     test_dir = 'varying_co2/{0}solar/'.format(insol)
#     for ppm in co2_ppm_list:
#         job_name = 'i{0}_{1}solar'.format(ppm, insol)
#         plotEQCheck(job_name, ppm, test_dir=test_dir)
#         print('DONE.', job_name)


# # Vary insol run
# insol_list = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
#               270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]
# test_dir = 'varying_solar/'
# for insol in insol_list:
#     job_name = 'i270_{0}solar'.format(insol)
#     plotEQResponse(job_name, test_dir=test_dir)
#     print('DONE.', job_name)


# Vary co2 qRadCst run
co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol           = 320
test_dir = 'varying_co2_qRadCst/'
for ppm in co2_ppm_list:
    job_name = 'i{0}_{1}solar_qRadCst'.format(ppm, insol)
    df = getDF(job_name, test_dir=test_dir)
    plotSeries(df, job_name, test_dir=test_dir, ppm=ppm)
    print('DONE.', job_name)
