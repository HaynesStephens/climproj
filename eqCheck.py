import numpy as np
import matplotlib.pyplot as plt
import os

def plotEQCheck(job_name, test_dir=''):
    base_name = '/project2/moyer/old_project/haynes/climt_files/'
    file_name = '{0}{1}{2}/{2}'.format(base_name, test_dir, job_name)
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'eqCheck/', test_dir, 'eq')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_eqCheck.png'.format(plot_dir, job_name)
    print(plot_name)

    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    time_arr = loadData(file_name, 'time')
    time_adj = time_arr / (3600 * 24)
    lh_flux = loadData(file_name, 'surface_upward_latent_heat_flux')
    sh_flux = loadData(file_name, 'surface_upward_sensible_heat_flux')

    tsurf = loadData(file_name, 'surface_temperature')
    co2_ppm = loadData(file_name, 'mole_fraction_of_carbon_dioxide_in_air')[0, 0] * (10 ** 6)

    upwelling_longwave_flux_in_air      = loadData(file_name, 'upwelling_longwave_flux_in_air')
    upwelling_shortwave_flux_in_air     = loadData(file_name, 'upwelling_shortwave_flux_in_air')
    downwelling_longwave_flux_in_air    = loadData(file_name, 'downwelling_longwave_flux_in_air')
    downwelling_shortwave_flux_in_air   = loadData(file_name, 'downwelling_shortwave_flux_in_air')

    net_flux = (upwelling_longwave_flux_in_air +
                upwelling_shortwave_flux_in_air -
                downwelling_longwave_flux_in_air -
                downwelling_shortwave_flux_in_air)

    net_flux_surface    = net_flux[:, 0] + lh_flux + sh_flux
    net_flux_toa        = net_flux[:, -1]

    years_back      = 0.30
    seconds_back    = years_back * 365.25 * 24 * 60 * 60
    t_final         = time_arr[-1]
    eq_index        = np.where(time_arr > (t_final - seconds_back))

    tsurf_mean              = np.mean(tsurf[eq_index], axis=0)
    net_flux_surface_mean   = np.mean(net_flux_surface[eq_index], axis=0)
    net_flux_toa_mean       = np.mean(net_flux_toa[eq_index], axis=0)


    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 10))
    ax0, ax1, ax2 = axes

    ax0.plot(time_adj, net_flux_toa - net_flux_toa_mean,
             c='k', label = str(net_flux_toa_mean))
    ax0.legend(frameon=False)
    ax0.set_ylabel('toa [Wm^-2]')
    ax0.set_ylim(-0.5, 0.5)
    ax0.set_xlim(time_adj[eq_index][0], time_adj[eq_index][-1])

    ax1.plot(time_adj, net_flux_surface - net_flux_surface_mean,
             c='k', label = str(net_flux_surface_mean))
    ax1.legend(frameon=False)
    ax1.set_ylabel('surf [Wm^-2]')
    ax1.set_ylim(-0.5, 0.5)

    ax2.plot(time_adj, tsurf-tsurf_mean, c='k', label = str(tsurf_mean))
    ax2.legend(frameon=False)
    ax2.set_ylabel('Tsurf [K]')
    ax2.set_ylim(-0.5, 0.5)


    ax2.set_xlabel('Days')



    ax0.set_title('CO$_2$: {0} ppm'.format(co2_ppm // 1))
    plt.tight_layout()
    plt.show()
    # plt.savefig(plot_name)


# Vary co2 run
co2_ppm_list    = [2]#, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol_list      = [290]#, 320]
for insol in insol_list:
    test_dir = 'varying_co2/{0}solar/'.format(insol)
    for ppm in co2_ppm_list:
        job_name = 'i{0}_{1}solar'.format(ppm, insol)
        plotEQCheck(job_name, test_dir=test_dir)
        # plotTransResponse(job_name, insol=insol, test_dir=test_dir)
        print('DONE.', job_name)


# # Vary insol run
# insol_list = [200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265,
#               270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335]
# test_dir = 'varying_solar/'
# for insol in insol_list:
#     job_name = 'i270_{0}solar'.format(insol)
#     plotEQResponse(job_name, test_dir=test_dir)
#     plotTransResponse(job_name, test_dir=test_dir)
#     print('DONE.', job_name)


# # Vary co2 qRadCst run
# co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
# insol           = 320
# test_dir = 'varying_co2_qRadCst/'
# for ppm in co2_ppm_list:
#     job_name = 'i{0}_{1}solar_qRadCst'.format(ppm, insol)
#     plotEQResponse(job_name, test_dir=test_dir)
#     # plotTransResponse(job_name, insol=insol, test_dir=test_dir)
#     print('DONE.', job_name)
