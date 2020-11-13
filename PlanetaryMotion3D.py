from vpython import *
import numpy as np

'''
To Do:

Fix phi rotations so that bodies can orbit slightly off plane (currently is a mess)
'''


'''
Colors
'''
yellow = vector(1, 1, 0)
magenta = vector(1, 0, 1)
cyan = vector(0, 1, 1)
red = vector(1, 0, 0)
green = vector(0, 1, 0)
blue = vector(0, 0, 1)
white = vector(1, 1, 1)
black = vector(0, 0, 0)


'''
Equations
'''
cycles = 50     # Updates every 1/20 = 0.05 seconds
G = 6.67e-8    # N kg-2 Km2
t = 0
seconds = 1
seconds_hour = 3600
seconds_day = 86400
seconds_week = 604800
seconds_month = 2.628e6
seconds_year = 3.154e7
day = 1
week = 1
month = 1
year = 0
dt = seconds_hour  # a day
time_period_list = []


def x_y_and_z(distance, direction, theta, phi):
    theta_rads = theta * pi / 180
    phi_rads = phi * pi / 180
    if direction[0] == 0:
        direction[0] = 1
    if direction[1] == 0:
        direction[1] = 1
    if direction[2] == 0:
        direction[2] = 1

    radius = sqrt(distance[0]**2 + distance[1]**2 + distance[2]**2)
    x = radius * direction[0] * sin(theta_rads) * cos(phi_rads)
    y = radius * direction[1] * cos(theta_rads) * cos(phi_rads)
    z = radius * direction[2] * sin(phi_rads)
    x_value = abs(x)
    y_value = abs(y)
    z_value = abs(z)
    x_direction = np.sign(x)
    y_direction = np.sign(y)
    z_direction = np.sign(z)
    return [x, y, z], [x_value, y_value, z_value], [x_direction, y_direction, z_direction]


def force(m_large, m_small, direction, distance):
    grav_x, grav_y, grav_z = 0, 0, 0

    if direction[0] != 0:
        grav_x = G * m_large * m_small * direction[0] / distance[0]**2
    if direction[1] != 0:
        grav_y = G * m_large * m_small * direction[1] / distance[1]**2
    if direction[2] != 0:
        grav_z = G * m_large * m_small * direction[2] / distance[2]**2
    return grav_x, grav_y, grav_z


def plane_velocity(m_small, distance, direction):
    v_x, v_y, v_z = 0, 0, 0
    if distance[0] != 0:
        v_x = direction[0] * sqrt(G * m_small / distance[0])
    if distance[1] != 0:
        v_y = direction[1] * sqrt(G * m_small / distance[1])
    if distance[2] != 0:
        v_z = direction[2] * sqrt(G * m_small / distance[2])
    return [v_x, v_y, v_z]


def plane_accel(distance, direction, velocity):
    a_x, a_y, a_z = 0, 0, 0
    if distance[0] != 0:
        a_x = velocity[0]**2 / distance[0]
    if distance[1] != 0:
        a_y = velocity[1] ** 2 / distance[1]
    if distance[2] != 0:
        a_z = velocity[2] ** 2 / distance[2]
    return [a_x, a_y, a_z]


# def time_period(accel, m_large):
#     time = sqrt((4 * pi**2 * accel[3]**3) / (G * m_large))
#     return time


def increment(day, week, month, year):
    if month == 13:
        month = 1
        year += 1
    if week == 5:
        week = 1
        month += 1
    if day == 8:
        day = 1
        week += 1
    return day, week, month, year


'''
Building Bodies
'''
# Constants
count = 0
increase_size = 20
pps_amount = 100
retain_amount = 100

bodies_list = ['sun', 'mercury', 'venus',
               'earth', 'moon', 'mars',
               'jupiter', 'saturn', 'uranus',
               'neptune']
radius = {'sun': 696340, 'mercury': 2439.5 * increase_size, 'venus': 6052 * increase_size,
          'earth': 6371 * increase_size, 'moon': 3389.5 * increase_size, 'mars': 3389.5 * increase_size,
          'jupiter': 142984/2 * increase_size, 'saturn': 120536/2 * increase_size, 'uranus': 51118/2 * increase_size,
          'neptune': 49528/2 * increase_size}
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
pos = {}
velocity = {}
accel = {}
sun_initial_pos = vector(0, 0, 0)
for body in bodies_list:
    pos[body], distances_value[body], distances_direction[body] = x_y_and_z(distance=distances_value[body],
                                                                            direction=distances_direction[body],
                                                                            theta=theta_deg[body],
                                                                            phi=phi_deg[body])
    if body != 'sun':
        velocity[body] = plane_velocity(m_small=mass[body], distance=distances_value[body], direction=distances_direction[body])
        accel[body] = plane_accel(distance=distances_value[body], direction=distances_direction[body], velocity=velocity[body])
        if distances_value[body][0] + distances_value[body][1] != 0:
            d_theta[body] = sqrt(accel[body][0]**2 + accel[body][1]**2) * dt / sqrt(distances_value[body][0]**2 + distances_value[body][1]**2)
        if distances_value[body][2] != 0:
            d_phi[body] = accel[body][2] * dt / distances_value[body][2]
        theta_deg[body] = theta_deg[body] + (d_theta[body] * 180 / pi)
        phi_deg[body] = phi_deg[body] + (d_phi[body] * 180 / pi)

sun = sphere(pos=sun_initial_pos + vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]),
             radius=radius['sun'],
             make_trail=True, trail_type='points', trail_radius=radius['sun'], pps=pps_amount, retain=retain_amount, trail_color=yellow,
             color=color.yellow)
sun_label = label(pos=sun.pos, text='Sun', xoffset=20, yoffset=12, line=False,
                  space=radius['sun'],
                  height=10, border=6,
                  font='sans')

mercury = sphere(pos=sun.pos + vector(pos['mercury'][0], pos['mercury'][1], pos['mercury'][2]),
                 radius=radius['mercury'],
                 make_trail=True, trail_type='points', trail_radius=radius['mercury'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=white,
                 color=color.green)
mercury_label = label(pos=mercury.pos, text='Mercury', xoffset=20, yoffset=12, line=False,
                      space=radius['mercury'],
                      height=10, border=6,
                      font='sans')

venus = sphere(pos=sun.pos + vector(pos['venus'][0], pos['venus'][1], pos['venus'][2]),
               radius=radius['venus'],
               make_trail=True, trail_type='points', trail_radius=radius['venus'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=blue,
               color=color.green)
venus_label = label(pos=mercury.pos, text='Venus', xoffset=20, yoffset=12, line=False,
                    space=radius['venus'],
                    height=10, border=6,
                    font='sans')

earth = sphere(pos=sun.pos + vector(pos['earth'][0], pos['earth'][1], pos['earth'][2]),
               radius=radius['earth'],
               make_trail=True, trail_type='points', trail_radius=radius['earth'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=green,
               color=color.green)
earth_label = label(pos=earth.pos, text='Earth', xoffset=20, yoffset=12, line=False,
                    space=radius['earth'],
                    height=10, border=6,
                    font='sans')

# moon = sphere(pos=earth.pos + vector(pos['moon'][0], pos['moon'][1], pos['moon'][2]),
#               radius=radius['moon'],
#               make_trail=False, pps=pps_amount, retain=retain_amount, trail_color=white,
#               color=color.white)
# moon_label = label(pos=moon.pos, text='Moon', line=False,
#                    space=radius['moon'],
#                    height=10, border=6,
#                    font='sans')
#
# mars = sphere(pos=sun.pos + vector(pos['mars'][0], pos['mars'][1], pos['mars'][2]),
#               radius=radius['mars'],
#               make_trail=True, trail_type='points', trail_radius=radius['mars'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=red,
#               color=color.red)
# mars_label = label(pos=mars.pos, text='Mars', xoffset=20, yoffset=12, line=False,
#                    space=radius['mars'],
#                    height=10, border=6,
#                    font='sans')
#
# jupiter = sphere(pos=sun.pos + vector(pos['jupiter'][0], pos['jupiter'][1], pos['jupiter'][2]),
#                  radius=radius['jupiter'],
#                  make_trail=True, trail_type='points', trail_radius=radius['jupiter'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=magenta,
#                  color=color.red)
# jupiter_label = label(pos=jupiter.pos, text='Jupiter', xoffset=20, yoffset=12, line=False,
#                       space=radius['jupiter'],
#                       height=10, border=6,
#                       font='sans')
#
# saturn = sphere(pos=sun.pos + vector(pos['saturn'][0], pos['saturn'][1], pos['saturn'][2]),
#                 radius=radius['saturn'],
#                 make_trail=True, trail_type='points', trail_radius=radius['saturn'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=yellow,
#                 color=color.red)
# saturn_label = label(pos=saturn.pos, text='Saturn', xoffset=20, yoffset=12, line=False,
#                      space=radius['saturn'],
#                      height=10, border=6,
#                      font='sans')
#
# uranus = sphere(pos=sun.pos + vector(pos['uranus'][0], pos['uranus'][1], pos['uranus'][2]),
#                 radius=radius['uranus'],
#                 make_trail=True, trail_type='points', trail_radius=radius['uranus'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=white,
#                 color=color.red)
# uranus_label = label(pos=uranus.pos, text='Uranus', xoffset=20, yoffset=12, line=False,
#                      space=radius['uranus'],
#                      height=10, border=6,
#                      font='sans')
#
# neptune = sphere(pos=sun.pos + vector(pos['neptune'][0], pos['neptune'][1], pos['neptune'][2]),
#                  radius=radius['neptune'],
#                  make_trail=True, trail_type='points', trail_radius=radius['neptune'] * increase_size, pps=pps_amount, retain=retain_amount, trail_color=cyan,
#                  color=color.red)
# neptune_label = label(pos=neptune.pos, text='Neptune', xoffset=20, yoffset=12, line=False,
#                       space=radius['neptune'],
#                       height=10, border=6,
#                       font='sans')


focus_range = distances_value['earth'][0]
focus_item = sun
n = 0
'''
Animation Loop
'''
while n < 2:
    rate(cycles)

    # New Values
    for body in bodies_list:
        pos[body], distances_value[body], distances_direction[body] = x_y_and_z(distance=distances_value[body],
                                                                                direction=distances_direction[body],
                                                                                theta=theta_deg[body],
                                                                                phi=phi_deg[body])
        # print(pos, "\n", distances_value, "\n", distances_direction)
        if body != 'sun':
            velocity[body] = plane_velocity(m_small=mass[body], distance=distances_value[body],
                                            direction=distances_direction[body])
            accel[body] = plane_accel(distance=distances_value[body], direction=distances_direction[body],
                                      velocity=velocity[body])
            if distances_value[body][0] + distances_value[body][1] != 0:
                d_theta[body] = sqrt(accel[body][0] ** 2 + accel[body][1] ** 2) * dt / sqrt(distances_value[body][0]**2 + distances_value[body][1]**2)
            if distances_value[body][2] != 0:
                d_phi[body] = accel[body][2] * dt / distances_value[body][2]
            theta_deg[body] = theta_deg[body] + (d_theta[body] * 180 / pi)
            phi_deg[body] = phi_deg[body] + (d_phi[body] * 180 / pi)

    # Incrementing
    if dt == seconds_day * cycles:
        day += 1
        for i in range(4):
            day, week, month, year = increment(day, week, month, year)
    elif dt == seconds_week * cycles:
        week += 1
        for i in range(3):
            day, week, month, year = increment(day, week, month, year)
    elif dt == seconds_month * cycles:
        month += 1
        for i in range(2):
            day, week, month, year = increment(day, week, month, year)
    elif dt == seconds_year * cycles:
        year += 1
        day, week, month, year = increment(day, week, month, year)
    t += dt

    # Updating Positions
    for body in bodies_list:
        pos[body], distances_value[body], distances_direction[body] = x_y_and_z(distance=distances_value[body],
                                                                                direction=distances_direction[body],
                                                                                theta=theta_deg[body],
                                                                                phi=phi_deg[body])

    sun.pos = sun_initial_pos + vector(pos['sun'][0], pos['sun'][1], pos['sun'][2])
    sun_label.pos = sun_initial_pos + vector(pos['sun'][0], pos['sun'][1], pos['sun'][2])

    mercury.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['mercury'][0], pos['mercury'][1], pos['mercury'][2])
    mercury_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['mercury'][0], pos['mercury'][1], pos['mercury'][2])

    venus.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['venus'][0], pos['venus'][1], pos['venus'][2])
    venus_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['venus'][0], pos['venus'][1], pos['venus'][2])

    earth.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['earth'][0], pos['earth'][1], pos['earth'][2])
    earth_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['earth'][0], pos['earth'][1], pos['earth'][2])

    # moon.pos = vector(pos['earth'][0], pos['earth'][1], pos['earth'][2]) + vector(pos['moon'][0], pos['moon'][1], pos['moon'][2])
    # moon_label.pos = vector(pos['earth'][0], pos['earth'][1], pos['earth'][2]) + vector(pos['moon'][0], pos['moon'][1], pos['moon'][2])
    #
    # mars.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['mars'][0], pos['mars'][1], pos['mars'][2])
    # mars_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['mars'][0], pos['mars'][1], pos['mars'][2])
    #
    # jupiter.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['jupiter'][0], pos['jupiter'][1], pos['jupiter'][2])
    # jupiter_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['jupiter'][0], pos['jupiter'][1], pos['jupiter'][2])
    #
    # saturn.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['saturn'][0], pos['saturn'][1], pos['saturn'][2])
    # saturn_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['saturn'][0], pos['saturn'][1], pos['saturn'][2])
    #
    # uranus.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['uranus'][0], pos['uranus'][1], pos['uranus''][2])
    # uranus_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['uranus'][0], pos['uranus'][1], pos['uranus'][2])
    #
    # neptune.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['neptune'][0], pos['neptune'][1], pos['neptune'][2])
    # neptune_label.pos = vector(pos['sun'][0], pos['sun'][1], pos['sun'][2]) + vector(pos['neptune'][0], pos['neptune'][1], pos['neptune'][2])

    # scene.range = focus_range
    # scene.camera.follow(focus_item)

'''
Screen Settings
'''
# Constants
screen_dimension = focus_range

# Settings
scene.background = color.rgb_to_hsv(color.black)
scene.range = screen_dimension


