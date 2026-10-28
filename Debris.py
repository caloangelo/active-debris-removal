from astropy import units as u
from poliastro.bodies import Earth
import numpy as np
import time
import csv
import input.Analizer_csv as Analizer_csv
from input.Analizer_csv import stages
from Thrusters import thrusters
from input.INPUTS import FILE_TSV_num
from input.INPUTS import R,K




class Debris:

    def __init__(self, name, parameters:list) -> None:

        self.apogee = parameters[APOGEE]
        self.perigee = parameters[PERIGEE]
        self.avg_altitude = parameters[AVG_ALTITUDE]
        self.i = parameters[I]
        self.raan = parameters[RAAN]
        self.mass = parameters[MASS]
        self.area_on_mass = parameters[AREA_ON_MASS]
        self.argument_perigee = parameters[ARGUMENT_PERIGEE]
        self.true_anomaly = parameters[TRUE_ANOMALY]
        self.eccentricity = parameters[ECCENTRICITY]
        if parameters[ARGUMENT_PERIGEE]!=None and parameters[TRUE_ANOMALY]!=None:
            self.theta = parameters[ARGUMENT_PERIGEE]+parameters[TRUE_ANOMALY]
            if self.theta >= 360:
                self.theta -= 360
        else:
            self.theta = None
        self.cd = 1
        self.name = name

    def __call__(self) -> str:
        return self.name
    def get_velocity(self,r=0):
    

        if r==0:
            r = self.avg_altitude +R

        rp = self.perigee + R
        ra = self.apogee + R
        a = (rp+ra)/2
        v = np.sqrt(-K/a + 2*K/r)

        return v
    
    def Optimal_altitude(self):

        h = 8 #km
        H_fin = 0 #km
        pho0 = 1.225 #kg/m3
        Dt = 24*365*24*60*60 #24 years to seconds
        B = self.cd*(self.area_on_mass/100*(self.mass)/(self.mass+thrusters.dry_mass))
        C = np.sqrt(K*R) * B * pho0 /h 

        H0 = h*np.log(C*Dt+np.e**(H_fin/h))

        return H0
    
    def set_position_manouver(self,Dt):

        a  = self.avg_altitude +R
        P = 2*np.pi*np.sqrt((a**3)/K)
        n = 2*np.pi/P
       
        theta = self.theta + n*Dt
        theta = (theta-int(theta/360)*360)
        self.theta = theta

        return
    
    def Position(self,Dt,Theta0=0,OM_0=0):

        rp = self.perigee+R
        ra = self.apogee+R
        J2 = 0.001082
        a  = (ra+rp)/2
        e = self.eccentricity
        i = self.i

        P = 2*np.pi*np.sqrt((a**3)/K)

        n = 2*np.pi/P

        Theta = Theta0 + n*Dt
        r = a*(1-e**2 )/ (1+e*np.cos(Theta))

        OM_dot = -(3*n*J2*R**2) / ((2*a**2)*(1-e**2)**2) * np.cos(i)
        OM_deg_dot = OM_dot*180/np.pi
        OM = OM_0 + OM_deg_dot*Dt


        return r,Theta,OM
    
    def get_period(self):

        r = self.avg_altitude + R
        P = 2*np.pi*np.sqrt(r**3/K)

        return P



# Altitude (km),I (deg),RAAN (deg),Mass (kg),Span (m^2),Area/Mass ([m^2 / kg] x 100),,,,,Dry mass (kg),Isp (s)
if FILE_TSV_num==1:
    APOGEE,PERIGEE,AVG_ALTITUDE    ,ECCENTRICITY  = 0,1,2,3
    I     ,RAAN   ,ARGUMENT_PERIGEE,TRUE_ANOMALY  = 4,5,6,7
    MASS  ,AREA_ON_MASS         = 8,10

if FILE_TSV_num==2:  
    APOGEE,PERIGEE,AVG_ALTITUDE    ,ECCENTRICITY  = 0,1,2,3
    I     ,RAAN   ,ARGUMENT_PERIGEE,TRUE_ANOMALY  = 4,5,-1,-1
    MASS  ,AREA_ON_MASS         = 6,7

for key in stages:
    stages[key] = Debris(key,stages[key])

# print(stages)
# keys = stages.keys()
# for key in keys:
#     print(key)

"""
LIST DEBRIS:
N-2 R/B
ARIANE 40 R/B
SL-3 R/B
ATLAS F BURNER 2 R/B
CZ-4C R/B
ELECTRON KICK STAGE R/B
ARIANE 40 R/B(2)
IRS-P2 R/B
ARIANE 40 R/B(3)
ARIANE 40 R/B(4)

PARAMETERS:
DEBRIS,Apogee (km),Perigee (km),Average Altitude (km),
Eccentricity. e,I (deg),RAAN (deg),Argument of Perigee (deg),
True Anomaly (deg),Mass (kg),Span (m^2),Area/Mass ([m^2 / kg] x 100)

"""