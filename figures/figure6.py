import matplotlib.pyplot as plt
import numpy as np
import pints
import pints.plot
import os
import scipy.stats as stats
from matplotlib.ticker import FormatStrFormatter
import sys
current_dir=os.getcwd()
dir_list=current_dir.split("/")
upper_level_list=dir_list[:dir_list.index("SV_paper")+1]
upper_level=("/").join(upper_level_list)
class_loc=upper_level+"/src"
dir_path = os.path.dirname(os.path.realpath(__file__))
unit_dict={
    "E_0": "V",
    'E_start': "V",
    'E_reverse': "V",
    'omega':"Hz",
    'd_E': "V",
    'v': '$s^{-1}$',
    'area': '$cm^{2}$',
    'Ru': "$\\Omega$",
    'Cdl': "F",
    'CdlE1': "",
    'CdlE2': "",
    'CdlE3': "",
    'gamma': 'mol cm^{-2}$',
    'k_0': 's^{-1}$',
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
    'E_start': '$E_{start}$',
    'E_reverse': '$E_{reverse}$',
    'omega':'$\\omega$',
    'd_E': "$\\Delta E$",
    'v': "v",
    'area': "Area",
    'Ru': "R$_{u}$",
    'Cdl': "$C_{dl}$",
    'CdlE1': "$C_{dlE1}$",
    'CdlE2': "$C_{dlE2}$",
    'CdlE3': "$C_{dlE3}$",
    'gamma': '$\\Gamma',
    'k_0': '$k_0',
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
Titles={
    'omega':'Input frequency',
    'd_E': "Amplitude",
    'v': "Scan rate",
    'area': "Area",
    'Ru': "Uncompensated resistance",
    'Cdl': "Linear capacitance",
    'CdlE1': "First order capacitance",
    'CdlE2': "Second order capacitance",
    'CdlE3': "Third order capacitance",
    'gamma': 'Surface coverage',
    'k_0': 'Rate constant',
    'alpha': "Symmetry factor",
    "E0_mean":"Themodynamic mean",
    "E0_std": "Thermodynamic standard deviation",
    "E_0":"Midpoint potential",
    "cap_phase":"Capacitance phase",
    "alpha_mean": "Symmetry factor mean",
    "alpha_std": "Symmetry factor standard deviation",
    'phase' : "Phase",
    "":"Experiment",
    "noise":"Noise",
}
def chain_appender(chains, param):
    print(len(chains))
    if len(chains)>20:
        return chains[:, param]
    new_chain=chains[0, :, param]
    for i in range(1, len(chains)):
        new_chain=np.append(new_chain, chains[i, :, param])
    return new_chain
all_params=['E0_mean', "E0_std",'k_0',"Ru","Cdl", "CdlE1", "CdlE2",'gamma',"omega", "cap_phase","phase", "alpha_std", "noise"]
optim_list=['E0_mean', "E0_std",'k_0',"Ru", "phase", "cap_phase","alpha_std"]
positions=[all_params.index(x) for x in optim_list]
titles=[fancy_names[x]+"("+unit_dict[x]+")" if (unit_dict[x]!="") else fancy_names[x] for x in optim_list]
n_param=len(titles)
path=("/").join([upper_level,"Inferred_results", "MCMC", "Experimental"])
files=os.listdir(path)
def plot_kde_1d(x, ax, num=None):
    xmin = np.min(x)
    xmax = np.max(x)
    ax.set_xlim(xmin, xmax)
    x1 = np.linspace(xmin, xmax, 100)
    x2 = np.linspace(xmin, xmax, 50)
    ax.hist(x, bins=x2, label=num)
plt.rcParams.update({'font.size': 16})
def plot_kde_2d(x, y, ax):
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.scatter(x, y, s=0.5, alpha=0.5)
    ax.locator_params(nbins=2)
run="run24"
num=["_"+str(x)+"_" for x in range(1, 11)]
for number in num:
    for file in files:
        if number in file and run in file:
            fig_size=(12,12)
            fig, ax=plt.subplots(n_param, n_param)
            chain_result=np.load(path+"/"+file)
            for q in range(0, len(chain_result)):#len(chain_result)
                chain_len=len(chain_result[q, :, 0])
                chains=chain_result[q, 50000:, :]
                for i in range(0,n_param):
                    for j in range(0, n_param):
                        if i==j:
                            axes=ax[i,j]
                            ax1=axes.twinx()
                            plot_kde_1d(chains[:,positions[j]], ax=axes, num=("Chain "+str(q+1)))
                            if i==0:
                                axes.legend(loc="center left", bbox_to_anchor=(1.75, 0.5))
                            ticks=axes.get_yticks()
                            #labels=axes.get_yticklabes([])
                            axes.set_yticks([])
                            ax1.set_yticks(ticks)
                            if q==0:
                                ax1.set_ylabel("frequency")
                        elif i<j:
                            ax[i,j].axis('off')
                        else:
                            axes=ax[i,j]
                            plot_kde_2d(chains[:,positions[j]],chains[:,positions[i]], ax=axes)
                        if i!=0:
                            ax[i, 0].set_ylabel(titles[i])
                        if i<n_param-1:
                            ax[i,j].set_xticklabels([])#
                        if j>0 and i!=j:
                            ax[i,j].set_yticklabels([])
                        if j!=n_param:
                            ax[-1, i].set_xlabel(titles[i])
                            plt.setp( ax[-1, i].xaxis.get_majorticklabels(), rotation=15 )

            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.91, top=0.98, wspace=0.2, hspace=0.12)
            fig = plt.gcf()
            fig.set_size_inches((14,9))
            plt.show()
