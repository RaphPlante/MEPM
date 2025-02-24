from Velocity_driven import calculateQ, calculatePrequired, calculateReq, calculateReqError, calculateSR, calculateVisco, validateReynolds
from tools import printTableInConsole
import os
import sys
import numpy as np

# Add the MEPM directory to the Python path
mepm_path = r"C:\Users\anirb\OneDrive\Desktop\Additive Nozzle Manufacturing\CODE FOR MEPM"
sys.path.append(mepm_path)


def generateP(rho, v, D, L, n, K, eta_0, eta_inf, tau_0, lmbda, a, P_amb, debug_mode):
    """
    generateP function's purpose is to regroup all the necessary function calls in order to calculate the required pressure for a given material 
    and nozzle exit velocity. It validates the Reynold numbers. Finally, it returns the required Pressure along with Viscosities and Shear rates 
    arrays for plots.

    Inputs:
        rho (numeric): Density
        v (numeric): Nozzle exit velocity
        D (array-like): Nozzle diameter array along with the error for each diameter
        L (array-like): Nozzle length array along with the error for each length of nozzle
        n (numeric): Viscosity index
        K (numeric): Consistency index
        eta_0 (numeric): Rest-state viscosity
        eta_inf (numeric): Infinite viscosity
        tau_0 (numeric): Creep factor
        lmbda (numeric): Relaxation time
        a (numeric): Carreau model exponent
        P_amb (numeric): Ambient pressure
        debug_mode (bool): Flag for printing debug information

    Outputs:
        P (numeric): Required pressure
        eta (array-like): Viscosity array
        SR (array-like): Shear rate array
        Q (array-like): Flow rate array
        deta (array-like): Error in viscosity array
        dP (numeric): Error in required pressure
        dRi (array-like): Error in individual hydraulic resistance array
        dSR (array-like): Error in shear rate array

        Author: Jean-François Chauvette, Raphaël Plante
        Date: June 13, 2020 - February 13, 2024
    """

    print('------------------------------------------------------------------------------------------------')
    print(f'Desired nozzle exit speed (mm/s) = {v:.2f}\n')

    # Flows computation
    Q, dQ, Q_eq = calculateQ.calculateQ(D, v)

    if debug_mode:
        print(f'Total equivalent Q (mm³/s) = {Q_eq:.2f}')
        print('Volumetric flow rates (mm³/s):')
        printTableInConsole.printTableInConsole(Q)

    # Shear rate computation
    SR, dSR = calculateSR.calculateSR(Q, D, v)
    rabi = (3 + (1 / n)) / 4   # Weissenberg-Rabinowitsch correction
    SR = SR * rabi

    if debug_mode:
        print('Shear rates (1/s):')
        printTableInConsole.printTableInConsole(SR)

    # Viscosity computation
    eta, deta = calculateVisco.calculateVisco(
        SR, n, K, eta_inf, eta_0, tau_0, lmbda, a, debug_mode, dSR)

    if debug_mode:
        print('Viscosities (Pa.s):')
        printTableInConsole.printTableInConsole(eta)

    # Reynolds number hypothesis validation
    typeEcoul, Re = validateReynolds.validateReynolds(
        rho, v, D, eta, debug_mode)

    if debug_mode:
        print('Reynold numbers:')
        printTableInConsole.printTableInConsole(Re)

    if typeEcoul == 0:  # Laminar flow

        # Equivalent flow resistance computation
        R_eq, Ri = calculateReq.calculateReq(eta, L, D)
        R_eq = R_eq * rabi
        Ri = Ri * rabi
        R_eq_error, dRi = calculateReqError.calculateReqError(
            R_eq, Ri, D.shape[1], D, L, eta, deta)

        if debug_mode:
            print(f'Total equivalent R (Pa.s/mm³) = {R_eq:.2f}')
            print('Individual flow resistances (Pa.s/mm³):')
            printTableInConsole.printTableInConsole(Ri)

        # Required pressure computation
        P = calculatePrequired.calculatePrequired(R_eq, Q_eq, P_amb)
        dP = np.sqrt((R_eq_error * Q_eq)**2 + (R_eq * np.sum(dQ))**2)
        print(f'Required pressure (Pa) = {P:.0f}')
    else:  # Transition flow, turbulent flow or negative Reynolds
        P = np.nan
        eta = np.nan
        SR = np.nan
        Q = np.nan
        deta = np.nan
        dP = np.nan
        dRi = np.nan
        dSR = np.nan

    return P, eta, SR, Q, deta, dP, dRi, dSR
