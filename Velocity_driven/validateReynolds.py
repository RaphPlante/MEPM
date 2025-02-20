#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def validateReynolds(rho, v, D, eta, debug_mode=False):
    """
    validateReynolds is the function used to validate whether a laminar flow
    is occurring in the nozzles of the robot. Upon validation, the Hagen-
    Poiseuille viscosity formulation may be used. If any of the flow rates are
    in the transition zone or turbulent, the function returns the position of
    nozzles having non-laminar flow.

    The output is the flow type: 0=laminar, 1=transition zone, 2=turbulent.
    pos is the position array of nozzles having non-laminar flow.
    Function valid only for the Extended Herschell-Bulkley, Herschell-Bulkley,
    Sisko, Ostwald-de-Waele, Bingham, and Newtonian models.

    Parameters:
    rho (array-like): Density of the fluid.
    v (array-like): Velocity of the fluid.
    D (array-like): Diameter of the nozzles.
    eta (array-like): Viscosity of the fluid.
    debug_mode (bool, optional): Debug mode flag. Default is False.

    Returns:
    typeEcoul (int): Type of flow - 0 for laminar, 1 for transition zone, 2 for turbulent.
    Re (numpy.ndarray): Reynolds number array for each nozzle.
    
    Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
        %Date: June 13, 2020 - February 13, 2024
    """

    if np.isscalar(rho) and np.isscalar(v) and np.isscalar(D) and np.isscalar(eta):
        if rho == 0:
            print('Reynolds validation is skipped since rho = 0. Update material database to activate Reynolds validation.')
            typeEcoul = 0
            Re = np.nan
        else:
            Re = rho * v * D / eta
            Re = Re / 1e6  # To render unitless, since rho is in kg/m³ and viscosity is in Pa.s (kg/m.s)

            if np.all(Re > 0) and np.all(Re < 100):  # Laminar
                typeEcoul = 0
                if debug_mode:
                    print('All flow rates are laminar')
            elif np.any((Re >= 100) & (Re <= 2500)):  # Transition
                typeEcoul = 1
                pos = np.where((Re >= 100) & (Re <= 2500))[0]
                print('The flow is in the transition zone for nozzles #', pos)
            elif np.any(Re > 2500):  # Turbulent
                typeEcoul = 2
                pos = np.where(Re > 2500)[0]
                print('The flow is turbulent for nozzles #', pos)
            else:  # Negative Re number
                typeEcoul = np.nan
                print('Reynolds is negative')
    else:
        raise ValueError("Inputs 'rho', 'v', 'D', and 'eta' must be scalar values.")

    return typeEcoul, Re
