def calculatePrequired(R_eq, Q_eq, P_amb):
    """
    calculatePrequired is the function used to obtain the required pressure to extrude material through the equivalent flow resistance network
    characterized by the nozzles in parallel.

    Inputs:
        R_eq (numeric): Equivalent flow resistance
        Q_eq (numeric): Equivalent total flow rate
        P_amb (numeric): Ambient pressure

    Output:
        P (numeric): Required pressure
        
    Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
        %Date: June 13, 2020 - February 13, 2024
        
    """
    if isinstance(R_eq, (int, float)) and isinstance(Q_eq, (int, float)) and isinstance(P_amb, (int, float)):
        P = R_eq * Q_eq + P_amb
        return P
    else:
       raise ValueError("Inputs R_eq, Q_eq, and P_amb must be numeric.")
