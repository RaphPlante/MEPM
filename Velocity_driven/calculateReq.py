import numpy as np


def calculateReq(eta, theta, K, n, L, D, Noz_type, R):
    """
    calculateReq is the function used to obtain the equivalent hydraulic
    resistance of several nozzles in parallel.

    Inputs:
        eta (array-like): Apparent viscosity array
        L (array-like): Nozzle length array
        D (array-like): Nozzle diameter array

    Outputs:
        R_eq (numeric): Equivalent hydraulic resistance
        Ri (array-like): Individual hydraulic resistance for each nozzle

        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """
    eta = np.array(eta)
    L = np.array(L)
    D = np.array(D)

    if isinstance(eta, np.ndarray) and isinstance(L, np.ndarray) and isinstance(D, np.ndarray):
        if len(eta) != D.shape[1]:
            raise ValueError(" Inputs eta, L and D must have the same length.")
        # if D.shape[0] != 2:
        #     raise ValueError(" Input D must be a matrix with 2 columns.")
        if Noz_type == "tapered":
            # Extract diameters from the first column of D
            if R != 0:
                Ri = R*np.ones(len(eta))
                R_eq = Ri
            else:

                De = D[0, :]  # outlet diamter
                Do = D[2, :]  # inlet diameter

                # Ri = (2*K*(De**(3*n)-Do**(3*n))/(3*n*np.tan(theta)
                #                                  )) * (((32)/(np.pi * Do**3 * De**3))**n)
                Ri = ((4*K*L[0])/(3*n*(Do-De))) * ((3*n+1)/(n*np.pi)
                                                   ** n) * ((De/2)**(-3*n)-(Do/2)**(-3*n))

                # Calculate equivalent hydraulic resistance for nozzles in parallel

                R_eq = Ri
            # R_eq = 1/np.sum(1/Ri)
        else:

            # Extract diameters from the first column of D
            diameters = D[0, :]

            # Calculate individual hydraulic resistance for each nozzle
            Ri = (128*L[0]*eta)/(np.pi*diameters**4)

            # Calculate equivalent hydraulic resistance for nozzles in parallel
            R_eq = 1/np.sum(1/Ri)
            rabi = (3 + (1 / n)) / 4   # Weissenberg-Rabinowitsch correction
            R_eq = R_eq * rabi
            Ri = Ri * rabi

        return R_eq, Ri
