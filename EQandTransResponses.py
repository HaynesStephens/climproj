import numpy as np
import matplotlib.pyplot as plt
from metpy.calc import moist_lapse, relative_humidity_from_specific_humidity
from metpy.units import units
import os
import pickle


# # Plotting EQ Response

# In[90]:


def plotTempProfiles(ax, eq_air_temperature, air_pressure):
    ax0b = ax
    ln3 = ax0b.plot(eq_air_temperature,
                    air_pressure, '-o', markersize=3, c='r', label='Temp')
    ax0b.set_xlabel('K')
    ax0b.set_yscale('log')
    ax0b.axes.invert_yaxis()
    ax0b.set_ylabel('Pa')
    ax0b.grid()

    ### MOIST ADIABAT
    moist_adiabat_Tsurf = eq_air_temperature[0] * units.kelvin
    moist_adiabat_p = air_pressure * units.pascal
    moist_adiabat_profile = moist_lapse(moist_adiabat_p, moist_adiabat_Tsurf)
    ln4 = ax0b.plot(moist_adiabat_profile,
                    air_pressure, '-o', markersize=3, c='k', label='Moist Ad')
    ###

    lns = ln3 + ln4
    labs = [l.get_label() for l in lns]
    ax0b.legend(lns, labs, loc=2)


# In[91]:


def plotHumProfiles(ax, eq_q, eq_air_temperature, air_pressure):
    ax0 = ax
    ln1 = ax0.plot(eq_q * 1000,
                   air_pressure, '-o',
                   markersize=3, c='b', label='spec. hum.')
    ax0.set_yscale('log')
    ax0.axes.invert_yaxis()
    ax0.set_xlabel('g/kg')
    ax0.set_ylabel('Pa')
    ax0.grid()

    ### Relative Humidity Profile ###
    ax1 = ax0.twiny()
    rh_q = eq_q * units('kg/kg')
    rh_T = eq_air_temperature * units.kelvin
    rh_P = air_pressure * units.pascal
    rh_RH = relative_humidity_from_specific_humidity(rh_q, rh_T, rh_P)
    ln2 = ax1.plot(rh_RH,
                   air_pressure, '-o',
                   markersize=3, c='y', label='rel. hum.')
    #################################

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax0.legend(lns, labs, loc=2)


# In[152]:


def plotEQvals(ax, eq_pkl):
    ax1 = ax
    ax1.set_xticks([])
    ax1.set_yticks([])
    Tsurf = eq_pkl['surface_temperature'][0, 0]
    LH = eq_pkl['surface_upward_latent_heat_flux'][0, 0]
    SH = eq_pkl['surface_upward_sensible_heat_flux'][0, 0]
    LWsurf = (eq_pkl['upwelling_longwave_flux_in_air'] -
              eq_pkl['downwelling_longwave_flux_in_air'])[0, 0, 0]
    SWsurf = (eq_pkl['upwelling_shortwave_flux_in_air'] -
              eq_pkl['downwelling_shortwave_flux_in_air'])[0, 0, 0]
    netsurf = LWsurf + SWsurf + LH + SH
    LWtoa = (eq_pkl['upwelling_longwave_flux_in_air'] -
             eq_pkl['downwelling_longwave_flux_in_air'])[-1, 0, 0]
    SWtoa = (eq_pkl['upwelling_shortwave_flux_in_air'] -
             eq_pkl['downwelling_shortwave_flux_in_air'])[-1, 0, 0]
    nettoa = LWtoa + SWtoa
    Qsurf = eq_pkl['specific_humidity'][0, 0, 0]
    Qtot = np.sum(eq_pkl['specific_humidity'])
    convprec = eq_pkl['convective_precipitation_rate'][0, 0]
    stratprec = eq_pkl['stratiform_precipitation_rate'][0, 0]
    celltext = [['$\\bf{Surface}$', ''],
                ['Tsurf (K)', np.round(Tsurf, 2)],
                ['Qsurf (kg/kg)', np.round(Qsurf, 5)],
                ['LH (Wm^-2)', np.round(LH, 2)],
                ['SH (Wm^-2)', np.round(SH, 2)],
                ['LW (Wm^-2)', np.round(LWsurf, 2)],
                ['SW (Wm^-2)', np.round(SWsurf, 2)],
                ['net surf (Wm^-2)', np.round(netsurf, 2)],
                ['$\\bf{TOA}$', ''],
                ['SWinc (Wm^-2)', -np.round(eq_pkl['downwelling_shortwave_flux_in_air'][-1, 0, 0], 2)],
                ['SWtoa (Wm^-2)', np.round(SWtoa, 2)],
                ['net toa (Wm^-2)', np.round(nettoa, 2)],
                ['$\\bf{Total}$', ''],
                ['Qtot (kg/kg)', np.round(Qtot, 5)],
                ['ConvPrec (mm/day)', np.round(convprec, 2)],
                ['StratPrec (mm/day)', np.round(stratprec, 2)]]
    ax1.table(cellText=celltext, cellLoc='center', loc='center', fontsize=1)


# In[153]:


def plotTsurfPrecipLH(ax, time_adj, tsurf, precip, time_title, lh_flux, strat_prec='None'):
    ax2 = ax
    precip_flux = precip * (1 / 86400) * (2556) * (10 ** 3)
    ln1 = ax2.plot(time_adj, precip_flux, '-', c='b', label='Precip', linewidth=2)
    ax2.set_xlabel(time_title)
    ax2.grid()
    ln2 = ax2.plot(time_adj, lh_flux, '--', c='y', label='LH Flux', linewidth=1)
    ax2.set_ylabel('Wm$^{-2}$')

    ax2b = ax2.twinx()
    ln3 = ax2b.plot(time_adj, tsurf, '-.', c='k', label='Tsurf')
    ax2b.set_ylabel('K')

    if strat_prec == 'None':
        lns = ln1 + ln2 + ln3
    else:
        strat_prec_flux = strat_prec * (1 / 86400) * (2556) * (10 ** 3)
        ln4 = ax2.plot(time_adj, strat_prec_flux, '-', c='r', label='StratPrec', linewidth=2)
        lns = ln1 + ln2 + ln3 + ln4
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=1)


# In[154]:


def plotFluxes(ax, time_adj, net_flux_surface, sh_flux, lh_flux, net_flux_toa, time_title):
    ax3 = ax
    ax3.plot(time_adj, net_flux_surface, c='y', label='Rad')
    ax3.plot(time_adj, sh_flux, c='r', label='SH')
    ax3.plot(time_adj, lh_flux, c='b', label='LH')
    ax3.plot(time_adj, net_flux_surface + lh_flux + sh_flux, c='#7570b3', label='Surf')
    ax3.plot(time_adj, net_flux_toa, c='#d95f02', label='TOA')
    ax3.set_title('Fluxes (Up is +)')
    ax3.set_xlabel(time_title)
    ax3.set_ylabel('Wm$^{-2}$')
    # ax3.set_ylim(-50, 250)
    ax3.legend()
    ax3.grid()


# In[342]:


def plotEQResponse(job_name, test_dir='', save_step=36):
    base_name = '/project2/moyer/old_project/haynes/climt_files/'
    #     file_name = '{0}/{1}/{1}'.format(base_name, job_name)
    file_name = '{0}{1}{2}/{2}'.format(base_name, test_dir, job_name)
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    #     plot_name = '{0}/{1}/{1}_time_series.pdf'.format(plot_base, job_name)
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'EQandTransResponses/', test_dir, 'eq')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_eq.png'.format(plot_dir, job_name)
    print(plot_name)

    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    def loadPKL(filename, pkl_type):
        pkl_file = open('{0}_pkl_{1}.pkl'.format(filename, pkl_type), 'rb')
        pkl_dict = pickle.load(pkl_file)
        return pkl_dict

    time_arr = loadData(file_name, 'time')
    time_adj = time_arr / (3600 * 24)
    time_title = 'Days'
    lh_flux = loadData(file_name, 'surface_upward_latent_heat_flux')
    precip = loadData(file_name, 'convective_precipitation_rate')

    try:
        strat_prec = loadData(file_name, 'stratiform_precipitation_rate')
    except:
        strat_prec = 'None'

    tsurf = loadData(file_name, 'surface_temperature')
    co2_ppm = loadData(file_name, 'mole_fraction_of_carbon_dioxide_in_air')[0, 0] * (10 ** 6)

    upwelling_longwave_flux_in_air = loadData(file_name, 'upwelling_longwave_flux_in_air')
    upwelling_shortwave_flux_in_air = loadData(file_name, 'upwelling_shortwave_flux_in_air')
    downwelling_longwave_flux_in_air = loadData(file_name, 'downwelling_longwave_flux_in_air')
    downwelling_shortwave_flux_in_air = loadData(file_name, 'downwelling_shortwave_flux_in_air')

    net_flux = (upwelling_longwave_flux_in_air +
                upwelling_shortwave_flux_in_air -
                downwelling_longwave_flux_in_air -
                downwelling_shortwave_flux_in_air)

    net_flux_surface = net_flux[:, 0]
    net_flux_toa = net_flux[:, -1]

    eq_pkl = loadPKL(file_name, 'eq')
    air_pressure_on_interface_levels = eq_pkl['air_pressure_on_interface_levels'].flatten()
    air_pressure = eq_pkl['air_pressure'].flatten()
    eq_air_temperature = eq_pkl['air_temperature'].flatten()
    eq_sw_up = eq_pkl['upwelling_shortwave_flux_in_air'].copy()
    eq_sw_dn = eq_pkl['downwelling_shortwave_flux_in_air'].copy()
    eq_lw_up = eq_pkl['upwelling_longwave_flux_in_air'].copy()
    eq_lw_dn = eq_pkl['downwelling_longwave_flux_in_air'].copy()
    eq_net_flux = np.reshape((eq_sw_up + eq_lw_up - eq_sw_dn - eq_lw_dn), (29, 1))
    eq_q = eq_pkl['specific_humidity'].flatten()

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    plotTempProfiles(axes[0, 0], eq_air_temperature, air_pressure)

    plotHumProfiles(axes[0, 1], eq_q, eq_air_temperature, air_pressure)

    plotTsurfPrecipLH(axes[1, 0], time_adj, tsurf, precip, time_title, lh_flux, strat_prec=strat_prec)

    plotEQvals(axes[1, 1], eq_pkl)

    fig.suptitle('CO$_2$: {0} ppm'.format(co2_ppm // 1), fontsize=10,
                 bbox=dict(facecolor='none', edgecolor='green'),
                 x=0.53, y=0.5)
    plt.tight_layout()
    plt.savefig(plot_name)


#     plt.show()


# In[343]:


def plotEQResponseShanshan(job_name):
    base_name = '/project2/moyer/old_project/haynes/climt_files/'
    file_name = '{0}{1}/{1}'.format(base_name, job_name)
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    plot_dir = '{0}{1}{2}'.format(plot_base, 'EQandTransResponses/', job_name)
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_eq.png'.format(plot_dir, job_name)

    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    mid_levels = 28
    interface_levels = 29
    time_step_min = 10
    # SAVE STEP: KEY TO PLOTTING CORRECT TIMELINE
    save_step = 36

    time_arr = loadData(file_name, 'time')
    time_arr = np.arange(time_arr.size) * save_step * time_step_min * 60
    print(time_arr.size)
    time_adj = time_arr / (3600 * 24)
    time_title = 'Days'
    lh_flux = loadData(file_name, 'SrfLatFlx') * (-1)
    sh_flux = loadData(file_name, 'SrfSenFlx') * (-1)
    precip = loadData(file_name, 'precc')
    tsurf = loadData(file_name, 'Ts')
    co2_ppm = 270.0

    lwflx = loadData(file_name, 'lwflx')
    swflx = loadData(file_name, 'swflx')

    LwSrf = loadData(file_name, 'LwSrf')
    LwToa = loadData(file_name, 'LwToa')
    SwSrf = loadData(file_name, 'SwSrf')
    SwToa = loadData(file_name, 'SwToa')

    net_flux = (lwflx + swflx) * (-1)

    net_flux_surface = (LwSrf + SwSrf) * (-1)
    net_flux_toa = (LwToa + SwToa) * (-1)

    p = loadData(file_name, 'p')

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    eq_air_temperature = loadData(file_name, 'eqProfile_air_temperature')
    eq_net_flux = (-1) * loadData(file_name, 'eqProfile_net_radiation')
    plotEQProfiles(axes[0, 0], eq_net_flux, p[-1], eq_air_temperature, p[-1])

    #     moist_enthalpy = loadData(file_name, 'moist_enthalpy')
    plotTandME(axes[0, 1], time_adj, tsurf, time_title)

    plotTsurfPrecipLH(axes[1, 0], time_adj, tsurf, precip, time_title, lh_flux)

    plotFluxes(axes[1, 1], time_adj, net_flux_surface, sh_flux, lh_flux, net_flux_toa, time_title)

    fig.suptitle('CO$_2$: {0} ppm'.format(co2_ppm // 1), fontsize=10,
                 bbox=dict(facecolor='none', edgecolor='green'),
                 x=0.53, y=0.5)
    plt.tight_layout()
    plt.savefig(plot_name)


#     plt.show()


# # Transient Response Plotting

# In[344]:


def plotTransvals(ax, trans_pkl, control_pkl, response_index=0):
    ax1 = ax
    ax1.set_xticks([])
    ax1.set_yticks([])
    Tsurf0 = control_pkl['surface_temperature'][0, 0]
    Qsurf0 = control_pkl['specific_humidity'][0, 0, 0]
    LH0 = control_pkl['surface_upward_latent_heat_flux'][0, 0]
    SH0 = control_pkl['surface_upward_sensible_heat_flux'][0, 0]
    LWsurf0 = (control_pkl['upwelling_longwave_flux_in_air'] -
               control_pkl['downwelling_longwave_flux_in_air'])[0, 0, 0]
    SWsurf0 = (control_pkl['upwelling_shortwave_flux_in_air'] -
               control_pkl['downwelling_shortwave_flux_in_air'])[0, 0, 0]
    netsurf0 = LWsurf0 + SWsurf0 + LH0 + SH0
    LWtoa0 = (control_pkl['upwelling_longwave_flux_in_air'] -
              control_pkl['downwelling_longwave_flux_in_air'])[-1, 0, 0]
    SWtoa0 = (control_pkl['upwelling_shortwave_flux_in_air'] -
              control_pkl['downwelling_shortwave_flux_in_air'])[-1, 0, 0]
    nettoa0 = LWtoa0 + SWtoa0
    Qtot0 = np.sum(control_pkl['specific_humidity'])
    convprec0 = control_pkl['convective_precipitation_rate'][0, 0]
    stratprec0 = control_pkl['stratiform_precipitation_rate'][0, 0]

    Tsurf1 = trans_pkl['surface_temperature'][response_index][0, 0]
    Qsurf1 = trans_pkl['specific_humidity'][response_index][0, 0, 0]
    LH1 = trans_pkl['surface_upward_latent_heat_flux'][response_index][0, 0]
    SH1 = trans_pkl['surface_upward_sensible_heat_flux'][response_index][0, 0]
    LWsurf1 = (trans_pkl['upwelling_longwave_flux_in_air'][response_index] -
               trans_pkl['downwelling_longwave_flux_in_air'][response_index])[0, 0, 0]
    SWsurf1 = (trans_pkl['upwelling_shortwave_flux_in_air'][response_index] -
               trans_pkl['downwelling_shortwave_flux_in_air'][response_index])[0, 0, 0]
    netsurf1 = LWsurf1 + SWsurf1 + LH1 + SH1
    LWtoa1 = (trans_pkl['upwelling_longwave_flux_in_air'][response_index] -
              trans_pkl['downwelling_longwave_flux_in_air'][response_index])[-1, 0, 0]
    SWtoa1 = (trans_pkl['upwelling_shortwave_flux_in_air'][response_index] -
              trans_pkl['downwelling_shortwave_flux_in_air'][response_index])[-1, 0, 0]
    nettoa1 = LWtoa1 + SWtoa1
    Qtot1 = np.sum(trans_pkl['specific_humidity'][response_index])
    convprec1 = trans_pkl['convective_precipitation_rate'][response_index][0, 0]
    stratprec1 = trans_pkl['stratiform_precipitation_rate'][response_index][0, 0]

    celltext = [['$\\bf{Surface}$', '$\\bf{Response}$', '$\\bf{Shift}$'],
                ['Tsurf (K)', np.round(Tsurf1, 2), np.round((Tsurf1 - Tsurf0), 2)],
                ['Qsurf (kg/kg)', np.round(Qsurf1, 5), np.round((Qsurf1 - Qsurf0), 5)],
                ['LH (Wm^-2)', np.round(LH1, 2), np.round((LH1 - LH0), 2)],
                ['SH (Wm^-2)', np.round(SH1, 2), np.round((SH1 - SH0), 2)],
                ['LW (Wm^-2)', np.round(LWsurf1, 2), np.round((LWsurf1 - LWsurf0), 2)],
                ['SW (Wm^-2)', np.round(SWsurf1, 2), np.round((SWsurf1 - SWsurf0), 2)],
                ['net surf (Wm^-2)', np.round(netsurf1, 2), np.round((netsurf1 - netsurf0), 2)],
                ['$\\bf{TOA}$', '', ''],
                ['LWtoa (Wm^-2)', np.round(LWtoa1, 2), np.round((LWtoa1 - LWtoa0), 2)],
                ['SWtoa (Wm^-2)', np.round(SWtoa1, 2), np.round((SWtoa1 - SWtoa0), 2)],
                ['net toa (Wm^-2)', np.round(nettoa1, 2), np.round((nettoa1 - nettoa0), 2)],
                ['$\\bf{Total}$', '', ''],
                ['Qtot (kg/kg)', np.round(Qtot1, 5), np.round((Qtot1 - Qtot0), 5)],
                ['ConvPrec (mm/day)', np.round(convprec1, 2), np.round((convprec1 - convprec0), 2)],
                ['StratPrec (mm/day)', np.round(stratprec1, 2), np.round((stratprec1 - stratprec0), 2)]]
    ax1.table(cellText=celltext, cellLoc='center', loc='center', fontsize=1)


# In[345]:


def plotTransResponse(job_name, insol=320, test_dir=''):
    base_name = '/project2/moyer/old_project/haynes/climt_files/'
    #     file_name = '{0}/{1}/{1}'.format(base_name, job_name)
    file_name = '{0}{1}{2}/{2}'.format(base_name, test_dir, job_name)
    plot_base = '/home/haynes13/code/python/climproj/figures/'
    #     plot_name = '{0}/{1}/{1}_time_series.pdf'.format(plot_base, job_name)
    plot_dir = '{0}{1}{2}{3}'.format(plot_base, 'EQandTransResponses/', test_dir, 'trans')
    os.system('mkdir -p {0}'.format(plot_dir))
    plot_name = '{0}/{1}_trans.png'.format(plot_dir, job_name)
    print(plot_name)

    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    def loadPKL(filename, pkl_type):
        pkl_file = open('{0}_pkl_{1}.pkl'.format(filename, pkl_type), 'rb')
        pkl_dict = pickle.load(pkl_file)
        return pkl_dict

    control_type = '{0}solar'.format(insol)

    if test_dir == 'varying_solar/':
        control_job = 'i270_320solar_fullstore'
    else:
        control_job = 'i270_{0}_fullstore'.format(control_type)

    control_filename = '{0}{1}{2}/{2}'.format(base_name, 'control_fullstore/', control_job)
    control_pkl = loadPKL(control_filename, 'eq')
    trans_pkl = loadPKL(file_name, 'trans')

    #     precip = loadData(file_name, 'convective_precipitation_rate')

    #     try:
    #         strat_prec = loadData(file_name, 'stratiform_precipitation_rate')
    #     except:
    #         strat_prec = 'None'

    #     tsurf = loadData(file_name, 'surface_temperature')
    co2_ppm = loadData(file_name, 'mole_fraction_of_carbon_dioxide_in_air')[0, 0] * (10 ** 6)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    plotTempProfChange(axes[0, 0], trans_pkl, control_pkl)

    plotTransvals(axes[1, 1], trans_pkl, control_pkl)

    plotTransTempHumSeries(axes[1, 0], file_name, control_pkl)

    plotTransFluxSeries(axes[0, 1], file_name, control_pkl)

    fig.suptitle('CO$_2$: {0} ppm'.format(co2_ppm // 1), fontsize=10,
                 bbox=dict(facecolor='none', edgecolor='green'),
                 x=0.53, y=0.5)
    plt.tight_layout()
    plt.savefig(plot_name)


#     plt.show()


# In[346]:


def plotTempProfChange(ax, trans_pkl, control_pkl, response_index=0):
    control_P = control_pkl['air_pressure'].flatten()
    control_T = control_pkl['air_temperature'].flatten()
    trans_P = trans_pkl['air_pressure'][response_index].flatten()
    trans_T = trans_pkl['air_temperature'][response_index].flatten()
    assert np.array_equal(control_P, trans_P), "Why aren't the pressures the same?"
    ax0b = ax
    ln1 = ax0b.plot(control_T,
                    control_P, '--', markersize=3, c='r', label='T0')
    ln2 = ax0b.plot(trans_T,
                    trans_P, '-o', markersize=3, c='k', label='T0')
    ax0b.set_xlabel('K')
    ax0b.set_yscale('log')
    ax0b.axes.invert_yaxis()
    ax0b.set_ylabel('Pa')
    ax0b.grid()

    ### MOIST ADIABAT
    moist_control_T = control_T[0] * units.kelvin
    moist_control_P = control_P * units.pascal
    moist_control_profile = moist_lapse(moist_control_P, moist_control_T)
    ln3 = ax0b.plot(moist_control_profile,
                    control_P, '--', markersize=3, c='b', label='Moist cont.')

    moist_trans_T = trans_T[0] * units.kelvin
    moist_trans_P = trans_P * units.pascal
    moist_trans_profile = moist_lapse(moist_trans_P, moist_trans_T)
    ln4 = ax0b.plot(moist_trans_profile,
                    trans_P, '-o', markersize=3, c='y', label='Moist trans.')
    ###

    lns = ln1 + ln2 + ln3 + ln4
    labs = [l.get_label() for l in lns]
    ax0b.legend(lns, labs, loc=2)


# In[347]:


def plotTransFluxSeries(ax, file_name, control_pkl):
    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    def getTSeries0D(file_name, control_pkl, var):
        t_data = loadData(file_name, var)
        control_val = control_pkl[var][0]
        flux = np.append(control_val, t_data) / control_val[0]
        return flux

    def getTSeries1D(file_name, control_pkl, var, level):
        t_data = loadData(file_name, var)[:, level]
        control_val = control_pkl[var][:, :, 0][level]
        t_series = np.append(control_val, t_data) / control_val[0]
        return t_series

    time_arr = loadData(file_name, 'time') + (10 * 60)
    time_arr = np.append([0], time_arr)
    time_adj = time_arr / (3600 * 24)
    time_title = 'Days'

    lh_flux = getTSeries0D(file_name, control_pkl, 'surface_upward_latent_heat_flux')
    sh_flux = getTSeries0D(file_name, control_pkl, 'surface_upward_sensible_heat_flux')

    lw_up_surf = getTSeries1D(file_name, control_pkl, 'upwelling_longwave_flux_in_air', level=0)
    lw_dn_surf = getTSeries1D(file_name, control_pkl, 'downwelling_longwave_flux_in_air', level=0)

    sw_up_surf = getTSeries1D(file_name, control_pkl, 'upwelling_shortwave_flux_in_air', level=0)
    sw_dn_surf = getTSeries1D(file_name, control_pkl, 'downwelling_shortwave_flux_in_air', level=0)

    #     lw_up = np.append(control_pkl['upwelling_longwave_flux_in_air'][:,:,0],
    #                       loadData(file_name, 'upwelling_longwave_flux_in_air'))
    #     lw_dn = np.append(control_pkl['downwelling_longwave_flux_in_air'][:,:,0],
    #                       loadData(file_name, 'downwelling_longwave_flux_in_air'))
    #     sw_up = np.append(control_pkl['upwelling_shortwave_flux_in_air'][:,:,0],
    #                       loadData(file_name, 'upwelling_shortwave_flux_in_air'))
    #     sw_dn = np.append(control_pkl['downwelling_shortwave_flux_in_air'][:,:,0],
    #                       loadData(file_name, 'downwelling_shortwave_flux_in_air'))

    #     control_lw_surf = (control_pkl[upwelling_longwave_flux_in_air][:,:,0][0] -

    #     net_lw_surf = (loadData(file_name, 'upwelling_longwave_flux_in_air')[:,0] -
    #                    loadData(file_name, 'downwelling_longwave_flux_in_air')[:,0])
    #     net_lw_toa = net_lw[:,-1]

    #     net_sw = (sw_up - sw_dn)
    #     net_sw_surf = net_sw[:, 0]
    #     net_sw_toa = net_sw[:,-1]

    ax.plot(time_adj, sh_flux, label='SH')
    ax.plot(time_adj, lh_flux, label='LH')
    #     ax.plot(time_adj, lw_up_surf, '--', label='LWupsurf')
    ax.plot(time_adj, lw_dn_surf, '--', label='LWdnsurf')
    #     ax.plot(time_adj, sw_up_surf, '-.', label='SWupsurf')
    ax.plot(time_adj, sw_dn_surf, '-.', label='SWdnsurf')
    ax.set_title('Fluxes')
    ax.set_xlabel(time_title)
    ax.set_ylabel('%')
    ax.set_xlim(0, 1)
    ax.set_ylim(0.95, 1.2)
    ax.legend(loc=2)
    ax.grid()


# In[348]:


def plotTransTempHumSeries(ax, file_name, control_pkl):
    def loadData(file_name, var):
        return np.loadtxt('{0}_{1}.csv'.format(file_name, var), delimiter=',')

    def getTSeries0D(file_name, control_pkl, var):
        t_data = loadData(file_name, var)
        control_val = control_pkl[var][0]
        t_series = np.append(control_val, t_data) / control_val[0]
        return t_series

    time_arr = loadData(file_name, 'time') + (10 * 60)
    time_arr = np.append([0], time_arr)
    time_adj = time_arr / (3600 * 24)
    time_title = 'Days'

    tsurf = getTSeries0D(file_name, control_pkl, 'surface_temperature')

    control_q_tot = np.sum(control_pkl['specific_humidity'])
    q_tot = np.sum(loadData(file_name, 'specific_humidity'), axis=1)
    q_tot = np.append([control_q_tot], q_tot) / control_q_tot

    control_q_surf = control_pkl['specific_humidity'][0, 0, 0]
    q_surf = loadData(file_name, 'specific_humidity')[:, 0]
    q_surf = np.append([control_q_surf], q_surf) / control_q_surf

    ax.plot(time_adj, tsurf, label='Tsurf')
    ax.plot(time_adj, q_tot, '--', label='Qtot')
    ax.plot(time_adj, q_surf, '-.', label='Qsurf')
    ax.set_title('Temp + Humidity')
    ax.set_xlabel(time_title)
    ax.set_ylabel('%')
    ax.set_xlim(0, 1)
    ax.set_ylim(0.95, 1.05)
    ax.legend(loc=2)
    ax.grid()


# Vary co2 run
co2_ppm_list    = [2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215]
co2_ppm_list    = [100, 150, 220, 270, 540, 1080, 1215]
insol_list      = [290, 320]
insol_list      = [320]
for insol in insol_list:
    test_dir = 'varying_co2/{0}solar/'.format(insol)
    for ppm in co2_ppm_list:
        job_name = 'i{0}_{1}solar'.format(ppm, insol)
        plotEQResponse(job_name, test_dir=test_dir)
        plotTransResponse(job_name, insol=insol, test_dir=test_dir)
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
#     plotTransResponse(job_name, insol=insol, test_dir=test_dir)
#     print('DONE.', job_name)


# # Diagnostics run
# input_ppm_list = [100, 150, 220, 270, 540, 1080, 1215]
# run_type_list  = ['rad', 'tot']
# var_list       = ['q', 'T', 'co2']
# insol = 320
# for input_ppm in input_ppm_list:
#     for run_type in run_type_list:
#         for var in var_list:
#             test_dir = 'diagnostic/{0}/{1}/'.format(run_type, var)
#             job_name = 'diagnostic_{0}_{1}_input{2}'.format(run_type, var, input_ppm)
#             print(job_name)
#             plotEQResponse(job_name, test_dir=test_dir)
#             plotTransResponse(job_name, insol=insol, test_dir=test_dir)
#             print('DONE.', job_name)

