#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def generateVreal(P, dP, Q, rho, v, D, L, n, K, eta_0, eta_inf, tau_0, lmbda, a, P_amb, debug_mode):
    """
    generateVreal function's purpose is to calculate the true nozzle exit velocity and recalculated flow rates
    for a given applied pressure and desired nozzle exit velocity. It iteratively calculates the flow rates until
    convergence is reached.

    Inputs:
        P (numeric): Applied pressure
        dP (numeric): Error in applied pressure
        Q (array-like): Flow rate array
        rho (numeric): Density
        v (numeric): Nozzle exit velocity
        D (array-like): Nozzle diameter array
        L (array-like): Nozzle length array
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
        v_real (array-like): Real nozzle exit velocities
        Q_real (array-like): Real nozzle exit flow rates
        dv_real (array-like): Error in real nozzle exit velocities
        Q_theo (array-like): Theoretical recalculated flow rates
        
        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """

    print('\n-------------------- True velocity calculation --------------------------')
    print(f'Desired nozzle exit speed (mm/s) = {v:.2f}')
    print(f'Real applied pressure (Pa) = {P:.0f}\n')

    Q_real = np.zeros(D.shape[1])  # Array of true recalculated flow rate
    eta_real = np.zeros(D.shape[1])  # Array of true recalculated shear rates
    Q_theo = np.zeros(D.shape[1])  # Array of theoretical recalculated flow rate
    dQ_crit = 10**-4  # Convergence criterion for true flow rate recalculation

    rabi = (3 + (1 / n)) / 4  # Rabinowitch correction

    for i in range(D.shape[1]):  # Iteration on all nozzle for a given P/v combination

        variation_Q = dQ_crit + 1  # Initializing a first dummy delta Q just to enter the while loop
        nbIter = 0  # Number of iteration needed for convergence
        Q_guess = Q[i]  # The initial Q guess = the previously desired Q for each nozzle (at desired input nozzle exit velocity)

        if debug_mode:
            print(f'Nozzle #{i+1} -----------------------')
            print(f'Starting Q_guess (mm³/s) = {Q_guess:.4f}')

        while variation_Q >= dQ_crit:  # Keep recalculating Q until it converges
            nbIter += 1
            if debug_mode:
                print(f'Iteration Velocity #{nbIter}')

            # Intermediate calculations
            SR_temp, _ = calculateSR(Q_guess, D[:, i], 0)  # Shear rate
            SR_temp = SR_temp * rabi
            eta_temp, deta_temp = calculateVisco(SR_temp, n, K, eta_inf, eta_0, tau_0, lmbda, a, debug_mode, 0)  # Viscosity
            _, Ri = calculateReq(eta_temp, L[:, i], D[:, i])  # Nozzle flow resistance
            Ri = Ri * rabi
            dRi = calculateReqError(0, Ri, 1, D[:, i], L[:, i], eta_temp, deta_temp)[1]
            Q_temp = (P - P_amb) / Ri  # Temporary Q for comparison with criterion
            dQ_temp = (dP / Ri)**2 + ((P - P_amb) * dRi / Ri**2)**2
            variation_Q = np.abs(Q_temp - Q_guess) / Q_guess  # Delta Q with previous guess
            Q_guess = Q_temp  # New Q guess

            if debug_mode:
                print(f'Q_temp_{nbIter} (mm³/s) = {Q_temp:.4f}')
                print(f'dQ_{nbIter} = {variation_Q:.8f}')

        Q_real[i] = Q_temp
        Q_theo[i] = (np.pi * n / (3 * n + 1)) * (D[0, i] / 2)**((1 + 3 * n) / n) * \
            ((P - P_amb + rho * 9.81 * L[0, i] / 1000) / (2 * K * L[0, i]))**(1 / n)  # calculates theoretical Q based on the big formula
        Q_guess_error = dQ_temp
        eta_real[i] = eta_temp

    v_real = Q_real / (0.25 * np.pi * D[0, :]**2)
    dv_real = ((Q_guess_error / (np.pi * 4 * D[0, :]**2))**2) + ((D[1, :] * Q_temp) / (np.pi * 4 * D[0, :]**3))**3

    print('Real nozzle exit velocities (mm/s):')
    printTableInConsole(v_real)

    print('Real nozzle exit flow rates (mm³/s):')
    printTableInConsole(Q_real)

    return v_real, Q_real, dv_real, Q_theo

