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
from single_e_class_unified import single_electron
from harmonics_plotter import harmonics
from single_e_class_unified  import single_electron
import pints.plot
import math
from multiplotter import multiplot
from harmonics_plotter import harmonics
import time
method="timeseries"
file="Noramp_2_cv_high_ru_alpha_disp"
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
ramp_data_class=single_electron(CMAES_path+"/"+file)
counter=1
ramped_file="Ramped_3_cv_high_ru.ts"
ramp_data_class=single_electron(CMAES_path+"/"+ramped_file, {}, {}, {}, {}, False)
ramped_optim_list=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha_mean", "alpha_std"]
ramp_data_class.dim_dict["alpha_mean"]=0.5
ramp_data_class.dim_dict["alpha_std"]=1e-3
ramp_data_class.param_bounds["alpha_mean"]=[0.4, 0.6]
ramp_data_class.param_bounds["alpha_std"]=[1e-4, 1e-2]
ramp_data_class.def_optim_list(ramped_optim_list)
ramp_data_class.dim_dict["CdlE3"]=0
ramp_data_class.dim_dict["phase"]=0
ramp_data_class.dim_dict["cap_phase"]=0
ramp_data_class.simulation_options["GH_quadrature"]=True
ramp_data_class.simulation_options["dispersion_bins"]=[32, 10]
ramped_data_path=("/").join([upper_level, "experimental_data", "Ramped"])
start_harm=2
end_harm=7
ramp_data_harm_class=harmonics(list(range(start_harm, end_harm)), ramp_data_class.dim_dict["omega"], 0.05)
harmonic_range=list(range(start_harm, end_harm))
ramp_data_class.harmonic_range=harmonic_range
method="timeseries"
i="1"
ramped_current_results=np.loadtxt(ramped_data_path+"/Yellow_Electrode_Ramped_"+str(i)+"_cv_current")
ramped_voltage_results=np.loadtxt(ramped_data_path+"/Yellow_Electrode_Ramped_"+str(i)+"_cv_voltage")[:,1]
ramped_time_results=ramped_current_results[:,0]
ramped_current_results=ramped_current_results[:,1]
ramped_data_harmonics=ramp_data_harm_class.generate_harmonics(ramped_time_results, ramped_current_results)


CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
noramp_results=single_electron(CMAES_path+"/"+file)
noramp_results.simulation_options["dispersion_bins"]=[32,10]
noramp_results.def_optim_list(["E_0","k0_shape", "k0_scale","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","phase", "cap_phase","alpha_mean", "alpha_std"])
current_results_noramp=noramp_results.i_nondim(noramp_results.other_values["experiment_current"])
voltage_results_noramp=noramp_results.e_nondim(noramp_results.other_values["experiment_voltage"])
harms=harmonics(list(range(start_harm, end_harm)),noramp_results.dim_dict["omega"] , 0.05)
values=[[0.24076655487877807, 0.9160545932435216, 54.57673630269225, 544.0405150098435, 7.588258963750423e-05, 0.0024096777244230483, -0.00042186418363351214, 7.061673890583758e-11, 8.940521614985501, 5.087607311638155, 4.359094730658887, 0.54708141682858, 0.07163914467232897],
        [0.24076655487877807, 0.9160545932435216, 54.57673630269225, 544.0405150098435, 7.588258963750423e-05, 0.0024096777244230483, -0.00042186418363351214, 7.061673890583758e-11, 8.884751771027027, 0, 0.54708141682858, 0.07163914467232897]]

ramp_data_class.dim_dict["alpha_mean"]=None
ramp_data_class.dim_dict["alpha_std"]=None
ramp_data_class.param_bounds["alpha_mean"]=[0.4, 0.6]
ramp_data_class.param_bounds["alpha_std"]=[0.01, 0.1]
master_optim_list=["E_0","k0_shape", "k0_scale","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","phase", "alpha_mean", "alpha_std"]
ramp_data_class.def_optim_list(master_optim_list)
axes=multiplot(1, 2, **{"harmonic_position":0, "num_harmonics":5, "orientation":"landscape", "plot_width":5})
ramp_data_class.harmonic_range=harmonic_range
j=0

ramped_time_series=ramp_data_class.i_nondim(ramp_data_class.test_vals(values[1], "timeseries"))
ramped_times=ramp_data_class.t_nondim(ramp_data_class.time_vec[ramp_data_class.time_idx])
ramped_harmonics=ramp_data_harm_class.generate_harmonics(ramped_times, ramped_time_series)

noramp_time_series=noramp_results.i_nondim(noramp_results.test_vals(values[0], "timeseries"))
noramp_times=noramp_results.t_nondim(noramp_results.time_vec[ramp_data_class.time_idx])
noramp_harmonics=harms.generate_harmonics(noramp_times, noramp_time_series)
noramp_data=harms.generate_harmonics(noramp_times, current_results_noramp)
xs=[voltage_results_noramp,ramped_times]
ys=[noramp_harmonics, ramped_harmonics]
data_xs=[voltage_results_noramp, ramped_time_results]
datas=[noramp_data, ramped_data_harmonics]
xlabels=["Voltage(V vs. Ref)", "Time(s)"]
for i in range(0, 2):
    for harm_counter in range(0, len(ramped_harmonics),1):
        ax=axes.axes_dict["row1"][j]
        ax.plot(xs[i], (ys[i][harm_counter,:]*1e6), label="Sim")
        ax.plot(data_xs[i], (datas[i][harm_counter,:]*1e6), label="Exp", alpha=0.6)
        ax2=ax.twinx()
        ax2.set_ylabel(harmonic_range[harm_counter], rotation=0)
        ax2.set_yticks([])
        if harm_counter%3==2:
            ax.set_ylabel("Current($\mu$A)")
        if harm_counter==(len(ramped_harmonics)-1):
            ax.set_xlabel(xlabels[i])
            if i==0:
                ax.legend(bbox_to_anchor=[1.3, -1], loc="lower right")
        else:
            ax.set_xticks([])
        j+=1
fig=plt.gcf()
plt.subplots_adjust(top=0.94,
                    bottom=0.135,
                    left=0.105,
                    right=0.965,
                    hspace=0.2,
                    wspace=0.2)
fig.set_size_inches((7, 4.5))
plt.show()
save_path="Ramped_comparison.png"
fig.savefig(save_path, dpi=500)
