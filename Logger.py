from Debris import Debris
from Spacecraft import Spacecraft
from Thrusters import Thrusters
class Logger:

    _decayment_introduction = False
    _introduction = False

    def __init__(self, file_name):

        self.file_name = file_name
        self.manouver_number = 0


    def _write_introduction(self,spacecraft):
 
        if not Logger._introduction:
            with open(self.file_name, 'w') as file:
                file.write(f"SPACECRAFT STATE:")
                file.write(f"""
\t avg altitude:{spacecraft.orbit.avg_altitude}\t theta angle:{spacecraft.orbit.theta}
\t inclination:{spacecraft.orbit.i}\t RAAN:{spacecraft.orbit.raan}
\t total mass:{spacecraft.total_mass}\n""")
                
                file.write("-" * 40 + "\n")
            Logger._introduction = True  



    def write_manouver_raan(self,spacecraft:Spacecraft,debris:Debris,dv,t):

        self.manouver_number += 1

        with open(self.file_name, 'a') as file:

            file.write(f"MANOUVER NUMBER: {self.manouver_number}\n")
            file.write(f"RAAN MANOUVER to {debris()}\n")
            file.write(f"\t debris RAAN: {debris.raan} \n")
            file.write(f"\t DV: {dv} km/s \t time used: {t/86400} days\n\n")
            file.write(f"SPACECRAFT STATE AFTER MANOUVER:")
            file.write(f"""
\t avg altitude:{spacecraft.orbit.avg_altitude}\t theta angle:{spacecraft.orbit.theta}
\t inclination:{spacecraft.orbit.i}\t RAAN:{spacecraft.orbit.raan}
\t total mass:{spacecraft.total_mass}\n""")
            
            file.write("\n\n"+"-" * 40 + "\n")



    def write_manouver_i(self,spacecraft:Spacecraft,debris:Debris,dv,t):

        self.manouver_number += 1


        with open(self.file_name, 'a') as file:

            file.write(f"MANOUVER NUMBER: {self.manouver_number}\n")
            file.write(f"INCLINATION MANOUVER to {debris()}\n")
            file.write(f"\t debris inclination: {debris.i} \n")
            file.write(f"\t DV: {dv} km/s \t time used: {t/86400} days\n\n")
            file.write(f"SPACECRAFT STATE AFTER MANOUVER:")
            file.write(f"""
\t avg altitude:{spacecraft.orbit.avg_altitude}\t theta angle:{spacecraft.orbit.theta}
\t inclination:{spacecraft.orbit.i}\t RAAN:{spacecraft.orbit.raan}
\t total mass:{spacecraft.total_mass}\n""")
            file.write("\n\n"+"-" * 40 + "\n")



    def write_manouver_rendezvous(self,spacecraft:Spacecraft,debris:Debris,dv,t,r):

        self.manouver_number += 1


        with open(self.file_name, 'a') as file:

            file.write(f"MANOUVER NUMBER: {self.manouver_number}\n")
            file.write(f"RENDEZVOUS MANOUVER to {debris()}\n")
            file.write(f"\t avg altitude:{debris.avg_altitude}\t theta angle:{debris.theta} \n")
            file.write(f"\t parking orbit:{r}\n")
            file.write(f"\t DV: {dv} km/s \t time used: {t/86400} days\n\n")
            file.write(f"SPACECRAFT STATE AFTER MANOUVER:")
            file.write(f"""
\t avg altitude:{spacecraft.orbit.avg_altitude}\t theta angle:{spacecraft.orbit.theta}
\t inclination:{spacecraft.orbit.i}\t RAAN:{spacecraft.orbit.raan}
\t total mass:{spacecraft.total_mass}\n
""")
            file.write("\n\n"+"-" * 40 + "\n")



    def write_decayments(
        self,
        debris:Debris,
        thrusters:Thrusters,
        DV,
        time_manouver,
        final_h,
        fuel):

        if self._decayment_introduction == False:
             
            with open(self.file_name, 'w') as file:

                file.write("DEBRIS DECAYMENT DATA \n\n")
                self._decayment_introduction = True



        with open(self.file_name, 'a') as file:

            file.write(debris()+'\n')
            file.write("time decay active manouver: "+str(time_manouver/60/60/24)+'days\n')
            file.write("initial altitude: "+str(debris.avg_altitude)+'km \t final altitude: '+str(final_h)+'km\n')
            file.write("DV: "+ str(DV)+'\n')
            file.write("Mass of debris: "+str(debris.mass+thrusters.dry_mass)+'kg\n')
            # file.write("Fuel consumption: "+str(fuel)+ "\t msTOT/mf = "+str((thrusters.dry_mass+debris.mass)/fuel)+'\n')
            file.write("\n\n"+"-" * 40 + "\n")

    def write_decayment_total(
        self,
        DVtot,
        fuel_total,
        thrusters:Thrusters):
            

        with open(self.file_name, 'a') as file:
    
            file.write("\nTOTAL DV OF DEBRIS DECAYMENT SYSTEM: "+str(DVtot)+' km/s\n')
            # file.write("TOTAL FUEL CONSUMPTION: "+ str(fuel_total)+'\n')
            file.write("AVERAGE DV FOR EACH THRUSTER: "+ str(DVtot/thrusters.number_debris)+' km/s\n')
            # file.write("AVERAGE FUEL CONSUMPTION FOR EACH THRUSTER: "+str(fuel_total/10)+'\n')


    def write_final_decay(self,dv,t):

        with open(self.file_name, 'a') as file:

            file.write(f"LAST MANOUVER: spacecraft decayment\n")
            file.write(f"\t DV: {dv} km/s \t time used: {t/86400} days\n\n")
            file.write("\n\n"+"-" * 40 + "\n")


    def write_final_data(
        self,
        DVtot,
        t_tot):
            

        with open(self.file_name, 'a') as file:
    
            file.write(f"\n\nTOTAL DV: {DVtot} km/s  Total time of the mission: {t_tot} days\n")


    def write_partial_iterator_debris(
        self,
        lista):
            

        with open(self.file_name, 'a') as file:
    
            file.write(f"pattern: {lista}\n")

    def write_partial_iterator_dv(
        self,
        dv):
            

        with open(self.file_name, 'a') as file:
    
            file.write(f"{dv}\n")

    



    def read_log(self):

        with open(self.file_name, 'r') as file:
            print(file.read())


