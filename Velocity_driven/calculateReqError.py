#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def calculateReqError(R_eq, Ri, alpha, D, L, eta, deta):
    """
    calculateReqError is the function used to calculate the error in the equivalent hydraulic resistance.

    Inputs:
        R_eq (numeric): Equivalent hydraulic resistance
        Ri (array-like): Individual hydraulic resistance for each nozzle
        alpha (int): Number of nozzles
        D (array-like): Nozzle diameter array (2 x alpha)
        L (array-like): Nozzle length array (2 x alpha)
        eta (array-like): Apparent viscosity array (1 x alpha)
        deta (array-like): Error in apparent viscosity array (1 x alpha)

    Outputs:
        ReqError (numeric): Error in the equivalent hydraulic resistance
        dRi (array-like): Error in individual hydraulic resistance for each nozzle
        
        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """
    dRi = np.ones(alpha)
    sum_terms = np.zeros(alpha)

    for i in range(alpha):
        dRi[i] = (np.pi / 128) * (np.sum(1 / Ri) ** (-2)) * np.sqrt(((D[0, i] ** 2 / (eta[i] * L[0, i])) ** 4 * (L[0, i] * deta[i]) ** 2) +
                                                                      ((eta[i] * L[1, i]) ** 2) +
                                                                      16 * ((eta[i] * L[0, i] * D[1, i] / D[0, i])) ** 2)
        sum_terms[i] = (dRi[i] / Ri[i] ** 2) ** 2

    ReqError = R_eq ** 2 * np.sqrt(np.sum(sum_terms))

    return ReqError, dRi

