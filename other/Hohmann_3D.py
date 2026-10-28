import matplotlib.pyplot as plt
from poliastro.bodies import Earth
from poliastro.maneuver import Maneuver
from poliastro.twobody import Orbit
from poliastro.util import time_range
from poliastro.plotting.static import StaticOrbitPlotter
import plotly.graph_objects as go 
from astropy import units as u
import os
import numpy as np

def add_orbit(fig, orbit, label):
        r = orbit.sample(values=1000)
        fig.add_trace(go.Scatter3d(
            x=r.x.to(u.km).value,
            y=r.y.to(u.km).value,
            z=r.z.to(u.km).value,
            mode='lines',
            name=label
        ))
def add_planet(fig, Planet):
    phi, teta = np.mgrid[0:2*np.pi:1000j, 0:np.pi:500j]
    x = Planet.R.to(u.km).value * np.cos(phi) * np.sin(teta)
    y = Planet.R.to(u.km).value * np.sin(phi) * np.sin(teta)
    z = Planet.R.to(u.km).value * np.cos(teta)
    fig.add_trace(go.Mesh3d(
    x=x.flatten(),
    y=y.flatten(),
    z=z.flatten(),
    color='blue',
    opacity=1,
    showscale=False
    ))
    
print('\033[92m',"INIZIO PROGRAMMA",'\033[0m')


orbit_initial = Orbit.circular(Earth, alt=700*u.km, inc=80*u.deg)
hoh = Maneuver.hohmann(orbit_initial, 17900 << u.km)
orbit_transfer, orbit_final = orbit_initial.apply_maneuver(hoh, intermediate=True)


TIPOLOGIA_PLOT = 3
"""
PLOT 1 = plotly, apertura schermata web
PLOT 2 = matplotlib, problemi con la dimensione degli assi
"""


if TIPOLOGIA_PLOT==1:

    fig = go.Figure()
    add_orbit(fig, orbit_initial, 'Orbit initial')
    add_orbit(fig, orbit_transfer, 'Orbit transfer')
    add_orbit(fig, orbit_final, 'Orbit final')
    add_planet(fig, Earth)

    fig.show()


if TIPOLOGIA_PLOT==2:


    fig = plt.figure()
    plotter = fig.add_subplot(projection = "3d")

    positions_1 = orbit_initial.sample(values=1000)
    r_orb_init = (positions_1.x.to(u.km).value,positions_1.y.to(u.km).value,positions_1.z.to(u.km).value)

    positions_2 = orbit_transfer.sample(values=1000)
    r_orb_tran = (positions_2.x.to(u.km).value,positions_2.y.to(u.km).value,positions_2.z.to(u.km).value)

    positions_3 = orbit_final.sample(values=1000)
    r_orb_fin = (positions_3.x.to(u.km).value,positions_3.y.to(u.km).value,positions_3.z.to(u.km).value)

    phi, teta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
    x = Earth.R.to(u.km).value * np.cos(phi) * np.sin(teta)
    y = Earth.R.to(u.km).value * np.sin(phi) * np.sin(teta)
    z = Earth.R.to(u.km).value * np.cos(teta)


    plotter.plot(r_orb_init[0],r_orb_init[1],r_orb_init[2], label="Initial Orbit")
    plotter.plot(r_orb_tran[0],r_orb_tran[1],r_orb_tran[2], label="Transfer Orbit")
    plotter.plot(r_orb_fin[0],r_orb_fin[1],r_orb_fin[2], label="Final Orbit")
    plotter.plot_surface(x, y, z, label="Earth")

    plotter.set_xlabel("X (km)")
    plotter.set_ylabel("Y (km)")
    plotter.set_zlabel("Z (km)")
    max_range = np.array([r_orb_init[0].max(), r_orb_init[1].max(), r_orb_init[2].max(),
                        r_orb_tran[0].max(), r_orb_tran[1].max(), r_orb_tran[2].max(),
                        r_orb_fin[0].max(), r_orb_fin[1].max(), r_orb_fin[2].max(),
                        Earth.R.to(u.km).value]).max()
    min_range = np.array([r_orb_init[0].min(), r_orb_init[1].min(), r_orb_init[2].min(),
                        r_orb_tran[0].min(), r_orb_tran[1].min(), r_orb_tran[2].min(),
                        r_orb_fin[0].min(), r_orb_fin[1].min(), r_orb_fin[2].min(),
                        Earth.R.to(u.km).value]).min()
    plotter.set_xlim([min_range, max_range])
    plotter.set_ylim([min_range, max_range])
    plotter.set_zlim([min_range, max_range])


    plotter.legend()

    plt.show()




print('\033[92m',"FINE PROGRAMMA",'\033[0m')


