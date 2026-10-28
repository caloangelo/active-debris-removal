from matplotlib import pyplot as plt
import numpy as np
from astropy.coordinates import solar_system_ephemeris
from astropy.time import Time, TimeDelta
from astropy import units as u
from poliastro.bodies import Earth, Moon
from poliastro.constants import rho0_earth, H0_earth
from poliastro.core.elements import rv2coe
from poliastro.core.perturbations import (
    atmospheric_drag_exponential,
    third_body,
    J2_perturbation,
)
from poliastro.core.propagation import func_twobody
from poliastro.ephem import build_ephem_interpolant
from poliastro.plotting import OrbitPlotter3D
from poliastro.twobody import Orbit
from poliastro.twobody.propagation import CowellPropagator
from poliastro.twobody.sampling import EpochsArray
from poliastro.util import norm
from poliastro.twobody.events import LithobrakeEvent
import plotly.graph_objects as go 
import csv
import time
"""
VERIFICA ATMOFERA ANDAMENTO ESPONENZIALE INVERTITO









"""
def f(t0, state, k):
    du_kep = func_twobody(t0, state, k)
    ax, ay, az = atmospheric_drag_exponential(
        t0,
        state,
        k,
        R=R,
        C_D=C_D,
        A_over_m=A_over_m,
        H0=H0,
        rho0=rho0,
    )
    du_ad = np.array([0, 0, 0, ax, ay, az])

    return du_kep + du_ad
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

# starting program
print('\033[92m',"INIZIO PROGRAMMA",'\033[0m')
start_time = time.process_time()


# atmospheric drag
C_D = 0.8
A_over_m = ((np.pi / 4.0) * (u.m**2) / (100 * u.kg)).to_value(
    u.km**2 / u.kg
)  # km^2/kg
A_over_m = 0.000785 # km^2/kg
B = C_D * A_over_m
rho0 = rho0_earth.to(u.kg / u.km**3).value  # kg/km^3
H0 = H0_earth.to(u.km).value
R = Earth.R.to(u.km).value # impact distance" (set to right atmospheric wanted final altitude)

# orbit
k = Earth.k.to(u.km**3 / u.s**2).value
orbit = Orbit.circular(
    Earth, 300 * u.km, epoch=Time(0.0, format="jd", scale="tdb")
)

# events
lithobrake_event = LithobrakeEvent(R+50)
events = [lithobrake_event]

# propagator
tofs = TimeDelta(np.linspace(0 * u.h, 2 * u.h, num=500)) #20,12e3 4min
rr, _ = orbit.to_ephem(
    EpochsArray(
        orbit.epoch + tofs, method=CowellPropagator(f=f, events=events)
    ),
).rv()

H = norm(rr, axis=1).to(u.km).value - R
rho = rho0 * np.exp(-(H) / H0)

print(rho)
print(H)
plt.plot(H,rho)
plt.xlabel = "H"
plt.ylabel = "rho"

plt.show()
# Dati da scrivere nel file CSV
dati = [
    H,
    rho
]
# Scrivi i dati nel file CSV
with open("csv_atmosferico.csv", mode='w', newline='') as file_csv:
    writer = csv.writer(file_csv)
    writer.writerows(zip(*dati))






# plots

fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=rr[:,0].to(u.km).value,
    y=rr[:,1].to(u.km).value,
    z=rr[:,2].to(u.km).value,
    mode='lines',
    name="orbit decayment"
))
#add_planet(fig,Earth)
fig.show()

final_altitude = norm(rr, axis=1)[-1].to(u.km).value - R
reached_altitude = final_altitude <= 0.01*R 
if reached_altitude:
    print(
    "\n",
    "orbital decay seen after", lithobrake_event.last_t.to(u.d).value, "days \n",
    "orbital decay seen after", lithobrake_event.last_t.to(u.d).value*24, "hours \n",
    "orbital decay seen after", lithobrake_event.last_t.to(u.d).value*24*60, "minutes"
    )
else:
    print(
        "\n",
        "\033[93mWanted altitude not reached\033[0m, final altitude of", final_altitude,"km","\n",
        "reached after",lithobrake_event.last_t.to(u.d).value,"days \n",
        "\t\tor ", lithobrake_event.last_t.to(u.d).value*24, "hours \n",
         "\t\tor ", lithobrake_event.last_t.to(u.d).value*24*60, "minutes"
    )

plt.ylabel("h(t)")
plt.xlabel("t, days")
plt.plot(tofs[: len(rr)].value, norm(rr, axis=1) - Earth.R)
plt.show()

# print(norm(rr, axis=1) - Earth.R)

# finish program
end_time = time.process_time()
crono = end_time-start_time
print('\033[93m',"\n PROCESS TIME OF:")
print(crono,"s","\t",
      crono/60,"min","\t",
      crono/60/60,"h","\033[0m")
print('\033[92m',"FINE PROGRAMMA",'\033[0m')


import matlib

# Creare l'oggetto del modello atmosferico
# Nota: questo è solo un esempio generico. MATLIB potrebbe avere una sintassi diversa.

model = matlib.AtmosphericModel()

# Calcolare i parametri atmosferici per una data altitudine
altitude = 300  # in km
parameters = model.get_parameters(altitude)

print(f"Densità: {parameters['density']} kg/m^3")
print(f"Temperatura: {parameters['temperature']} K")
print(f"Pressione: {parameters['pressure']} Pa")
