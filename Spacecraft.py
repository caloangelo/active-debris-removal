import numpy as np
from input.INPUTS import R,K
from Thrusters import SC_thruster
from Debris import Debris

class Spacecraft:

    def __init__(self) -> None:

        # self.area_on_mass = 1
        self.Cd = 1
        self.dry_mass = 8540
        self.total_mass = self.dry_mass + SC_thruster.fuel_mass
        self.area = 100 
        self.area_on_mass = self.area / self.total_mass
        self.orbit = SpacecraftOrbit()
        self.parking_orbit = SpacecraftOrbit()

    def rad(self,n):
        return n*np.pi/180
    def deg(self,n):
        return n/np.pi*180

    
    def get_velocity(self,r=0):


        if r==0:
            r = self.orbit.avg_altitude +R


        a =  self.orbit.avg_altitude + R
        v = np.sqrt(-K/a + 2*K/r)

        return v
    
    def fuel_Tsiolkowski(self,DV):
    
        A = np.e**(DV*1000/(SC_thruster.Isp * 9.81))
        mf = (self.total_mass)*(A-1)/A
        

        return mf 
    
    def set_position_manouver(self,Dt):

        a  = self.orbit.avg_altitude + R
        P = 2*np.pi*np.sqrt((a**3)/K)
        n = 2*np.pi/P
       
        theta = self.orbit.theta + n*Dt
        theta = (theta-int(theta/360)*360)
        self.orbit.theta = theta

        return 
    
    def get_period(self,r):

        P = 2*np.pi*np.sqrt(r**3/K)
     
        return P

    def DV_raan_manouver(self,debris:Debris):

        a_sc = self.orbit.avg_altitude + R 
        A = np.pi/2*np.sqrt(K/a_sc)
        D_OM = abs(self.rad(self.orbit.raan - debris.raan))
        i = self.rad(self.orbit.i)
        DV = A * abs(np.sin(i)) * D_OM

        self.orbit.raan = debris.raan
        self.total_mass -= self.fuel_Tsiolkowski(DV)
        
        time_manouver = DV/(SC_thruster.thrust/self.total_mass)



        self.set_position_manouver(time_manouver)
        

        return DV,time_manouver
    
    def DV_inclination_manouver(self,debris:Debris):

        D_i = self.rad(self.orbit.i - debris.i)
        v = self.get_velocity()
        
        DV = v * np.sqrt( 2-2*np.cos(np.pi*D_i))

        self.orbit.i = debris.i
        self.total_mass -= self.fuel_Tsiolkowski(DV)
        time_manouver = DV/(SC_thruster.thrust/self.total_mass)
        self.set_position_manouver(time_manouver)
        

        return DV,time_manouver

    def Optimal_altitude_SC(self):

        h = 8 #km
        H_fin = 0 #km
        pho0 = 1.225 #kg/m3
        Dt = 24*365*24*60*60 #24 years to seconds
        B = self.Cd*(self.area_on_mass/100*(self.total_mass)/(self.total_mass))
        C = np.sqrt(K*R) * B * pho0 /h 

        H0 = h*np.log(C*Dt+np.e**(H_fin/h))

        return H0
    
    def decay_manouver(
        self,
        r=0, # position of the spacecraft, if 0 then is avg_altitude
        ) ->tuple:

        if r==0:
            r = self.orbit.avg_altitude + R

        final_radius = self.Optimal_altitude_SC() + R
        velocity_initial = self.get_velocity()
        acceleration  = SC_thruster.thrust/(self.total_mass)
        velocity_final = np.sqrt(K/(final_radius))
        DV = abs((velocity_initial-velocity_final))
        time_manouver = abs((velocity_initial-velocity_final)/acceleration)

        return DV,time_manouver



        
    
class SpacecraftOrbit:

    def __init__(self) -> None:

        self.apogee = 751.5
        self.perigee = 751.5
        self.avg_altitude = 751.5
        self.i = 98.28
        self.raan = 326
        self.mass = 2000
        # self.area_on_mass = 0.6859410431
        self.argument_perigee = 228.3
        self.true_anomaly = 100.8
        self.eccentricity = 0.0002204
        if self.argument_perigee!=None and self.true_anomaly!=None:
            self.theta = self.argument_perigee + self.true_anomaly
        else:
            self.theta = None

    def get_period(self):

        r = self.avg_altitude + R
        P = 2*np.pi*np.sqrt(r**3/K)

        return P
    
    





        
        

spacecraft = Spacecraft()

