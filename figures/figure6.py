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
def RMSE(series1, series2):
    return np.sqrt((np.sum(1/(len(series1))*np.power(np.subtract(series1, series2),2))))
method="timeseries"
file="Noramp_2_cv_high_ru_alpha_disp"
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
ramp_data_class=single_electron(CMAES_path+"/"+file)
counter=1
ramped_file="Ramped_3_cv_high_ru.ts"
ramp_data_class=single_electron(CMAES_path+"/"+ramped_file, {}, {}, {}, {}, False)
print(ramp_data_class.simulation_options["dispersion_bins"])
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
ramp_data_class.simulation_options["dispersion_bins"]=[16, 16]
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
values=[[0.24055747088306997, 0.05047523191357855, 176.56116945811587, 474.43867201525205, 7.584083348640005e-05, 0.0021028609527935505, -0.0004094927674505519, 7.146018738751102e-11, 8.88475177102702,0,0.6246797783009037, 0.1779493870477656],
        [0.22925918516708654, 0.04595696579195954, 123.33007397100599, 873.5412252656006, 3.3412012933121965e-05, 0.057928207116134806, -0.0021217096115628917, 7.178042062464878e-11, 8.884751771027027, 0,0.43751189633466997,  0.15509617967563671]]
ramp_data_class.dim_dict["alpha_mean"]=None
ramp_data_class.dim_dict["alpha_std"]=None
ramp_data_class.param_bounds["alpha_mean"]=[0.4, 0.6]
ramp_data_class.param_bounds["alpha_std"]=[0.01, 0.1]
master_optim_list=["E0_mean","E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","phase", "alpha_mean", "alpha_std"]
ramp_data_class.def_optim_list(master_optim_list)
axes=multiplot(1, 2, **{"harmonic_position":0, "num_harmonics":5, "orientation":"landscape", "plot_width":5})
ramp_data_class.harmonic_range=harmonic_range
j=0

labels=["Sinusoidal parameters", "Ramped parameters", "Interpolated+shifted"]
for i in range(0, 2):
    errors=[]
    ramped_time_series=ramp_data_class.i_nondim(ramp_data_class.test_vals(values[i], "timeseries"))
    alpha_val=round(ramp_data_class.dim_dict["alpha"],3)
    ramped_times=ramp_data_class.t_nondim(ramp_data_class.time_vec[ramp_data_class.time_idx])
    ramped_harmonics=ramp_data_harm_class.generate_harmonics(ramped_times, ramped_time_series)
    for harm_counter in range(0, len(ramped_harmonics),1):
        syn_harms=ramped_harmonics[harm_counter,:]*1e6
        data_harms=ramped_data_harmonics[harm_counter,:]*1e6
        interped_data=np.interp(ramped_times, ramped_time_results, data_harms)
        ax=axes.axes_dict["row1"][j]
        errors.append(RMSE(abs(syn_harms), abs(interped_data)))
        ax.plot(ramped_times, (syn_harms), label="Sim")
        ax.plot(ramped_time_results, (data_harms), label="Exp", alpha=0.6)
        ax2=ax.twinx()
        ax2.set_ylabel(harmonic_range[harm_counter], rotation=0)
        ax2.set_yticks([])
        if harm_counter%3==2:
            ax.set_ylabel("Current($\mu$A)")
        if harm_counter==(len(ramped_harmonics)-1):
            ax.set_xlabel("Time(s)")
            if i==0:
                ax.legend(bbox_to_anchor=[1.3, -1], loc="lower right")
        else:
            ax.set_xticks([])
        j+=1
    print(errors)
    print("Error", np.mean(errors))
fig=plt.gcf()
fig.set_size_inches((7, 4.5))
plt.show()
save_path="Ramped_comparison.png"
fig.savefig(save_path, dpi=500)
