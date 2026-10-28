from astropy import units as u
from poliastro.bodies import Earth
import numpy as np
import time
import matplotlib.pyplot as plt
from Thrusters import SC_thruster
from Debris import Debris, stages
from input.INPUTS import R,K,MANOUVERS_FILE,TOTAL_LOG,ITERATIONS_PROGRAM,ITERATOR_OUTPUT_FILE,COMPUTATIONAL_TIMER_PATH
from Spacecraft import Spacecraft,spacecraft
import pandas as pd
from os import system
from Logger import Logger
from rendezvouz_manouver import rendezvous_manouver
import decayment_manouvers
from random import shuffle


# Starting program
if __name__ == COMPUTATIONAL_TIMER_PATH:
    print('\033[92m',"INIZIO PROGRAMMA",'\033[0m') 
    start_time = time.process_time()

# DATA

ALL_DEBRIS = stages.values()

if ITERATIONS_PROGRAM:
    ALL_DEBRIS = list(ALL_DEBRIS)
    shuffle(ALL_DEBRIS)

first_debris = list(ALL_DEBRIS)[0]
spacecraft.orbit.raan = first_debris.raan
spacecraft.orbit.i = first_debris.i
spacecraft.orbit.theta = first_debris.theta

rendez_dv_AUS  = []
rendez_t_AUS = []
t_AUS = []
dv_AUS = []

DV = []
time_manouvers = []
mission = Logger(MANOUVERS_FILE)
if TOTAL_LOG:
    mission._write_introduction(spacecraft)


for debris in ALL_DEBRIS:
    # if not ITERATIONS_PROGRAM:
    #     print(debris(), "\t ongoing...")
    dv_ausilio,tempo_ausilio = 0,0
    rendez_ausilio_dv, rendez_ausilio_t = 0,0
    dv,t =0,0
    if spacecraft.orbit.raan != debris.raan:

        dv,t = spacecraft.DV_raan_manouver(debris)
        DV.append(dv)
        time_manouvers.append(t)
        if TOTAL_LOG:
            mission.write_manouver_raan(spacecraft,debris,dv,t)
        for debris2 in ALL_DEBRIS:
            debris2.set_position_manouver(t)
        dv_ausilio+=dv
        tempo_ausilio += t

    if spacecraft.orbit.i != debris.i:
        dv,t = spacecraft.DV_inclination_manouver(debris)
        DV.append(dv)
        time_manouvers.append(t)
        if TOTAL_LOG:
            mission.write_manouver_i(spacecraft,debris,dv,t)
        for debris2 in ALL_DEBRIS:
            debris2.set_position_manouver(t)
        dv_ausilio+= dv

    if spacecraft.orbit.theta != debris.theta:
        dv,t,r = rendezvous_manouver(spacecraft,debris)
        DV.append(dv)
        time_manouvers.append(t)
        if TOTAL_LOG:
            mission.write_manouver_rendezvous(spacecraft,debris,dv,t,r)
        for debris2 in ALL_DEBRIS:
            debris2.set_position_manouver(t)
        rendez_ausilio_dv += dv
        rendez_ausilio_t += t

    if dv_ausilio!=0:
        dv_AUS.append(dv_ausilio)
    if rendez_ausilio_dv!=0:
        rendez_dv_AUS.append(rendez_ausilio_dv)
    if rendez_ausilio_t!=0:
        rendez_t_AUS.append(rendez_ausilio_t)
    if tempo_ausilio!=0:
        t_AUS.append(tempo_ausilio)

    print("\n",debris(),
          "\nDV", dv_ausilio,"\tt",tempo_ausilio/3600,"h",
          "\nrendezvous dv", rendez_ausilio_dv,"\tt", rendez_ausilio_t/3600/24,"d")


# print("\nMEAN DV", np.mean(dv_AUS),
#       "\n MEAN TIME", np.mean(t_AUS)/3600,
#       "\nRENDEZVOUZ MEAN DV", np.mean(rendez_dv_AUS),
#       "\nRENDEZVOUZ T", np.mean(rendez_t_AUS)/3600/24)


#final manouever
sc_decay_dv,sc_decay_t = spacecraft.decay_manouver()
DV.append(sc_decay_dv)
time_manouvers.append(sc_decay_t)
if TOTAL_LOG:
    mission.write_final_decay(sc_decay_dv,sc_decay_t)
    mission.write_final_data(sum(DV),sum(time_manouvers)/3600/24)

#final data
if ITERATIONS_PROGRAM:
    iterator_output_debris = Logger(ITERATOR_OUTPUT_FILE[0])
    iterator_output_dv = Logger(ITERATOR_OUTPUT_FILE[1])
    output_debris = [element() for element in ALL_DEBRIS]
    iterator_output_debris.write_partial_iterator_debris(output_debris)
    iterator_output_dv.write_partial_iterator_dv(sum(DV))




# finish program
if __name__ == COMPUTATIONAL_TIMER_PATH:
    end_time = time.process_time()
    crono = end_time-start_time
    print('\033[93m',"\n PROCESS TIME OF:")
    print(crono,"s","\t",
        crono/60,"min","\t",
        crono/60/60,"h","\033[0m")
    print('\033[92m',"FINE PROGRAMMA",'\033[0m')
