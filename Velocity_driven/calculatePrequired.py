import numpy as np


def calculatePrequired(R_eq, Q_eq, P_amb, n, mP, Noz_type):
    """
    calculatePrequired is the function used to obtain the required pressure to extrude material through the equivalent flow resistance network
    characterized by the nozzles in parallel.

    Inputs:
        R_eq (numeric): Equivalent flow resistance (scalar)
        Q_eq (numeric): Equivalent total flow rate (scalar)
        P_amb (numeric): Ambient pressure (scalar)

    Output:
        P (numeric): Required pressure

    Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
        %Date: June 13, 2020 - February 13, 2024

    """
    if isinstance(P_amb, (int, float)):  # and isinstance(R_eq, (int, float)) and isinstance(Q_eq, (int, float)) :
        if Noz_type == "tapered":

            if mP != 0:
                print(f'R_eq moyen (Pa) = {np.mean(R_eq)}')
                print(f'Q_eq moyen (Pa) = {np.mean(Q_eq)}')
                P = (np.mean(R_eq) * (np.mean(Q_eq))**mP)*10**6  # + P_amb
                print(f'Required pressure (Pa) = {P}')
            else:
                # Weissenberg-Rabinowitsch correction
                rabi = (3 + (1 / n)) / 4
                P = np.mean(R_eq) * (np.mean(Q_eq))**n + P_amb
                print(f'Required pressure (Pa) = {P}')
        else:
            P = R_eq * Q_eq + P_amb
        return P
    else:
        raise ValueError("Inputs R_eq, Q_eq, and P_amb must be numeric.")
