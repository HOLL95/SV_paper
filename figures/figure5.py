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
figure=multiplot(3, 1, **{"harmonic_position":2, "num_harmonics":7, "orientation":"landscape", "fourier_position":1, "plot_width":5, "row_spacing":2, "plot_height":1})
keys=sorted(figure.axes_dict.keys())
plot_counter=0
h_counter=0
f_counter=0
CMAES_path=("/").join([upper_level, "Inferred_results", "CMAES"])
plt.rcParams.update({'font.size': 9})
def RMSE(series1, series2):
    return np.sqrt((np.sum(1/(len(series1))*np.power(np.subtract(series1, series2),2))))
param_mat=[[0.24696678941258246, 0.02150713711591799, 99.45832461312207, 774.704213209354, 7.701956070978554e-05, 0.003017010623506844, -0.00039055262925760496, 7.758858523468079e-11, 8.940640920538685, 4.410033377066397,5.1069657955459,  0.5825105457091572, 0.14328732063771737] ,
        [0.2438679560342186, 0.04933431717529572, 191.31132541897506, 497.5055066560729, 7.69338292657605e-05, 0.0031326600706418906, -0.0004312564011993529, 7.271953365051911e-11, 8.94052385943315, 4.3351579045955795,4.925339460865147,  0.6496639586748201, 0.17177231234727677] ,
        [0.24430949230426569, 0.04731795471469772, 176.34896534285173, 521.4259532758771, 7.647752507363084e-05, 0.002994039070869009, -0.0004190299720139099, 7.275919967176139e-11, 8.940534898414818, 4.342816983799178, 4.943663135736721, 0.6362752123549957, 0.1720460446880876] ,
        [0.24390113149368509, 0.0457048751819453, 161.20949406256256, 536.934970450984, 7.621126298448553e-05, 0.0028379095150146416, -0.000413526916786134, 7.281036191448345e-11, 8.940539372196708, 4.34670259354896, 4.957545393990694, 0.6227137060882207, 0.1713086829766499] ,
        [0.24264240746946078, 0.04862334843813994, 174.5319444179432, 501.7381191076415, 7.621609295572e-05, 0.0025967801809421154, -0.00041475793632247265, 7.236585251042315e-11, 8.94052009496047, 4.336548651366052, 4.934251569752124, 0.6291348730960813, 0.17453584870953875] ,
        [0.24160781666577544, 0.05036058151555205, 183.91624120363147, 478.0527573517239, 7.62482655530355e-05, 0.002429757046640779, -0.00041668758601426555, 7.209545158956022e-11, 8.940507420558243, 4.330200828730097, 4.9203855923331705, 0.633836591099598, 0.17606178914368914] ,
        [0.24122209427368013, 0.049981782635136945, 179.81828332106306, 480.1074385658014, 7.615225208615455e-05, 0.002305928382454525, -0.00041429576393527123, 7.19385317237139e-11, 8.940492881836837, 4.331293568942899, 4.923830104418481, 0.6292049920997411, 0.17637075996545973] ,
        [0.24100346908927325, 0.05022099349663932, 178.28549652948317, 477.9310528442049, 7.59455358542439e-05, 0.002273221478669929, -0.00041353404857902287, 7.160330874703819e-11, 8.940504038013483, 4.329624942864246, 4.92163560153165, 0.6277651371395521, 0.17665475180369178] ,
        [0.2412440781552388, 0.050226126358631266, 180.12768848217763, 485.192042495465, 7.548546629894573e-05, 0.0021505398969171585, -0.00040389051055751864, 7.11413102722647e-11, 8.940519733026564,  4.3302796214687795,4.9224469580118715, 0.6290049217531675, 0.17737634083075238],
        [0.24055747088306997, 0.05047523191357855, 176.56116945811587, 474.43867201525205, 7.584083348640005e-05, 0.0021028609527935505, -0.0004094927674505519, 7.146018738751102e-11, 8.940505868813535,  4.327745982059323, 4.920060562270928,0.6246797783009037, 0.1779493870477656],
        ]

for i in range(10,11):
    file="Noramp_"+str(i)+"_cv_high_ru_alpha_disp"
    method="timeseries"
    master_optim_list=["E0_mean", "E0_std","k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha"]
    noramp_results=single_electron(CMAES_path+"/"+file)
    master_optim_list=["E0_mean", "E0_std", "k_0","Ru","Cdl","CdlE1", "CdlE2","gamma","omega","cap_phase","phase", "alpha_mean", "alpha_std"]
    param_vals=([noramp_results.save_dict["params"][0][noramp_results.save_dict["optim_list"].index(key)] if  (key in noramp_results.save_dict["optim_list"]) else noramp_results.dim_dict[key] for key in master_optim_list])
    param_vals=param_mat[i-1]
    noramp_results.simulation_options["dispersion_bins"]=[5,8]
    noramp_results.dim_dict["simulation_freq"]=1/2000.0
    noramp_results.def_optim_list(master_optim_list)
    cmaes_time=noramp_results.i_nondim(noramp_results.test_vals(param_vals, method))
    current_results=noramp_results.i_nondim(noramp_results.other_values["experiment_current"])#[0::dec_amount]
    voltage_results=noramp_results.e_nondim(noramp_results.other_values["experiment_voltage"])#[0::dec_amount]
    print_vals=np.append(param_vals, RMSE(current_results, cmaes_time)*1e6)
    print(list(print_vals), ",")
    harms=harmonics(range(1, 8),noramp_results.dim_dict["omega"] , 0.05)
    time_results=noramp_results.t_nondim(noramp_results.other_values["experiment_time"])#[0::dec_amount]
    figure.axes_dict[keys[0]][plot_counter].plot(voltage_results*1e3, (cmaes_time)*1e3, label="Sim")
    figure.axes_dict[keys[0]][plot_counter].plot(voltage_results*1e3,(current_results)*1e3, alpha=0.5, label="Exp")
    figure.axes_dict[keys[0]][plot_counter].set_xlabel("Potential(mV vs. Ref.)")
    figure.axes_dict[keys[0]][plot_counter].set_ylabel("Current(mA)")
    figure.axes_dict[keys[0]][plot_counter].plot(voltage_results*1e3, np.subtract(cmaes_time*1e3, current_results*1e3), label="Residual")
    figure.axes_dict[keys[0]][plot_counter].legend()
    plot_counter+=1
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter], cmaes_time, time_results,  box=False, arg=np.real, line_label="Sim")
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter],current_results, time_results,  box=False, arg=np.real, line_label="Exp", alpha=0.5)
    figure.axes_dict[keys[1]][f_counter].set_xlabel("Frequency(Hz)")
    figure.axes_dict[keys[1]][f_counter].set_ylabel("Real")
    figure.axes_dict[keys[1]][f_counter].legend(bbox_to_anchor=(-0.32, 0.25), loc="upper left")
    f_counter+=1
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter], cmaes_time, time_results, box=False, arg=np.imag,line_label="Sim")
    harms.harmonic_selecter(figure.axes_dict[keys[1]][f_counter],  current_results,  time_results,box=False, arg=np.imag, line_label="Exp", alpha=0.5)
    figure.axes_dict[keys[1]][f_counter].set_xlabel("Frequency(Hz)")
    figure.axes_dict[keys[1]][f_counter].set_ylabel("Imag.")

    f_counter+=1
    data_harms=harms.generate_harmonics(time_results, cmaes_time)
    print(len(data_harms))
    exp_harms=harms.generate_harmonics(time_results, current_results)
    for q in range(0, len(data_harms)):
        print(q)
        figure.axes_dict[keys[2]][h_counter].plot(voltage_results*1e3, data_harms[q]*1e6, label="Sim")
        figure.axes_dict[keys[2]][h_counter].plot(voltage_results*1e3, exp_harms[q]*1e6, alpha=0.5, label="Exp")
        lb, ub = figure.axes_dict[keys[2]][h_counter].get_ylim( )
        figure.axes_dict[keys[2]][h_counter].set_yticks([round(x,1) for x in np.linspace(0.5*lb, 0.5*ub, 2)])
        ax2=figure.axes_dict[keys[2]][h_counter].twinx()
        ax2.set_ylabel(harms.harmonics[q], rotation=0)
        ax2.set_yticks([])
        if q==len(data_harms)//2:
            figure.axes_dict[keys[2]][h_counter].set_ylabel("Current($\mu$A)")
        if q==len(data_harms)-1:
            figure.axes_dict[keys[2]][h_counter].set_xlabel("Potential(mV vs. Ref.)")
            figure.axes_dict[keys[2]][h_counter].legend(framealpha=1.0,bbox_to_anchor=(-0.3, 0.0), loc="upper left")
        else:
            figure.axes_dict[keys[2]][h_counter].set_xticks([])
        h_counter+=1
fig=plt.gcf()
plt.subplots_adjust(left=0.23, bottom=0.08, right=0.97, top=0.99, wspace=0.2, hspace=0.02)
fig.set_size_inches((3.25, 7.5))
plt.show()
save_path="Alice_"+str(i)+"_sims.png"
fig.savefig(save_path, dpi=500)

plt.show()
