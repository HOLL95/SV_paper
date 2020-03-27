# Sinusoidal voltammetry paper code
This repository acts as a companion for our paper about using parameterising sinusoidal voltammetry experiments. To install and run it, you will require a distribution of linux, git, python3.6 or higher (and the associated package manager pip), boost and cmake. If you do not have these programs they can be installed on e.g. Ubuntu can be done using ```apt```. 
```
sudo apt-get update
sudo apt-get install git python3.6 pip3 cmake libboost-all-dev
```

Once these packages are installed, you can clone this repository and it's submodules, 
i.e. 

```
git clone --recurse-submodules https://github.com/HOLL95/SV_paper
```

The authors recommend that you install this repository in a Python virtual environment. 
Setup a new environment `env` and then activate it like so:

```
python3 -m venv env
source env/bin/activate
```

Finally, you can install this repository using ```pip```
```
pip install -r requirements.txt
```

Simulation code can be found in the ```SV_paper/src``` directory, and code to generate 
each of the figures in the main body of the paper can be found in ```SV_paper/figures```
