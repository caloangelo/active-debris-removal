from astropy import units as u
from poliastro.bodies import Earth
import numpy as np
import time
import matplotlib.pyplot as plt
from Thrusters import thrusters
from Debris import Debris, stages
from input.INPUTS import R,K, DECAYMENT_FILE, TOTAL_LOG
from Logger import Logger

def V_cir(r:float):

    r = r + R
    v = np.sqrt(K/r)
    return v
def V_ell(rp, ra, r):
    rp = rp+R
    ra = ra+R
    r = r+R
    a = (rp+ra)/2
    v = np.sqrt(-K/a + 2*K/r)

    return v
def Hoh_time(rp, ra):
    rp = rp+R
    ra = ra+R
    a = (rp+ra)/2
    time = np.pi*((a**3)/K)**(0.5)
    return time
def fuel_mass_thrusters(DV,debris:Debris):

    A = DV*1000/(thrusters.Isp * 9.81)
    B = np.e**(A) - 1 

    mf = (thrusters.dry_mass+debris.mass)/B
    return mf 
def time_decay_manouver(
                debris:Debris,
                r=0, # position of the debris, if 0 then is avg_altitude
                ) ->tuple:

    if r==0:
        r = debris.avg_altitude

    final_radius = debris.Optimal_altitude() 
    velocity_initial = debris.get_velocity(r)
    acceleration  = thrusters.thrust/(debris.mass+thrusters.total_mass)
    velocity_final = V_cir(final_radius)

    time_manouver = abs((velocity_initial-velocity_final)/acceleration)

    return time_manouver, final_radius



# Starting program
if __name__ == "__main__":
    print('\033[92m',"INIZIO PROGRAMMA",'\033[0m') 
    start_time = time.process_time()

decayments_data = Logger(DECAYMENT_FILE)


# Values
ALL_DEBRIS = stages.values()


DVtot = 0
fuel_total = 0
for debris in ALL_DEBRIS:

    time_manouver, final_h = time_decay_manouver(debris,r=0)
    DV = abs(debris.get_velocity(r=0)-V_cir(final_h))
    DVtot += DV
    fuel = fuel_mass_thrusters(DV,debris)
    fuel_total += fuel

    if TOTAL_LOG:
        decayments_data.write_decayments(debris,thrusters,DV,time_manouver,final_h,fuel)
if TOTAL_LOG: 
    decayments_data.write_decayment_total(DVtot,fuel_total,thrusters)


# finish program

if __name__ == "__main__":

    end_time = time.process_time()
    crono = end_time-start_time

    print('\033[93m',"\n PROCESS TIME OF:")
    print(crono,"s","\t",
        crono/60,"min","\t",
        crono/60/60,"h","\033[0m")
    print('\033[92m',"FINE PROGRAMMA",'\033[0m')
