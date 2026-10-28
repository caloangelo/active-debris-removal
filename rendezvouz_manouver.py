import numpy as np
from Thrusters import SC_thruster,thrusters
from Debris import Debris
from input.INPUTS import R,K,DEBRIS_RENDEZVOUS_DATA,RENDEZVOUS_DATA_PATH,TOTAL_LOG,ARBITRARY_THETA
from Spacecraft import Spacecraft
import pandas as pd
import re
import math
from typing import Tuple



def rendezvous_manouver(spacecraft: "Spacecraft", debris: "Debris") -> Tuple[float, float, float]:
    """
    Perform a rendezvous maneuver between a spacecraft and debris.
    
    This function simulates the orbital adjustments needed for a spacecraft
    to rendezvous with a target debris by adjusting its orbital radius until
    the orbital periods nearly match, and then waiting for proper phase alignment.
    
    Args:
        spacecraft (Spacecraft): The spacecraft performing the maneuver.
        debris (Debris): The target debris.
    
    Returns:
        Tuple[float, float, float]: A tuple containing:
            - DV: The total Delta-V required for the maneuver.
            - final_time: The final simulation time at the end of the maneuver.
            - altitude_difference: The difference between the target radius and Earth’s radius.
    """

    GIRI_SC = 0
    GIRI_D = 0

    Time = [0.0]
    Theta_SC = [spacecraft.orbit.theta]  # degrees
    Theta_d = [debris.theta]             # degrees

    # Compute the initial angular difference normalized to [-180, 180]
    init_dtheta = Theta_SC[-1] - Theta_d[-1]
    if abs(init_dtheta) >= 180:
        init_dtheta = init_dtheta + 360 if init_dtheta < 0 else init_dtheta - 360
    D_Theta = [init_dtheta]
    D_Period = []  # Difference in periods (SC period - debris period)
    D_R = []       # Difference in radii (SC radius - debris radius)

    def update_position(dt: float, n_SC: float, n_d: float, 
                        r_SC: float, r_d: float, 
                        Period_SC: float, Period_d: float) -> None:
        """
        Update the spacecraft and debris positions and record the differences.
        
        Args:
            dt (float): The time step.
            n_SC (float): Spacecraft angular velocity (rad/time).
            n_d (float): Debris angular velocity (rad/time).
            r_SC (float): Spacecraft orbital radius.
            r_d (float): Debris orbital radius.
            Period_SC (float): Spacecraft orbital period.
            Period_d (float): Debris orbital period.
        """
        nonlocal GIRI_SC, GIRI_D

        # Compute new angles in degrees
        total_angle_sc = Theta_SC[-1] + math.degrees(n_SC * dt)
        total_angle_d = Theta_d[-1] + math.degrees(n_d * dt)
        
        # Calculate full rotations (integer part)
        full_rotations_sc = int(total_angle_sc // 360)
        full_rotations_d = int(total_angle_d // 360)
        
        # Get angles modulo 360
        new_theta_sc = total_angle_sc - full_rotations_sc * 360
        new_theta_d = total_angle_d - full_rotations_d * 360
        
        # Update revolution counters if a full rotation occurred
        if full_rotations_sc >= 1:
            GIRI_SC += full_rotations_sc
        if full_rotations_d >= 1:
            GIRI_D += full_rotations_d
        
        Theta_SC.append(new_theta_sc)
        Theta_d.append(new_theta_d)
        
        # Compute and normalize the angular difference to [-180, 180]
        d_theta = new_theta_sc - new_theta_d
        if abs(d_theta) >= 180:
            d_theta = d_theta + 360 if d_theta < 0 else d_theta - 360
        D_Theta.append(d_theta)
        
        # Record period and radius differences
        D_Period.append(Period_SC - Period_d)
        D_R.append(r_SC - r_d)

    # Set up initial orbital parameters
    Period_d = debris.get_period()
    Period_SC = spacecraft.orbit.get_period()
    
    # Determine target period using an arbitrary phase correction
    if D_Theta[-1] > 0:
        d_Dtheta_arbitrary = -math.radians(ARBITRARY_THETA)
    else:
        d_Dtheta_arbitrary = math.radians(ARBITRARY_THETA)
    Period_target = (1 - d_Dtheta_arbitrary / (2 * np.pi)) * Period_d
    
    # Angular velocity of debris.
    n_d = 2 * np.pi / Period_d

    # Calculate the target orbital radius from Kepler’s law
    radius_target = ((math.sqrt(K) * Period_target / (2 * np.pi)) ** (2 / 3))
    
    # Initial orbital radii 
    r_SC = spacecraft.orbit.avg_altitude + R
    r_d = debris.avg_altitude + R
    D_R.append(r_SC - r_d)
    
    # Simulation parameters.
    dt = 0.4
    eps = 1 / 100
    speed_up = True if Period_target < Period_SC else False
    time_restart_manouver = 0.0
    condition_transfer = True
    waiting = True


    # Main simulation loop
    while condition_transfer or waiting:
        # Increment simulation time
        current_time = Time[-1] + dt
        Time.append(current_time)
        
        # Compute acceleration from thruster
        acc = SC_thruster.thrust / spacecraft.total_mass
        
        # Compute change in spacecraft radius
        dr = 2 * acc * np.sqrt((r_SC ** 3 / K)) * dt
        
        # Adjust the spacecraft orbital radius based on maneuver direction
        r_SC = r_SC - dr if speed_up else r_SC + dr
        
        # Update the spacecraft's orbital period and angular velocity
        Period_SC = spacecraft.get_period(r_SC)
        n_SC = 2 * np.pi / Period_SC

        
        # Update positions and angles
        update_position(dt, n_SC, n_d, r_SC, r_d, Period_SC, Period_d)

        # Check if we have nearly reached the target period and are in the waiting phase
        safety_condition = Period_SC - Period_target < 0 if speed_up else Period_SC - Period_target > 0

        if abs(Period_SC - Period_target) <= eps*Period_target and waiting and safety_condition:

            tf_manouver = Time[-1]
            # Jump ahead in time to reduce computation (based on the phase difference)
            d_Dtheta_arbitrary = abs(2*np.pi - n_SC * Period_d)
            t_jump = abs((math.radians(D_Theta[-1]) / d_Dtheta_arbitrary) * Period_d)
            t_jump = t_jump * 0.95 # avoiding jumping too much for simuilation stability
            current_time += t_jump
            Time.append(current_time)
            update_position(t_jump, n_SC, n_d, r_SC, r_d, Period_SC, Period_d)


            # WAITING PHASE: wait until the angular difference is within tolerance
            while abs(D_Theta[-1]) >= eps:
                current_time += dt
                Time.append(current_time)
                update_position(dt, n_SC, n_d, r_SC, r_d, Period_SC, Period_d)
                
            time_waiting_phase = Time[-1]
            # Additional waiting phase to synchronize for catch-up
            while Time[-1] < time_waiting_phase + tf_manouver:
                current_time += dt
                Time.append(current_time)
                update_position(dt, n_SC, n_d, r_SC, r_d, Period_SC, Period_d)
                time_restart_manouver = Time[-1]
            
            # Switch maneuver phase based on the relative radii
            speed_up = False if r_SC <= r_d else True
            waiting = False

        # Continue transfer until the spacecraft radius is close enough to the debris radius
        condition_transfer = abs(r_SC - r_d) >= dr * 2
        
        # Safety check for abnormal orbit radii
        if r_SC > 8000 or r_SC < R:
            error_mex = "impact on Earth" if r_SC < R else "tend to infinity"
            raise ValueError("spacecraft radius exceed normal values: " + error_mex)

        
            

    # Finalize the results
    final_time = Time[-1]
    total_time_manouvers = (final_time - time_restart_manouver) + tf_manouver
    DV = acc * total_time_manouvers
    
    # Update spacecraft data after rendezvous
    spacecraft.total_mass -= thrusters.total_mass
    spacecraft.total_mass -= spacecraft.fuel_Tsiolkowski(DV)
    spacecraft.orbit.avg_altitude = debris.avg_altitude
    spacecraft.orbit.theta = debris.theta
    
    # Optionally, log the rendezvous data if enabled
    if DEBRIS_RENDEZVOUS_DATA and TOTAL_LOG:
        data = {
            'time': Time,
            'D_Theta': D_Theta,
            'D_R': D_R
        }
        df = pd.DataFrame(data)
        filename = RENDEZVOUS_DATA_PATH + re.sub(r'\W+', '_', str(debris)) + '.csv'
        df.to_csv(filename, index=False)
    
    return DV, final_time, radius_target - R


