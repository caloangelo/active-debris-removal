import matplotlib.pyplot as plt
from poliastro.bodies import Earth
from poliastro.maneuver import Maneuver
from poliastro.twobody import Orbit
from poliastro.util import time_range
from poliastro.plotting.static import StaticOrbitPlotter
from poliastro.plotting import OrbitPlotter2D
from astropy import units as u
import os

print('\033[92m',"INIZIO PROGRAMMA",'\033[0m')


orbit_initial = Orbit.circular(Earth, alt=700*u.km, inc=80*u.deg)
hoh = Maneuver.hohmann(orbit_initial, 7900 << u.km)
orbit_transfer, orbit_final = orbit_initial.apply_maneuver(hoh, intermediate=True)

plotter = StaticOrbitPlotter()
plotter.plot(orbit_initial, label="orbita circolare leo", color= "blue")
plotter.plot(orbit_transfer, label = "orbit_transfer",color= "red")
plotter.plot(orbit_final, label = "orbit_final",color= "yellow")
plt.show()
print('\033[92m',"FINE PROGRAMMA",'\033[0m')

