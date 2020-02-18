import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import os
import seaborn as sns
import copy


def loadProfiles(co2_ppm, qRadCst=False):
    if not qRadCst:
        pkl = pickle.load(open('{0}i{1}_320solar_pkl_eq.pkl'.format(pkl_dir, co2_ppm), 'rb'))
    else:
        pkl = pickle.load(open('{0}i{1}_320solar_qRadCst_pkl_eq.pkl'.format(pkl_dir, co2_ppm), 'rb'))
    lw      = pkl['air_temperature_tendency_from_longwave'].flatten()
    sw      = pkl['air_temperature_tendency_from_shortwave'].flatten()
    print(pkl['air_temperature_tendency_from_convection'][0])
    print(pkl['air_temperature_tendency_from_longwave'][-1])
    conv    = pkl['air_temperature_tendency_from_convection'].flatten()
    print(lw.shape)
    print(conv.shape)
    tot     = lw + sw + conv
    p       = pkl['air_pressure'].flatten()
    data    = {'lw':lw, 'sw':sw, 'conv':conv, 'tot':tot}
    df = pd.DataFrame(data, index=p)
    return df


def plotdTdtVertSingle(co2_ppm, qRadCst=False, save=False):
    if not qRadCst:
        save_name = '/content/drive/My Drive/Research/climproj/figures/TraDinh/varyingCO2_320/dTdtVertSingle320_{0}.png'.format(co2_ppm)
        pkl = pickle.load(open('{0}i{1}_320solar_pkl_eq.pkl'.format(pkl_dir, co2_ppm), 'rb'))
        title = '{0} ppm'.format(co2_ppm)
    else:
        pkl = pickle.load(open('{0}i{1}_320solar_qRadCst_pkl_eq.pkl'.format(pkl_dir, co2_ppm), 'rb'))
        save_name = '/content/drive/My Drive/Research/climproj/figures/TraDinh/qRadCst/dTdtVertSingle320_{0}_qRadCst.png'.format(co2_ppm)
        title = '{0} ppm, qRadCst'.format(co2_ppm)

    dTdt_lw = pkl['air_temperature_tendency_from_longwave'].flatten()
    dTdt_sw = pkl['air_temperature_tendency_from_shortwave'].flatten()
    dTdt_conv = pkl['air_temperature_tendency_from_convection'].flatten()

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
    fig = plt.figure(figsize=(16, 16))
    spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[2.5,1])

    ax = fig.add_subplot(spec[0, 0])
    ax.tick_params(which = 'major', direction='in', bottom = True, left = True)
    ax.tick_params(which = 'minor', direction='in', bottom = True, left = True)

    ax1 = fig.add_subplot(spec[0, 1])
    ax1.tick_params(which = 'major', direction='in', bottom = True, left = True)
    ax1.tick_params(which = 'minor', direction='in', bottom = True, left = True)
    plt.setp(ax1.get_yticklabels(), visible=False)

    ax1t = ax1.twiny()
    ax1t.tick_params(which = 'major', direction='in', top = True)
    ax1t.tick_params(which = 'minor', direction='in', top = True)
    plt.setp(ax1t.get_yticklabels(), visible=False)

    ax.plot(dTdt_lw, air_pressure, c='#d95f02', label='LW', marker='o')
    ax.plot(dTdt_sw, air_pressure, c='#1b9e77', label='SW', marker='o')
    ax.plot(dTdt_conv, air_pressure, c='#7570b3', label='Conv', marker='o')
    ax.plot(dTdt_sw + dTdt_lw + dTdt_conv, air_pressure, c='black', label='Tot', marker='x', markersize=8)

    ax.invert_yaxis()
    ax.set_yscale('log')
    ax.axvline(0, c = 'k', linestyle = 'dotted')
    ax.set_xlabel('K/day')
    ax.set_ylabel('log(Pa)')
    ax.set_xlim(-6, 6)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.set_title(title)
    ax.legend()

    sh = pkl['specific_humidity'].flatten()
    ax1t.plot(sh, air_pressure, c='blue', label='SH', marker='o')
    t = pkl['air_temperature'].flatten()
    ax1.plot(t, air_pressure, c='red', label = 'T', marker = '+')
    ax1.invert_yaxis()
    ax1.set_yscale('log')

    if save:
        plt.savefig(save_name)
    return True


def makeGif(gif_name = 'dorian', fps = 1):
    # For making Gifs
    import glob
    import moviepy.editor as mpy
    filedir     = '/content/drive/My Drive/my_bootcamp/dorianfigs/'
    writedir    = '/content/drive/My Drive/my_bootcamp/'

    # Get all the pngs in the current directory
    file_list = glob.glob('{0}*.png'.format(filedir))

    # Sort the images by number, still have to name them reasonably well to begin with
    list.sort(file_list, key=lambda x: x.split('.')[0].split('/')[-1])
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{0}{1}.gif'.format(writedir, gif_name), fps=fps)
