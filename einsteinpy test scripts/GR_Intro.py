'''
REF : https://docs.einsteinpy.org/en/stable/
'''

from einsteinpy.coordinates import SphericalDifferential, CartesianDifferential, BoyerLindquistDifferential
from einsteinpy.metric import Schwarzschild, Kerr
from einsteinpy.bodies import Body
from einsteinpy.geodesic import Geodesic
from einsteinpy.plotting import GeodesicPlotter
from einsteinpy.symbolic import EinsteinTensor, ChristoffelSymbols
import numpy as np
import sympy
from astropy import units as u


'''
Creating Objects
'''
# # Creating a Schwarzschild Object (Spherical Coords)
# M = 5.972e24 * u.kg
# sph_coord = SphericalDifferential(306.0 * u.m, np.pi/2 * u.rad, -np.pi/6 * u.rad,
#                                   0 * u.m / u.s, 0 * u.rad / u.s, 1900 * u.rad / u.s)
# sph_obj = Schwarzschild.from_coords(sph_coord, M, 0 * u.s)
#
# # Creating a Schwarzschild Object (Cartesian Coords)
# cartsn_coord = CartesianDifferential(0.265003774 * u.km, -153.000000e-03 * u.km,  0 * u.km,
#                                      145.45557 * u.km / u.s, 251.93643748389 * u.km / u.s, 0 * u.km / u.s)
# cart_obj = Schwarzschild.from_coords(cartsn_coord, M, 0 * u.s)
#
#
# '''
# Calculating Trajectories and Time-Like Geodesics
# '''
# end_tau = 0.01
# step_size = 0.3e-6
# ans = sph_obj.calculate_trajectory(end_lambda=end_tau, OdeMethodKwargs={"stepsize": step_size})
# # Can return ans in Cartesian by:
# ans = sph_obj.calculate_trajectory(end_lambda=end_tau, OdeMethodKwargs={"stepsize": step_size}, return_cartesian=True)


'''
Bodies  -   Can define the attractor and the corresponding revolving bodies
            Plotting and geodesic calculation is easier
'''
# defining some bodies:
spin_factor = 0.3 * u.m
attractor = Body(name='BH', mass=1.989e30 * u.kg, a=spin_factor)
bl_obj = BoyerLindquistDifferential(50e5 * u.km, np.pi/2 * u.rad, np.pi * u.rad,
                                    0 * u.km / u.s, 0 * u.rad / u.s, 0 * u.rad / u.s,
                                    spin_factor)
particle = Body(differential=bl_obj, parent=attractor)
geodesic = Geodesic(body=particle, end_lambda=((1 * u.year).to(u.s)).value / 930,
                    step_size=((0.02 * u.min).to(u.s)).value,
                    metric=Kerr)
geodesic.trajectory     # returns the trajectory values

# Plotting the trajectory values
obj = GeodesicPlotter()
obj.plot(geodesic)
obj.show()


'''
Symbolic Calculations   -   Currently SchwarzschildMetric() cannot be called from package: einsteinpy.symbolic
'''
# m = SchwarzschildMetric()
# ch = ChristoffelSymbols.from_metric(m)
# print(ch[1, 2, :])
#
# m = SchwarzschildMetric()
# G1 = EinsteinTensor.from_metric(m)
# print(G1.arr)
