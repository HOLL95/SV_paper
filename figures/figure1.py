import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pints
import os
import sys
current_dir=os.getcwd()
dir_list=current_dir.split("/")
upper_level_list=dir_list[:dir_list.index("SV_paper")+1]
upper_level=("/").join(upper_level_list)
class_loc=upper_level+"/src"
sys.path.insert(0, class_loc)
try:
    from PIL import Image
    resize=True
except:
    resize=False
from single_e_class_unified import single_electron
from harmonics_plotter import harmonics
import pints.plot
import math
from multiplotter import multiplot
from harmonics_plotter import harmonics
import time
font = {'family' : 'normal',
        'size'   : 12}

plt.rc('font', **font)
letters=["A", "B", "C", "D", "E", "F", "G", "H"]
method="timeseries"
file="Noramp_2_cv_high_ru_alpha_disp"
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
noramp_results=single_electron(CMAES_path+"/"+file)
counter=1
ramped_file="Ramped_1_cv_high_ru.ts"
ramp_data_class=single_electron(CMAES_path+"/"+ramped_file, {}, {}, {}, {}, False)
master_optim_list=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha"]
param_vals=([noramp_results.save_dict["params"][0][noramp_results.save_dict["optim_list"].index(key)] if  (key in noramp_results.save_dict["optim_list"]) else noramp_results.dim_dict[key] for key in master_optim_list])
param_vals[master_optim_list.index("Cdl")]=1e-5
param_vals[master_optim_list.index("CdlE1")]=0
param_vals[master_optim_list.index("CdlE2")]=0
ramp_param_vals=np.delete(param_vals, master_optim_list.index("cap_phase"))
ramp_data_class.param_bounds=noramp_results.param_bounds
ramp_data_class.simulation_options["dispersion_bins"]=[5]
noramp_results.simulation_options["dispersion_bins"]=[5]
noramp_results.simulation_options["sampling_freq"]=1/200.0
ramp_data_class.simulation_options["GH_quadrature"]=True
noramp_results.def_optim_list(master_optim_list)
ramp_data_class.def_optim_list(["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","phase", "alpha"])

cmaes_time=noramp_results.i_nondim(noramp_results.test_vals(param_vals, method))*1e3
ramped_cmaes_time=ramp_data_class.i_nondim(ramp_data_class.test_vals(ramp_param_vals, method))*1e3
current_results=noramp_results.i_nondim(noramp_results.other_values["experiment_current"])#[0::dec_amount]
voltage_results=noramp_results.e_nondim(noramp_results.other_values["experiment_voltage"])#[0::dec_amount]
voltage_plots=noramp_results.e_nondim(noramp_results.define_voltages())
voltage_times=noramp_results.t_nondim(noramp_results.time_vec)
time_results=noramp_results.t_nondim(noramp_results.other_values["experiment_time"])#[0::dec_amount]
ramp_current_results=ramp_data_class.i_nondim(ramp_data_class.other_values["experiment_current"])#[0::dec_amount]
ramp_voltage_results=ramp_data_class.e_nondim(ramp_data_class.define_voltages())#[0::dec_amount]
ramp_time_results=ramp_data_class.t_nondim(ramp_data_class.time_vec)
num_harms=6
start_harm=1
end_harm=start_harm+num_harms
harms=harmonics(range(start_harm, end_harm),noramp_results.dim_dict["omega"] , 0.05)
noramp_harms=harms.generate_harmonics(time_results, cmaes_time)
ramp_harms=harms.generate_harmonics(ramp_time_results, ramped_cmaes_time)
all_harms=[ramp_harms, noramp_harms]
fourier_funcs=[np.real, np.imag]
fourier_ylabels=["Real", "Imaginary"]
fourier_times=[ramp_time_results, time_results]
fourier_currents=[ramped_cmaes_time, cmaes_time]
harm_xlabels=["Time(s)", "Potential(V)"]
fig=multiplot(2, 4, **{"harmonic_position":3, "num_harmonics":num_harms, "fourier_position":2,"orientation":"portrait", "plot_width":6, "col_spacing":2, "font_size":15})
keys=sorted(fig.axes_dict.keys())

fig.axes_dict["col1"][0].plot(ramp_time_results, ramp_voltage_results)
fig.axes_dict["col1"][0].set_xlabel("Time(s)")
fig.axes_dict["col1"][0].set_ylabel("Potential(V)")
fig.axes_dict["col1"][1].plot(voltage_times, voltage_plots)
fig.axes_dict["col1"][1].set_xlabel("Time(s)")
fig.axes_dict["col1"][1].set_ylabel("Potential(V)")
fig.axes_dict["col2"][0].plot(ramp_time_results, ramped_cmaes_time)
fig.axes_dict["col2"][0].set_xlabel("Time(s)")
fig.axes_dict["col2"][0].set_ylabel("Current(mA)")
fig.axes_dict["col2"][1].plot(voltage_results, cmaes_time)
fig.axes_dict["col2"][1].set_xlabel("Potential(V)")
fig.axes_dict["col2"][1].set_ylabel("Current(mA)")
for i in range(0, 2):
    for j in range(0, 2):
        pos=(i*2)+j
        if j==1:
            fig.axes_dict["col3"][pos].set_xlabel("Frequency(Hz)")
        fig.axes_dict["col3"][pos].set_ylabel(fourier_ylabels[j])
        if j==0:
            fig.axes_dict["col3"][pos].set_xticks([])
        harms.harmonic_selecter(fig.axes_dict["col3"][pos], fourier_currents[i],fourier_times[i], box=False, arg=fourier_funcs[j])
for i in range(0, 2):
    for j in range(0, num_harms):
        if i==0:
            x=ramp_time_results
            if j==3:
                fig.axes_dict["col4"][pos].set_ylabel("Current($\\mu A$)")
        else:
            x=voltage_results
            if j==4:
                fig.axes_dict["col4"][pos].set_ylabel("Current($\\mu A$)")
        pos=(i*num_harms)+j
        fig.axes_dict["col4"][pos].plot(x, all_harms[i][j,:]*1e3)

        twiny=fig.axes_dict["col4"][pos].twinx()
        twiny.set_ylabel(j+1, rotation=0)
        twiny.set_yticklabels([])
        if j==num_harms-1:
            fig.axes_dict["col4"][pos].set_xlabel(harm_xlabels[i])
        else:
            fig.axes_dict["col4"][pos].set_xticks([])
        ticks=fig.axes_dict["col4"][pos].get_yticks()
        fig.axes_dict["col4"][pos].set_yticks([ticks[1], ticks[-2]])

letter_count=0
y_pos=[1.1, 1.1, 1.195, 1.58]
for i in range(0, len(keys)):
    letter_idx=[0, len(fig.axes_dict[keys[i]])//2]

    for j in range(0, len(letter_idx)):
        pos=i+(j*(len(keys)))
        fig.axes_dict[keys[i]][letter_idx[j]].text(-0.1, y_pos[i], letters[pos], transform=fig.axes_dict[keys[i]][letter_idx[j]].transAxes,
          fontsize=14, fontweight='bold', va='top', ha='right')
        letter_count+=1

fig=plt.gcf()
fig.set_size_inches((14, 9))
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.94, wspace=0.29, hspace=0.2)
plt.show()
save_path="experiment_comparison.png"
fig.savefig(save_path, dpi=500)
if resize==True:
    img = Image.open(save_path)
    basewidth = float(img.size[0])//2
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((int(basewidth),hsize), Image.ANTIALIAS)
    img.save(save_path, "PNG", quality=95, dpi=(500, 500))
