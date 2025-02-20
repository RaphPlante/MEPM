#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np # type: ignore


def calculateQ(D, v):
    """
    calculateQ is the function used to obtain the volumetric flow rate through several nozzles.

    Inputs:
        D (array-like): Nozzle diameter array
        v (numeric): Desired speed for all nozzles array

    Outputs:
        Q (array-like): Flow rate array for each of the nozzles
        dQ (array-like): Change in flow rate for each of the nozzles
        Q_eq (numeric): Equivalent total flow rate

        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """

    v1 = v
    print(v)

    print(isinstance(D, (list, np.ndarray)))
    print(isinstance(v, (int, float)))
    print(len(D))
    # print(range(len(D[0, :])))
    # Q = np.zeros((len(v), len(D[0, :])))
    # dQ = np.zeros((len(v), len(D[0, :])))
    if isinstance(D, (list, np.ndarray)) and isinstance(v, (np.int64, float)):

        area = np.pi * 0.25 * D[0] ** 2
        Q = area * v
        dQ = np.pi * 0.5 * D[0] * D[1] * v
        Q_eq = np.sum(Q)
        return Q, dQ, Q_eq
    else:
        raise ValueError("Inputs D and v must be numeric or array-like.")
