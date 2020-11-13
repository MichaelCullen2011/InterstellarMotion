'''
REF : https://docs.einsteinpy.org/en/stable/
'''

from einsteinpy.plotting import StaticGeodesicPlotter
from einsteinpy.coordinates import SphericalDifferential
from einsteinpy.bodies import Body
from einsteinpy.geodesic import Geodesic
import numpy as np
import sympy
from astropy import units as u

'''
Variables
'''
attractor = Body(name="BH", mass=6e24 * u.kg, parent=None)
sph_obj = SphericalDifferential(130 * u.m, np.pi/2 * u.rad, -np.pi/8 * u.rad,
                                0 * u.m / u.s, 0 * u.rad / u.s, 1900 * u.rad / u.s)
object = Body(differential=sph_obj, parent=attractor)
geodesic = Geodesic(body=object, time=0 * u.s, end_lambda=0.002, step_size=5e-8)


'''
Plotting Animation
'''
obj = StaticGeodesicPlotter()
obj.animate(geodesic, interval=25)
obj.show()
















