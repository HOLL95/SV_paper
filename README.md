# Sinusoidal voltammetry paper code
This repository acts as a companion for our paper about using parameterising sinusoidal voltammetry experiments. To install and run it, you will require a distribution of linux, git, python3.6 or higher (and the associated package manager pip3), boost and cmake. If you do not have these programs they can be installed on e.g. Ubuntu can be done using ```apt```. 
```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python3.6
sudo apt-get install pip3
sudo apt-get install cmake
sudo apt-get install libboost-all-dev
```
Once these packages are installed, you can clone this repository, i.e. 
```
git clone https://github.com/HOLL95/SV_paper/
```
and download the required submodules.
```
cd SV_paper
git submodule init
git submodule update
```
Finally, you can install this repository using ```pip3```
```
pip3 install -r requirements.txt
```
If you do not have install priveliges but have all the required packages installed on your system then you can install a user only version 
```
pip3 install -r requirements.txt --user
```
Simulation code can be found in the ```SV_paper/src``` directory, and code to generate each of the figures in the main body of the paper can be found in ```SV_paper/figures```
