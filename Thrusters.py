
class Thrusters:
    def __init__(self,thrust,Isp,dry_mass=0,acc=None,number_debris=10,fuel_mass=0) -> None:
        
        self.thrust = thrust
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.total_mass = self.dry_mass+self.fuel_mass
        self.Isp = Isp
        self.acc = acc
        self.number_debris = number_debris

thrusters = Thrusters(thrust=0.449, #N
                      dry_mass = 525,  #kg
                      fuel_mass = 0,#kg
                      Isp = 2210, #s
                      )

SC_thruster = Thrusters(thrust=1.35, #N
                      fuel_mass = 0,#kg
                      Isp = 3000, #s
                      )