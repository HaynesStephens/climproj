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


def plotSeries(df, job_name, test_dir='', title = None):
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'eqCheck/', test_dir, 'eq')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_evolution.png'.format(plot_dir, job_name)
    print(plot_name)

    yrs_back = 3600 * 24 * 30
    time_max = df.time.max() - yrs_back
    mean_df = df[df.time > time_max]

    fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(10, 10))

    def plotVal(ax, val):
        mean_val = mean_df[val].mean()
        ax.plot(df.time / (3600*24), df[val] - mean_val, label = '{0}:{1:.2f}'.format(val, mean_val))
        ax.set_ylim(-1, 1)

    ax0 = axes[0]
    plotVal(ax0, 'net_toa')
    plotVal(ax0, 'lw_up_toa')
    plotVal(ax0, 'lw_dn_toa')
    plotVal(ax0, 'sw_up_toa')
    plotVal(ax0, 'sw_dn_toa')
    ax0.set_xlabel('Days')
    ax0.set_ylabel('Wm^-2 (mean +/-)')
    ax0.legend()

    ax1 = axes[1]
    plotVal(ax1, 'lh')
    plotVal(ax1, 'sh')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('Wm^-2 (mean +/-)')
    ax1.legend()

    ax2 = axes[2]
    plotVal(ax2, 'net_surf')
    plotVal(ax2, 'lw_up_surf')
    plotVal(ax2, 'lw_dn_surf')
    plotVal(ax2, 'sw_up_surf')
    plotVal(ax2, 'sw_dn_surf')
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Wm^-2 (mean +/-)')
    ax2.legend()

    ax3 = axes[3]
    tsurf_mean = mean_df.tsurf.mean()
    ax3.plot(df.time / (3600*24), df.tsurf, label = '{0}:{1:.2f}'.format('tsurf', tsurf_mean))
    ax3.set_ylim(tsurf_mean - 0.5, tsurf_mean + 0.5)
    ax3.set_xlabel('Days')
    ax3.set_ylabel('Tsurf (K)')
    ax3.legend()

    if 'co2' in test_dir:
        ax0.set_title('CO$_2$: {0} ppm'.format(title // 1))
    else:
        ax0.set_title('insol: {0}'.format(title // 1))
    plt.tight_layout()
    # plt.show()
    plt.savefig(plot_name)


def plotRolling(df_roll, job_name, test_dir='', title = None):
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'eqCheck/', test_dir, 'mean')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_mean.png'.format(plot_dir, job_name)
    print(plot_name)

    fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(10, 10))

    def plotVal(ax, val):
        last_val = df_roll[val].iloc[-1]
        ax.plot(df.time / (3600 * 24), df_roll[val] - last_val, label='{0}:{1:.2f}'.format(val, last_val))
        ax.set_ylim(-1, 1)

    ax0 = axes[0]
    plotVal(ax0, 'net_toa')
    plotVal(ax0, 'lw_up_toa')
    plotVal(ax0, 'lw_dn_toa')
    plotVal(ax0, 'sw_up_toa')
    plotVal(ax0, 'sw_dn_toa')
    ax0.set_xlabel('Days')
    ax0.set_ylabel('Wm^-2 (mean +/-)')
    ax0.legend()

    ax1 = axes[1]
    plotVal(ax1, 'lh')
    plotVal(ax1, 'sh')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('Wm^-2 (mean +/-)')
    ax1.legend()

    ax2 = axes[2]
    plotVal(ax2, 'net_surf')
    plotVal(ax2, 'lw_up_surf')
    plotVal(ax2, 'lw_dn_surf')
    plotVal(ax2, 'sw_up_surf')
    plotVal(ax2, 'sw_dn_surf')
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Wm^-2 (mean +/-)')
    ax2.legend()

    ax3 = axes[3]
    tsurf_last = df_roll.tsurf.iloc[-1]
    ax3.plot(df.time / (3600 * 24), df.tsurf, label='{0}:{1:.2f}'.format('tsurf', tsurf_last))
    ax3.set_ylim(tsurf_last - 0.5, tsurf_last + 0.5)
    ax3.set_xlabel('Days')
    ax3.set_ylabel('Tsurf (K)')
    ax3.legend()

    if 'co2' in test_dir:
        ax0.set_title('CO$_2$: {0} ppm'.format(title // 1))
    else:
        ax0.set_title('insol: {0}'.format(title // 1))
    plt.tight_layout()
    # plt.show()
    plt.savefig(plot_name)


# Vary co2 run
co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol_list      = [290, 320]
for insol in insol_list:
    test_dir = 'varying_co2/{0}solar/'.format(insol)
    for ppm in co2_ppm_list:
        job_name = 'i{0}_{1}solar'.format(ppm, insol)
        df = getDF(job_name, test_dir=test_dir)
        df_roll = df.rolling(120).mean()
        plotSeries(df, job_name, test_dir=test_dir, title=ppm)
        plotRolling(df_roll, job_name, test_dir=test_dir, title=ppm)
        print('DONE.', job_name)


# Vary insol run
insol_list = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
              270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]
test_dir = 'varying_solar/'
for insol in insol_list:
    job_name = 'i270_{0}solar'.format(insol)
    df = getDF(job_name, test_dir=test_dir)
    df_roll = df.rolling(120).mean()
    plotSeries(df, job_name, test_dir=test_dir, title=insol)
    plotRolling(df_roll, job_name, test_dir=test_dir, title=insol)
    print('DONE.', job_name)


# Vary co2 qRadCst run
co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol           = 320
test_dir = 'varying_co2_qRadCst/'
for ppm in co2_ppm_list:
    job_name = 'i{0}_{1}solar_qRadCst'.format(ppm, insol)
    df = getDF(job_name, test_dir=test_dir)
    df_roll = df.rolling(120).mean()
    plotSeries(df, job_name, test_dir=test_dir, title=ppm)
    plotRolling(df_roll, job_name, test_dir=test_dir, title=ppm)
    print('DONE.', job_name)

































