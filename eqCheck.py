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
    time_title = 'Days'
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

    air_pressure_on_interface_levels = np.array([101320.00000000001, 100768.79955129435,
                                                 99623.53236467099, 97897.77890813441,
                                                 95612.00299988744, 92793.30915035386,
                                                 89475.12115967272, 85696.7857812654,
                                                 81503.10615205651, 76943.81052094584,
                                                 72072.96257624963, 66948.3203635812,
                                                 61630.651396513, 56183.01208129487,
                                                 50670.00000000001, 45156.98791870526,
                                                 39709.348603486964, 34391.67963641881,
                                                 29267.037423745773, 24396.189479064356,
                                                 19836.89384795723, 15643.214218720825,
                                                 11864.87884032738, 8546.69084963619,
                                                 5727.997000119585, 3442.221091853463,
                                                 1716.4676353184418, 571.2004487176397, 20.0])

    air_pressure = np.array([101044.31028193687, 100195.77632999333,
                             98759.75807374805, 96753.28367666947,
                             94200.14571469926, 91130.61904627077,
                             87581.1018155814, 83593.68384655102,
                             79215.6475452361, 74498.90722888586,
                             69499.39352997651, 64276.39017480756,
                             58891.83100071549, 53409.56554755569,
                             47894.60193160131, 42412.335978499286,
                             37027.775754769726, 31804.770689935383,
                             26805.254424202667, 22088.51034726227,
                             17710.468509501374, 13723.042175710103,
                             10173.511710084977, 7103.962555307896,
                             4550.781983286063, 2544.211053128718,
                             1107.8840498713269, 256.08938210400294])

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_title('CO$_2$: {0} ppm'.format(co2_ppm // 1))
    plt.tight_layout()
    # plt.savefig(plot_name)


# Vary co2 run
co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
insol_list      = [290, 320]
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
