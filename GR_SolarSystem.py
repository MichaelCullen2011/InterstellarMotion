from astropy import units as u
import numpy as np
from einsteinpy.metric import Schwarzschild
from einsteinpy.plotting import StaticGeodesicPlotter
from einsteinpy.coordinates import SphericalDifferential
from einsteinpy.bodies import Body
from einsteinpy.geodesic import Geodesic

def run(planet):
    '''
    Defining Variables and Objects
    '''
    grav_constant = 6.67430e-20 * u.km**3 / (u.kg * u.s**2)     # km3 kg-1 s-2
    bodies_list = ['sun', 'mercury', 'venus', 'earth', 'moon']
    all_bodies_list = ['sun', 'mercury', 'venus',
                    'earth', 'moon', 'mars',
                    'jupiter', 'saturn', 'uranus',
                    'neptune']
    radius = {'sun': 696340 * u.km, 'mercury': 2439.5 * u.km, 'venus': 6052 * u.km,
            'earth': 6371 * u.km, 'moon': 3389.5 * u.km, 'mars': 3389.5 * u.km,
            'jupiter': 142984/2 * u.km, 'saturn': 120536/2 * u.km, 'uranus': 51118/2 * u.km,
            'neptune': 49528/2 * u.km}
    aphelion = {'sun': 0 * u.km, 'mercury': 69.8e6 * u.km,
                'venus': 108.9e6 * u.km, 'earth': 152.1e6 * u.km,
                'moon': 0.406e6 * u.km, 'mars': 249.2e6 * u.km,
                'jupiter': 816.6e6 * u.km, 'saturn': 1514.5e6 * u.km, 'uranus': 3003.6e6 * u.km,
                'neptune': 4545.7e6 * u.km}
    perihelion = {'sun': 0 * u.km, 'mercury': 46.0e6 * u.km,
                'venus': 107.5e6 * u.km, 'earth': 147.1e6 * u.km,
                'moon': 0.363e6 * u.km, 'mars': 206.6e6 * u.km,
                'jupiter': 740.5e6 * u.km, 'saturn': 1352.6e6 * u.km, 'uranus': 2741.3e6 * u.km,
                'neptune': 4444.5e6 * u.km}
    mass = {'sun': 1.989e30 * u.kg, 'mercury': 0.33e24 * u.kg, 'venus': 4.87e24 * u.kg,
            'earth': 5.972e24 * u.kg, 'moon': 7.34767309e22 * u.kg, 'mars': 6.39e23 * u.kg,
            'jupiter': 1898e24 * u.kg, 'saturn': 568e24 * u.kg, 'uranus': 86.8e24 * u.kg,
            'neptune': 103e24 * u.kg}

    distances_value = {}
    speed_at_perihelion = {}
    omega = {}

    for body in bodies_list:
        distances_value[body] = [0 * u.km, perihelion[body], 0 * u.km]
        if body != 'sun':
            speed_at_perihelion[body] = np.sqrt(grav_constant * mass['sun'] / perihelion[body])
            omega[body] = (u.rad * speed_at_perihelion[body]) / perihelion[body]

    '''
    Spherical Differentiation Objects and Body Objects
    '''

    # args(name=str, mass=kg, R(radius)=units, differential=coordinates of body,
    #       a=spin factor, q=charge, is_attractor=True/False, parent=who's the parent body)

    sd_obj = {}
    body_obj = {}
    for object in bodies_list:
        if object != 'sun':
            sd_obj[object] = SphericalDifferential(perihelion[object],
                                                np.pi / 2 * u.rad,
                                                np.pi * u.rad,
                                                0 * u.km / u.s,
                                                0 * u.rad / u.s,
                                                omega[object])
            body_obj[object] = Body(name=object, mass=mass[object], differential=sd_obj[object], parent=body_obj['sun'])
        elif object == 'sun':
            body_obj[object] = Body(name="sun", mass=mass[object], parent=None)
        elif object == 'moon':
            body_obj[object] = Body(name=object, mass=mass[object], differential=sd_obj[object], parent=body_obj['earth'])

    '''
    Calculating Trajectory
    '''
    # Set for a year (in seconds)
    end_lambda = {'earth': ((1 * u.year).to(u.s)).value, 'moon': ((1/12 * u.year).to(u.s)).value}
    # Choosing stepsize for ODE solver to be 5 minutes
    stepsize = {'earth': ((5 * u.min).to(u.s)).value, 'moon': ((5/12 * u.min).to(u.s)).value}

    '''
    Trajectory to Cartesian
    '''


    def get_schwarz():
        schwarz_obj = {}
        schwarz_ans = {}
        for object in bodies_list:
            if object != 'sun':
                schwarz_obj[object] = Schwarzschild.from_coords(sd_obj[object], mass['sun'])
                schwarz_ans[object] = schwarz_obj[object].calculate_trajectory(
                    end_lambda=end_lambda['earth'], OdeMethodKwargs={"stepsize": stepsize['earth']}, return_cartesian=True
                )
        return schwarz_obj, schwarz_ans


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
    geodesic = {}
    plotter = {}
    for object in bodies_list:
        if object != 'sun':
            if object == 'moon':
                geodesic[object] = Geodesic(body=body_obj[object], time=0 * u.s, end_lambda=end_lambda['moon'],
                                            step_size=stepsize['moon'])
            geodesic[object] = Geodesic(body=body_obj[object], time=0 * u.s, end_lambda=end_lambda['earth'],
                                        step_size=stepsize['earth'])


    sgp = StaticGeodesicPlotter()
    sgp.animate(geodesic[planet], interval=5)    # Objects currently limited to ['sun', 'mercury', 'venus', 'earth', 'moon']
    sgp.show()

if __name__=='__main__':
    planet = 'earth'
    run(planet)