# Interstellar Motion

## Description

This project simulates our solar system using newtonian kinematics or gravitational relativity.

## Getting Started

### Installing

To look at the code just fork this repo and set up a virtual environment and install requirements.txt using
```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r 'requirements.txt'
```

### Executing program
#### Newtonian
This script simulates the solar system using vpython and numpy. The planet trajectories are calculated for time steps delta_t and displayed on the vpython screen.
```
python PlanetaryMotion2D.py
```
![alt text](https://github.com/MichaelCullen2011/InterstellarMotion/blob/master/screenshot1.png?raw=true)

#### General Relativity
With the help of einsteinpy this script plots the trajectory of a planet and a host using GR calculations.

You can change the planet that it tracks by changing the planet variable in the script.
```
python GR_SolarSystem.py
```

![alt text](https://github.com/MichaelCullen2011/InterstellarMotion/blob/master/screenshot2.png?raw=true)




## Authors

Contributors names and contact info

ex. Michael Cullen
michaelcullen2011@hotmail.co.uk


