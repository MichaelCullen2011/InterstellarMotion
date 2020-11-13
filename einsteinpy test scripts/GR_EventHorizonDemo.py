'''
REF : https://docs.einsteinpy.org/en/stable/
'''

import numpy as np
import sympy
from astropy import units as u
import matplotlib.pyplot as plt
from einsteinpy.utils import kerr_utils, schwarzschild_radius

'''
Variables
'''
M = 4e30
scr = schwarzschild_radius(M * u.kg).value  # calculates radius based on M

# for a near maximally rotating BH
a1 = 0.499999 * scr

# for an ordinary BH
a2 = 0.3 * scr


'''
Calculating Ergosphere and Event Horizon (spherical coords)
'''
ergo1, ergo2, hori1, hori2 = list(), list(), list(), list()
thetas = np.linspace(0, np.pi, 720)

for angle in thetas:
    ergo1.append(kerr_utils.radius_ergosphere(M, a1, angle, "Spherical"))
    ergo2.append(kerr_utils.radius_ergosphere(M, a2, angle, "Spherical"))
    hori1.append(kerr_utils.event_horizon(M, a1, angle, "Spherical"))
    hori2.append(kerr_utils.event_horizon(M, a2, angle, "Spherical"))
ergo1, ergo2, hori1, hori2 = np.array(ergo1), np.array(ergo2), np.array(hori1), np.array(hori2)


'''
Calculating X and Y for Plotting
'''
Xe1, Ye1 = ergo1[:, 0] * np.sin(ergo1[:, 1]), ergo1[:, 0] * np.cos(ergo1[:, 1])
Xh1, Yh1 = hori1[:, 0] * np.sin(hori1[:, 1]), hori1[:, 0] * np.cos(hori1[:, 1])
Xe2, Ye2 = ergo2[:, 0] * np.sin(ergo2[:, 1]), ergo2[:, 0] * np.cos(ergo2[:, 1])
Xh2, Yh2 = hori2[:, 0] * np.sin(hori2[:, 1]), hori2[:, 0] * np.cos(hori2[:, 1])


'''
Plotting
'''
fig, ax = plt.subplots()

# For maximally rotating
ax.fill(Xh1, Yh1, 'b', Xe1, Ye1, 'r', alpha=0.3)
ax.fill(-1 * Xh1, Yh1, 'b', -1 * Xe1, Ye1, 'r', alpha=0.3)
plt.show()

# For normally rotating
ax.fill(Xh2, Yh2, 'b', Xe2, Ye2, 'r', alpha=0.3)
ax.fill(-1 * Xh2, Yh2, 'b', -1 * Xe2, Ye2, 'r', alpha=0.3)
plt.show()

# Inner body represents event horizon and outer body represents ergosphere
