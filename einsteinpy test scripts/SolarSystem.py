from astropy import units as u
import numpy as np
from einsteinpy.metric import Schwarzschild
from einsteinpy.plotting import StaticGeodesicPlotter
from einsteinpy.coordinates import SphericalDifferential
from einsteinpy.bodies import Body
from einsteinpy.geodesic import Geodesic
from einsteinpy.plotting import GeodesicPlotter

'''
Defining Variables and Objects
'''
bodies_list = ['sun', 'mercury', 'venus',
               'earth', 'moon', 'mars',
               'jupiter', 'saturn', 'uranus',
               'neptune']
radius = {'sun': 696340, 'mercury': 2439.5, 'venus': 6052,
          'earth': 6371, 'moon': 3389.5, 'mars': 3389.5,
          'jupiter': 142984/2, 'saturn': 120536/2, 'uranus': 51118/2,
          'neptune': 49528/2}
aphelion = {'sun': 0, 'mercury': 69.8e6,
            'venus': 108.9e6, 'earth': 152.1e6,
            'moon': 0.406e6, 'mars': 249.2e6,
            'jupiter': 816.6e6, 'saturn': 1514.5e6, 'uranus': 3003.6e6,
            'neptune': 4545.7e6}
perihelion = {'sun': 0, 'mercury': 46.0e6,
              'venus': 107.5e6, 'earth': 147.1e6,
              'moon': 0.363e6, 'mars': 206.6e6,
              'jupiter': 740.5e6, 'saturn': 1352.6e6, 'uranus': 2741.3e6,
              'neptune': 4444.5e6}
distances_value = {'sun': [0, 0, 0], 'mercury': [0, 57.9e6, 0],
                   'venus': [0, 108.2e6, 0], 'earth': [0, 149.11e6, 0],
                   'moon': [0, 384400, 0], 'mars': [0, 213.51e6, 0],
                   'jupiter': [0, 778.6e6, 0], 'saturn': [0, 1433.5e6, 0], 'uranus': [0, 2872.5e6, 0],
                   'neptune': [0, 4495.1e6, 0]}
distances_direction = {'sun': [1, 1, 1], 'mercury': [1, 1, 1],
                       'venus': [1, 1, 1], 'earth': [1, 1, 1],
                       'moon': [1, 1, 1], 'mars': [1, 1, 1],
                       'jupiter': [1, 1, 1], 'saturn': [1, 1, 1], 'uranus': [1, 1, 1],
                       'neptune': [1, 1, 1]}
mass = {'sun': 1.989e30, 'mercury': 0.33e24, 'venus': 4.87e24,
        'earth': 5.972e24, 'moon': 7.34767309e22, 'mars': 6.39e23,
        'jupiter': 1898e24, 'saturn': 568e24, 'uranus': 86.8e24,
        'neptune': 103e24}
theta_deg = {'sun': 0, 'mercury': 1, 'venus': 1,
             'earth': 1, 'moon': 1, 'mars': 1,
             'jupiter': 1, 'saturn': 1, 'uranus': 1,
             'neptune': 1}
phi_deg = {'sun': 0, 'mercury': 0, 'venus': 0,
           'earth': 1, 'moon': 0, 'mars': 0,
           'jupiter': 0, 'saturn': 0, 'uranus': 0,
           'neptune': 0}
d_theta = {'sun': 0, 'mercury': 0, 'venus': 0,
           'earth': 0, 'moon': 0, 'mars': 0,
           'jupiter': 0, 'saturn': 0, 'uranus': 0,
           'neptune': 0}
d_phi = {'sun': 0, 'mercury': 0, 'venus': 0,
         'earth': 0, 'moon': 0, 'mars': 0,
         'jupiter': 0, 'saturn': 0, 'uranus': 0,
         'neptune': 0}

M = 1.989e30 * u.kg  # mass of sun
distance = 147.09e6 * u.km
speed_at_perihelion = 30.29 * u.km / u.s
omega = (u.rad * speed_at_perihelion) / distance

# SphericalDifferential(name=str,
#                       mass=kg,
#                       R(radius)=units,
#                       differential=coordinates of body,
#                       a=spin factor,
#                       q=charge,
#                       is_attractor=True/False,
#                       parent=who's the parent body)
earth_obj = SphericalDifferential(distance,
                                  np.pi / 2 * u.rad,
                                  np.pi * u.rad,
                                  0 * u.km / u.s,
                                  0 * u.rad / u.s,
                                  omega)

moon_obj = SphericalDifferential(perihelion['earth'] * u.km,
                                 np.pi / 2 * u.rad,
                                 np.pi * u.rad,
                                 0 * u.km / u.s,
                                 0 * u.rad / u.s,
                                 omega)

'''
Calculating Trajectory
'''
# Set for a year (in seconds)
end_lambda = ((1 * u.year).to(u.s)).value
# Choosing stepsize for ODE solver to be 5 minutes
stepsize = ((5 * u.min).to(u.s)).value

'''
Trajectory to Cartesian
'''
obj = Schwarzschild.from_coords(earth_obj, M)
ans = obj.calculate_trajectory(
    end_lambda=end_lambda, OdeMethodKwargs={"stepsize": stepsize}, return_cartesian=True
)


'''
Calculating Distance
'''
# # At Aphelion   -   r should be 152.1e6 km
# r = np.sqrt(np.square(ans[1][:, 1]) + np.square(ans[1][:, 2]))
# i = np.argmax(r)
# print((r[i] * u.m).to(u.km))
# #                   speed should be 29.29 km/s
# print(((ans[1][i][6]) * u.m / u.s).to(u.km / u.s))
# #                   eccentricity should be 0.0167
# xlist, ylist = ans[1][:, 1], ans[1][:, 2]
# i = np.argmax(ylist)
# x, y = xlist[i], ylist[i]
# eccentricity = x / (np.sqrt(x ** 2 + y ** 2))
# print(eccentricity)


'''
Animating
'''
Sun = Body(name="Sun", mass=M, parent=None)
Earth = Body(name="Earth", differential=earth_obj, parent=Sun)
geodesic = Geodesic(body=Earth, time=0 * u.s, end_lambda=end_lambda, step_size=stepsize)
sun_earth = StaticGeodesicPlotter()
sun_earth.animate(geodesic, interval=5)
sun_earth.show()

