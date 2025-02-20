#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def calculateReq(eta, L, D):
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
    if isinstance(eta, (list, np.ndarray)) and isinstance(L, (list, np.ndarray)) and isinstance(D, (list, np.ndarray)):
        Ri = (128 * L[0] * eta) / (np.pi * D[0] ** 4)
        R_eq = 1 / np.sum(1 / Ri)
        return R_eq, Ri
    else:
        raise ValueError("Inputs eta, L, and D must be numeric or array-like.")
