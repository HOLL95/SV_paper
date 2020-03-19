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
from single_e_class_unified  import single_electron
import pints.plot
import math
from multiplotter import multiplot
from harmonics_plotter import harmonics
dir_path = os.path.dirname(os.path.realpath(__file__))
results_dict="Inferred_params"
Electrode="Yellow"
run="Run_6"
concs=["1e-1M", "1e0M"]
file_numbers=[str(x) for x in range(1, 4)]
figure=multiplot(3, 1, **{"harmonic_position":2, "num_harmonics":7, "orientation":"landscape", "fourier_position":1, "plot_width":5, "row_spacing":2, "plot_height":1})
keys=sorted(figure.axes_dict.keys())
plot_counter=0
h_counter=0
f_counter=0
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
plt.rcParams.update({'font.size': 9})
def RMSE(series1, series2):
    return np.sqrt((np.sum(1/(len(series1))*np.power(np.subtract(series1, series2),2))))
for i in range(10,11):
    file="Noramp_"+str(i)+"_cv_high_ru_alpha_disp"
    method="timeseries"
    master_optim_list=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha"]
    noramp_results=single_electron(CMAES_path+"/"+file)
    master_optim_list=["E0_mean", "E0_std", "k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha_mean", "alpha_std"]
    param_vals=([noramp_results.save_dict["params"][0][noramp_results.save_dict["optim_list"].index(key)] if  (key in noramp_results.save_dict["optim_list"]) else noramp_results.dim_dict[key] for key in master_optim_list])
    noramp_results.simulation_options["dispersion_bins"]=[5,5]
    noramp_results.def_optim_list(master_optim_list)
    cmaes_time=noramp_results.i_nondim(noramp_results.test_vals(param_vals, method))
    current_results=noramp_results.i_nondim(noramp_results.other_values["experiment_current"])#[0::dec_amount]
    voltage_results=noramp_results.e_nondim(noramp_results.other_values["experiment_voltage"])#[0::dec_amount]
    print_vals=np.append(param_vals, RMSE(current_results, cmaes_time)*1e6)
    print(list(print_vals), ",")
    harms=harmonics(range(1, 8),noramp_results.dim_dict["omega"] , 0.05)
    time_results=noramp_results.t_nondim(noramp_results.other_values["experiment_time"])#[0::dec_amount]
    figure.axes_dict[keys[0]][plot_counter].plot(voltage_results*1e3, (cmaes_time)*1e3, label="Sim")
    figure.axes_dict[keys[0]][plot_counter].plot(voltage_results*1e3,(current_results)*1e3, alpha=0.5, label="Data")
    figure.axes_dict[keys[0]][plot_counter].set_xlabel("Voltage(mV)")
    figure.axes_dict[keys[0]][plot_counter].set_ylabel("Current(mA)")
    figure.axes_dict[keys[0]][plot_counter].plot(voltage_results*1e3, np.subtract(cmaes_time*1e3, current_results*1e3), label="Residual")
    figure.axes_dict[keys[0]][plot_counter].legend()
    plot_counter+=1
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter], cmaes_time, time_results,  box=False, arg=np.real, line_label="Sim")
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter],current_results, time_results,  box=False, arg=np.real, line_label="Data", alpha=0.5)
    figure.axes_dict[keys[1]][f_counter].set_xlabel("Frequency(Hz)")
    figure.axes_dict[keys[1]][f_counter].set_ylabel("Real")
    f_counter+=1
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter], cmaes_time, time_results, box=False, arg=np.imag,line_label="Sim")
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter],  current_results,  time_results,box=False, arg=np.imag, line_label="Data", alpha=0.5)
    figure.axes_dict[keys[1]][f_counter].set_xlabel("Frequency(Hz)")
    figure.axes_dict[keys[1]][f_counter].set_ylabel("Imaginary")
    figure.axes_dict[keys[1]][f_counter].legend(bbox_to_anchor=(0.4, 0.6))
    f_counter+=1
    data_harms=harms.generate_harmonics(time_results, cmaes_time)
    print(len(data_harms))
    exp_harms=harms.generate_harmonics(time_results, current_results)
    for q in range(0, len(data_harms)):
        print(q)
        figure.axes_dict[keys[2]][h_counter].plot(voltage_results*1e3, data_harms[q]*1e6, label="Sim")
        figure.axes_dict[keys[2]][h_counter].plot(voltage_results*1e3, exp_harms[q]*1e6, alpha=0.5, label="Data")
        lb, ub = figure.axes_dict[keys[2]][h_counter].get_ylim( )
        figure.axes_dict[keys[2]][h_counter].set_yticks([round(x,1) for x in np.linspace(0.5*lb, 0.5*ub, 2)])
        ax2=figure.axes_dict[keys[2]][h_counter].twinx()
        ax2.set_ylabel(harms.harmonics[q], rotation=0)
        ax2.set_yticks([])
        if q==len(data_harms)//2:
            figure.axes_dict[keys[2]][h_counter].set_ylabel("Current($\mu$A)")
        if q==len(data_harms)-1:
            figure.axes_dict[keys[2]][h_counter].set_xlabel("Voltage(mV)")
            figure.axes_dict[keys[2]][h_counter].legend(framealpha=1.0,bbox_to_anchor=(0.1, 0.1))
        else:
            figure.axes_dict[keys[2]][h_counter].set_xticks([])
        h_counter+=1
fig=plt.gcf()
plt.subplots_adjust(left=0.23, bottom=0.06, right=0.97, top=0.99, wspace=0.2, hspace=0.02)
fig.set_size_inches((3.25, 7.5))
plt.show()
save_path="Alice_"+str(i)+"_sims.png"
fig.savefig(save_path, dpi=500)

plt.show()
