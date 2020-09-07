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
run="Run_7"
concs=["1e-1M", "1e0M"]
file_numbers=[str(x) for x in range(1, 4)]

plot_counter=0
h_counter=0
f_counter=0
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
plt.rcParams.update({'font.size': 9})
def RMSE(series1, series2):
    return np.sqrt((np.sum(1/(len(series1))*np.power(np.subtract(series1, series2),2))))


for i in range(1,11):
    file="Noramp_"+str(i)+"_cv_high_ru_alpha_disp"
    method="timeseries"
    master_optim_list=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha"]
    noramp_results=single_electron(CMAES_path+"/"+file)
    master_optim_list=["E0_mean", "E0_std", "k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha_mean", "alpha_std"]
    param_vals=([noramp_results.save_dict["params"][2][noramp_results.save_dict["optim_list"].index(key)] if  (key in noramp_results.save_dict["optim_list"]) else noramp_results.dim_dict[key] for key in master_optim_list])
    noramp_results.simulation_options["dispersion_bins"]=[5,5]
    #print(noramp_results.dim_dict["sampling_freq"])
    noramp_results.dim_dict["sampling_freq"]=1/200.0
    noramp_results.def_optim_list(master_optim_list)
    cmaes_time=noramp_results.i_nondim(noramp_results.test_vals(param_vals, method))
    current_results=noramp_results.i_nondim(noramp_results.other_values["experiment_current"])#[0::dec_amount]
    voltage_results=noramp_results.e_nondim(noramp_results.other_values["experiment_voltage"])#[0::dec_amount]
    #print_vals=np.append(param_vals, RMSE(current_results, cmaes_time)*1e6)

    #print(list(print_vals), ",")

    harms=harmonics(range(1, 8),noramp_results.dim_dict["omega"] , 0.05)
    time_results=noramp_results.t_nondim(noramp_results.other_values["experiment_time"])#[0::dec_amount]
    plt.plot(voltage_results*1e3, (cmaes_time)*1e3, label="Simulation")
    plt.plot(voltage_results*1e3,(current_results)*1e3, alpha=0.5, label="Experiment")
    plt.xlabel("Potential(mV vs. Ref.)")
    plt.ylabel("Current(mA)")
    plt.legend()
    fig=plt.gcf()

    fig.set_size_inches((3.25, 1.75))
    plt.show()
    #save_path="toc_graphic.png"
    #fig.savefig(save_path, dpi=500)
