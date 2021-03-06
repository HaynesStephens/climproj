import pickle
import numpy as np
import matplotlib.pyplot as plt


def getMass_H2O(pkl):
    g = 9.8
    q = pkl['specific_humidity'].flatten()
    p_diff = np.abs(np.diff(pkl['air_pressure_on_interface_levels'].flatten()))
    mass = (q * p_diff) / g
    print('PW Mass (kg)', np.sum(mass))
    return np.sum(mass)

def getPKLvals(file_name):
    file_load = open(file_name, 'rb')
    pkl = pickle.load(file_load)
    pw = getMass_H2O(pkl)
    tsurf = pkl['surface_temperature'].flatten()[0]
    print('Tsurf (K)', tsurf)
    return pw, tsurf

insol=320
test_dir = '/project2/moyer/old_project/haynes/climt_files/varying_co2/{0}solar/'.format(insol)
ppm_list = np.array([2, 5, 10, 20, 50, 100, 150, 190, 220, 270, 405, 540, 675, 756, 1080, 1215])
job_list = ['i{0}_{1}solar'.format(ppm, insol) for ppm in ppm_list]
file_name_list = ['{0}{1}/{1}_pkl_eq.pkl'.format(test_dir, job_name) for job_name in job_list]

pkl_vals = [getPKLvals(file_name) for file_name in file_name_list]
pw_vals, tsurf_vals = list(zip(*pkl_vals))
pw_vals, tsurf_vals = np.array(pw_vals), np.array(tsurf_vals)

control_i = np.where(ppm_list==270)[0][0]
control_pw = pw_vals[control_i]
control_tsurf = tsurf_vals[control_i]

t_anom = tsurf_vals - control_tsurf
pw_pct = ((pw_vals / control_pw) * 100) - 100

outlier_index = -2
outlier_t_anom, outlier_pw_pct = t_anom[outlier_index:], pw_pct[outlier_index:]
t_anom, pw_pct = t_anom[:outlier_index], pw_pct[:outlier_index]

pw_slope, pw_int = np.polyfit(t_anom, pw_pct, 1)
pw_fit = (t_anom * pw_slope) + pw_int

plt.plot(t_anom, pw_pct, 'o')
plt.plot(t_anom, pw_fit, label = '{0} %/K'.format(pw_slope))
plt.plot(outlier_t_anom, outlier_pw_pct, 'x', c='k')
plt.xlabel('Tsurf Anomaly (K)')
plt.ylabel('PW Anomaly (%)')
print('{0} %/K'.format(pw_slope))
plt.legend()
plt.savefig('/home/haynes13/code/python/climproj/figures/Clausius_Clapeyron_check/check.png')
