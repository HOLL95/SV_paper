import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import math
import copy
from single_e_class_unified import single_electron
from harmonics_plotter import harmonics
"""
Parameters for both the experiment (such as the start and end potentials) are stored along with electrochemical parameters in the param_dict dictionary.
A number of parameters are required: E_0, k_0, alpha, gamma, Ru, Cdl, CdlE1,CdlE2,CdlE3, E_start,E_reverse, omega, phase, d_E, area, original_gamma
Not including the parameters in the dictionary will return an error
"""
param_list={
        "E_0":0.2, #Midpoint potnetial (V)
        'E_start': -0.1, #Sinusoidal input minimum (or starting) potential (V)
        'E_reverse': 0.5, #Sinusoidal input maximum potential (V)
        'omega':10,   #frequency Hz
        "original_omega":10, #Nondimensionalising value for frequency (Hz)
        'd_E': 300e-3,   #ac voltage amplitude - V
        'area': 0.07, #electrode surface area cm^2
        'Ru': 100.0,  #     uncompensated resistance ohms
        'Cdl': 1e-5, #capacitance parameters
        'CdlE1': 0,
        'CdlE2': 0,
        "CdlE3":0,
        'gamma': 1e-10,   # surface coverage per unit area
        "original_gamma":1e-10,        # Nondimensionalising cvalue for surface coverage
        'k_0': 100, #(reaction rate s-1)
        'alpha': 0.5, #(Symmetry factor)
        'phase' : 3*(math.pi/2),#Phase of the input potential
        "cap_phase":3*(math.pi/2),
        'sampling_freq' : (1.0/400),
    }
likelihood_options=["timeseries", "fourier"]
"""
Simulation options description
-----------------------------
No transient:
    If this is submitted as a numerical value, then the simulation will only return simulated current from after this time.
    If experimental data is submitted, then the initial current up to the set time will be removed. Will default to False
Experimental fitting:
    If this is True, then the code will look for data provided in the other_values dictionary.
    The code will then attempt to non-dimensionalise the provided data, and truncate it if necessary.
    The simulation code will use the experimental time (and associated sampling rate) for simulation if provided.
Method:
    The input potential to be used for the simulation code and voltage generation.
    Can be sinusoidal, ramped or DCV
Likelihood:
    Controls the format in which simulated current will be returned from the simulate() function.
    Can be "timeseries", or "fourier" for time domain or (filtered) frequency domain respectively
Label:
    Can be "MCMC" or "cmaes". CMAES means that the simulate() function will rescale values submitted between 0 and 1 to the appoprate value within the set param_bounds.
    MCMC will simulate current using the provided values.
Optim list:
    The parameters which the code will change to produce simualte current in the simulate() function
"""
simulation_options={
        "no_transient":False,
        "experimental_fitting":False,
        "method": "sinusoidal",
        "likelihood":"timeseries",
        "label": "MCMC",
        "optim_list":["E_0", "k_0", "Ru", "Cdl", "alpha"]
    }
"""
Other values description
-----------------------
Filter val:
    The width of the top hat filter either side of the harmonic peak, multiplied by the frequency.
Harmonic range:
    Defines which harmonics in the fourier spectrum that will be returned by the simulate() function
Num peaks:
    Defines the number of oscillations for the input potential for a simulated sinusoidal voltammetry experiment
"""
other_values={
        "filter_val": 0.5,
        "harmonic_range":list(range(3,9,1)),
        "num_peaks":30,
    }
"""
The param bounds dictionary is used to define the range of values which the CMAES algorithm can propose for each parameter.
"""
param_bounds={
        'E_0':[0.2, 0.3],
        'Ru': [0, 1e3],
        'Cdl': [0,1e-4],
        'k_0': [50, 1e3],
        "alpha":[0.4, 0.6],
    }
"""
Initialisation of the simulation class requires either dictionaries, as defined above, or the name of a file.
"""
SV_test=single_electron(file_name=None, dim_parameter_dictionary=param_list, simulation_options=simulation_options, other_values=other_values, param_bounds=param_bounds)
"""
To test individual parameter values we use the test_vals() function with a list of parameters, as defined by optim_list.
"""
test_current=SV_test.test_vals([param_list[x] for x in simulation_options["optim_list"]], "timeseries")
test_voltage=SV_test.define_voltages()
plt.plot(test_voltage, test_current)
plt.show()
"""
We will now add normal dispersion for E0 and alpha. We first update the paramater and param bounds dictionaries with a mean and standard deviation.
For dispersed paramters, the naming rule for the parameter is "parameter+_+(distribution parameter)". Currently, the distribution parameters are:
Normal - mean, std
Lognormal - loc, scale
Uniform - upper, lower
We also take this oppurtunity to remove the first two oscillations of the current
"""
param_list["E0_mean"]=0.2
param_list["E0_std"]=0.05
param_list["alpha_mean"]=0.5
param_list["alpha_std"]=0.01
param_bounds["E0_mean"]=[0.2, 0.3]
param_bounds["E0_std"]=[0.001, 0.1]
param_bounds["alpha_mean"]=[0.4, 0.6]
param_bounds["alpha_std"]=[0.001, 0.1]
simulation_options["no_transient"]=2/(param_list["omega"])
"""
We then update the optimisation list, and simulation options. We also need to specify the number of bins to approximate each of these distributions (please refer to the paper as to why and how this is done)
"""
simulation_options["GH_quadrature"]=True
simulation_options["optim_list"]=["E0_mean", "E0_std", "k_0", "Ru", "Cdl", "alpha_mean", "alpha_std"]
simulation_options["dispersion_bins"]=[5, 5]
"""
We then create a new initisation of the class
"""
SV_test=single_electron(file_name=None, dim_parameter_dictionary=param_list, simulation_options=simulation_options, other_values=other_values, param_bounds=param_bounds)
test_current=SV_test.test_vals([param_list[x] for x in simulation_options["optim_list"]], "timeseries")
test_voltage=SV_test.define_voltages(transient=False)
plt.plot(test_voltage, test_current)
plt.show()
"""
If we want to simulate the same parameters with a ramped input, we reduce the amplitude of the input potential, and change the simulation method. The ramped method uses a different non-dimensionalisation for the time,
so we need to define a scan rate, and remove the "original_omega" parameter
"""
ramped_param_list=copy.deepcopy(param_list)
ramped_sim_options=copy.deepcopy(simulation_options)
del ramped_param_list["original_omega"]
ramped_param_list["v"]=25e-3
ramped_param_list["d_E"]=150e-3
ramped_sim_options["method"]="ramped"
ramped_sim_options["no_transient"]=False
ramp_test=single_electron(file_name=None, dim_parameter_dictionary=ramped_param_list, simulation_options=ramped_sim_options, other_values=other_values, param_bounds=param_bounds)
test_current=ramp_test.test_vals([param_list[x] for x in simulation_options["optim_list"]], "timeseries")
test_voltage=ramp_test.define_voltages()
test_time=ramp_test.time_vec
plt.plot(test_time, test_current)
plt.show()
