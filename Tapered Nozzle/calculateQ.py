import numpy as np

def calculateQ(D, v):
    """
    calculateQ is the function used to obtain the volumetric flow rate through several nozzles.

    Inputs:
        D (array-like): Nozzle diameter array (alpha x 3) ID;OD;Error
        v (numeric): Desired speed for all nozzles

    Outputs:
        Q (array-like): Flow rate array for each of the nozzles
        dQ (array-like): Change in flow rate for each of the nozzles
        Q_eq (numeric): Equivalent total flow rate

        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """
    # Ensure inputs are valid
    if D.ndim != 3:
        raise ValueError("Input array D must be 2-dimensional")
    if not (isinstance(D, (list, np.ndarray))): #and isinstance(v, (int, float))):
        raise ValueError("Inputs D and v must be numeric or array-like.")
    
    if isinstance(D, list):
        D = np.array(D)


    alpha = D.shape[1]

    # Initialize arrays for Q and dQ
    Q = np.empty(alpha)
    dQ = np.empty(alpha)

    for i in range(alpha):
         area = np.pi * 0.25 * D[0,i] ** 2  # Calculate cross-sectional area of the nozzle exit diameter
         Q[i] = area * v  # Calculate flow rate for each nozzle
         dQ[i] = np.pi * 0.5 * D[0,i] * D[2,i] * v  # Calculate change in flow rate for each nozzle

    Q_eq = np.sum(Q)  # Calculate the equivalent total flow rate
    return Q, dQ, Q_eq 