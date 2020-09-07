import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pints
import os
import sys
try:
    from PIL import Image
    resize=True
except:
    resize=False
current_dir=os.getcwd()
dir_list=current_dir.split("/")
upper_level_list=dir_list[:dir_list.index("SV_paper")+1]
upper_level=("/").join(upper_level_list)
class_loc=upper_level+"/src"
sys.path.insert(0, class_loc)
from single_e_class_unified  import single_electron
import pints.plot
from decimal import Decimal
import math
from multiplotter import multiplot
from harmonics_plotter import harmonics
results_dict="Inferred_params"
master_optim_list=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase","alpha_mean", "alpha_std"]
num_harms=5
font = {'family' : 'normal',
        'size'   : 9}

plt.rc('font', **font)
unit_dict={
    "E_0": "V",
    'E_start': "V", #(starting dc voltage - V)
    'E_reverse': "V",
    'omega':"Hz",#8.88480830076,  #    (frequency Hz)
    'd_E': "V",   #(ac voltage amplitude - V) freq_range[j],#
    'v': '$s^{-1}$',   #       (scan rate s^-1)
    'area': '$cm^{2}$', #(electrode surface area cm^2)
    'Ru': "$\\Omega$",  #     (uncompensated resistance ohms)
    'Cdl': "F", #(capacitance parameters)
    'CdlE1': "",#0.000653657774506,
    'CdlE2': "",#0.000245772700637,
    'CdlE3': "",#1.10053945995e-06,
    'gamma': 'mol cm^{-2}$',
    'k_0': "$s^{-1}$",#'$s^{-1}$', #(reaction rate s-1)
    'alpha': "",
    "E0_mean":"V",
    "E0_std": "V",
    "k0_shape":"",
    "k0_loc":"",
    "k0_scale":"",
    "cap_phase":"",
    'phase' : "",
    "alpha_mean": "",
    "alpha_std": "",
    "":"",
    "noise":"",
}
fancy_names={
    "E_0": '$E^0$',
    'E_start': '$E_{start}$', #(starting dc voltage - V)
    'E_reverse': '$E_{reverse}$',
    'omega':'$\\omega$',#8.88480830076,  #    (frequency Hz)
    'd_E': "$\\Delta E$",   #(ac voltage amplitude - V) freq_range[j],#
    'v': "v",   #       (scan rate s^-1)
    'area': "Area", #(electrode surface area cm^2)
    'Ru': "R$_{u}$",  #     (uncompensated resistance ohms)
    'Cdl': "$C_{dl}$", #(capacitance parameters)
    'CdlE1': "$C_{dlE1}$",#0.000653657774506,
    'CdlE2': "$C_{dlE2}$",#0.000245772700637,
    'CdlE3': "$C_{dlE3}$",#1.10053945995e-06,
    'gamma': '$\\Gamma',
    'k_0': '$k_0$', #(reaction rate s-1)
    'alpha': "$\\alpha$",
    "E0_mean":"$E^0 \\mu$",
    "E0_std": "$E^0 \\sigma$",
    "cap_phase":"$C_{dl}$ phase",
    "alpha_mean": "$\\alpha\\mu$",
    "alpha_std": "$\\alpha\\sigma$",
    'phase' : "Phase",
    "":"Experiment",
    "noise":"$\sigma$",
}
param_bounds={
    'E_0':[0.3, 0.6],#[param_list['E_start'],param_list['E_reverse']],
    'Ru': [0,1000],  #     (uncompensated resistance ohms)
    'Cdl': [0,1e-4], #(capacitance parameters)
    'CdlE1': [-0.15,0.15],#0.000653657774506,
    'CdlE2': [-0.01,0.01],#0.000245772700637,
    'CdlE3': [-0.01,0.01],#1.10053945995e-06,
    'gamma': [8e-11,1e-9],
    'k_0': [10, 150], #(reaction rate s-1)
    'alpha': [0.4, 0.6],
    "cap_phase":[5*math.pi/4, 2*math.pi],
    "E0_mean":[0.1, 0.4],
    "E0_std": [0.01, 0.1],
    "alpha_mean":[0.4, 0.6],
    "alpha_std":[0.001, 0.2],
    'phase' : [5*math.pi/4, 7*math.pi/4]
}
method="timeseries"
file="Noramp_2_cv_high_ru_alpha_disp"
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
noramp_results=single_electron(CMAES_path+"/"+file)
print(noramp_results.dim_dict["num_peaks"])
noramp_results.simulation_options["dispersion_bins"]=[15,15]
noramp_results.dim_dict["sampling_freq"]=1/2000.0
noramp_results.dim_dict["phase"]=3*math.pi/2
plot_params=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "cap_phase", "alpha_mean", "alpha_std"]
param_vals=[0.25, 0.05, 0.1, 100,1e-5, 1e-5,3*math.pi/2, 0.5, 0.05]
noramp_results.dim_dict["Cdl"]=1e-5
noramp_results.dim_dict["CdlE1"]=0
noramp_results.dim_dict["CdlE2"]=0
noramp_results.def_optim_list(plot_params)
cmaes_time=noramp_results.i_nondim(noramp_results.test_vals(param_vals, method))
current_results=noramp_results.i_nondim(noramp_results.other_values["experiment_current"])
voltage_results=noramp_results.e_nondim(noramp_results.other_values["experiment_voltage"])
time_results=noramp_results.t_nondim(noramp_results.other_values["experiment_time"])
start_harm=3
harms=harmonics(range(start_harm, start_harm+num_harms),noramp_results.dim_dict["omega"] , 0.05)
num_scans=4
plt.rcParams.update({'font.size': 15})
#mpl.rcParams['axes.labelsize'] = 1
col_len=3
row_len=len(plot_params)//col_len

fig, axes=plt.subplots(row_len, col_len)
value_list=[[0.1, 0.2, 0.3, 0.4],
        [0.01, 0.04, 0.07, 0.1],
        [10, 50, 100, 150],
        [0, 300, 600, 900],
        [0, 3e-5,6e-5, 9e-5],
        [-0.15, -0.05, 0.05, 0.15],
        [4, 4.75, 5.5, 6.25],
        [0.4, 0.45, 0.55, 0.6],
        [0.01, 0.07, 0.13, 0.2]]
for j in range(0,len(plot_params)):#
    col_idx=j%row_len
    row_idx=j//row_len
    new_params=np.copy(param_vals)
    values=value_list[j]
    for q in range(0, num_scans):
        new_params[j]=values[q]
        cmaes_time=noramp_results.i_nondim(noramp_results.test_vals(new_params, method))

        ax=axes[row_idx, col_idx]
        xlims=ax.get_xlim()
        ax.set_xlim(noramp_results.dim_dict["E_start"], 0.8)
        if row_idx==row_len-1:
            ax.set_xlabel("Potential(V)")
        else:
            ax.set_xticks([])
        if col_idx==0:
            ax.set_ylabel("Current(mA)")
        value_label=str(values[q])
        ax.plot(voltage_results, cmaes_time*1e3, label=value_label+unit_dict[plot_params[j]])
        ax.text(0.85, 0.9,fancy_names[plot_params[j]],
        horizontalalignment='center',
        verticalalignment='center',
        transform = ax.transAxes,
        fontsize=16)
        ax.legend(loc="center right", handlelength=0.3,bbox_to_anchor=(1.02, 0.5))


fig=plt.gcf()
fig.set_size_inches((14, 9))
plt.subplots_adjust(left=0.08, bottom=0.1, right=0.98, top=0.94, wspace=0.25, hspace=0.10)
plt.show()
save_path="parameter_scans.png"
fig.savefig(save_path, dpi=500)
if resize==True:
    img = Image.open(save_path)
    basewidth = float(img.size[0])//2
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((int(basewidth),hsize), Image.ANTIALIAS)
    img.save(save_path, "PNG", quality=95, dpi=(500, 500))
