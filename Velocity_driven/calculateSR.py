#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def calculateSR(Q, D, v):
    """
    calculateSR is the function used to obtain the shear rate inside multiple nozzles.

    Inputs:
        Q (array-like): Flow rate array
        D (array-like): Nozzle diameter array
        v (numeric): Desired speed for all nozzles

    Outputs:
        SR (array-like): Shear rate array
        dSR (array-like): Change in shear rate array
        
        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """
    if isinstance(Q, np.ndarray) and isinstance(D, np.ndarray):
        SR = 32 * Q / (np.pi * D[0] ** 3)
        dSR = 8 * v * D[1] / D[0] ** 2
        return SR, dSR
    else:
        raise ValueError("Inputs Q and D must be NumPy arrays.")


