#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def calculateVisco(SR, n, K, eta_inf, eta_0, tau_0, lmbda, a, debug_mode=False, dSR=None):
    """
    calculateVisco is the function used to obtain the apparent viscosity inside every nozzle,
    depending on the material's behavior law.

    Inputs:
        SR (array-like): Shear rate
        n (numeric): Viscosity index
        K (numeric): Consistency index
        eta_inf (numeric): Infinite viscosity
        eta_0 (numeric): Rest-state viscosity
        tau_0 (numeric): Creep factor
        lmbda (numeric): Relaxation time
        a (numeric): Carreau model exponent
        debug_mode (bool): Flag to print debug information
        dSR (array-like): Error in shear rate array

    Outputs:
        eta (array-like): Apparent viscosity array
        deta (array-like): Error in apparent viscosity array
        
        Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
            %Date: June 13, 2020 - February 13, 2024
    """
    dK = 0.1
    dn = 0.0001
    deta_inf = 0
    deta_0 = 0
    dlambda = 0
    da = 0
    dtau_0 = 0

    if isinstance(SR, np.ndarray) and isinstance(n, (int, float)) and isinstance(K, (int, float)) \
            and isinstance(eta_inf, (int, float)) and isinstance(eta_0, (int, float)) \
            and isinstance(tau_0, (int, float)) and isinstance(lmbda, (int, float)) \
            and isinstance(a, (int, float)):

        if n != 0 and K != 0 and eta_inf != 0 and eta_0 == 0 and tau_0 == 0 and lmbda == 0 and a == 0:
            eta = K * SR ** (n - 1) + eta_inf  # Sisko model
            deta = np.sqrt((SR ** (n - 1) * dK) ** 2 + (K * (n - 1) * SR ** (n - 2) * dSR) ** 2 +
                           (K * SR ** (n - 1) * np.log(SR) * dn) ** 2 + deta_inf ** 2)
            if debug_mode:
                print('Sisko model is used')
        elif n == 1 and K == 0 and eta_inf != 0 and eta_0 == 0 and tau_0 == 0 and lmbda == 0 and a == 0:
            eta = eta_inf * np.ones(SR.shape)  # Newtonian model
            deta = deta_inf * np.ones(SR.shape)
            if debug_mode:
                print('Newtonian model is used')
        elif n != 0 and K != 0 and eta_inf == 0 and eta_0 == 0 and tau_0 == 0 and lmbda == 0 and a == 0:
            eta = K * SR ** (n - 1)  # Pure power law model
            deta = np.sqrt((SR ** (n - 1) * dK) ** 2 + (K * (n - 1) * SR ** (n - 2) * dSR) ** 2 +
                           (K * SR ** (n - 1) * np.log(SR) * dn) ** 2)
            if debug_mode:
                print('Ostwald-de-Waele model (pure power law) is used')
        elif n != 0 and K == 0 and eta_inf != 0 and eta_0 != 0 and tau_0 == 0 and lmbda != 0 and a != 0:
            eta = eta_inf + (eta_0 - eta_inf) * (1 + (lmbda * SR) ** a) ** ((n - 1) / a)  # Carreau model
            ratio = 1 + (lmbda * SR) ** a
            deta1 = ((1 - ratio ** ((n - 1) / a)) * deta_inf) ** 2
            deta2 = (ratio ** ((n - 1) / a) * deta_0) ** 2
            deta3 = ((eta_0 - eta_inf) * ratio ** ((n - 1 - a) / a) * (n - 1) * (lmbda * SR) ** (a - 1) * SR * dlambda) ** 2
            deta4 = ((eta_0 - eta_inf) * ratio ** ((n - 1 - a) / a) * (n - 1) * (lmbda * SR) ** (a - 1) * lmbda * dSR) ** 2
            deta5 = ((eta_0 - eta_inf) * (n - 1) * ratio / a * ((lmbda * SR) ** a * (np.log(lmbda * SR)) / (1 + (lmbda * SR) ** a) - np.log(ratio) / a) * da) ** 2
            deta = np.sqrt(deta1 + deta2 + deta3 + deta4 + deta5)
            if debug_mode:
                print('Carreau model is used')
        elif n == 1 and K == 0 and eta_inf != 0 and eta_0 == 0 and tau_0 != 0 and lmbda == 0 and a == 0:
            eta = tau_0 / SR + eta_inf  # Bingham model
            deta = np.sqrt((dtau_0 / SR) ** 2 + (tau_0 * dSR / SR ** 2) ** 2 + (deta_inf) ** 2)
            if debug_mode:
                print('Bingham model is used')
        elif n != 0 and K != 0 and eta_inf != 0 and eta_0 == 0 and tau_0 != 0 and lmbda == 0 and a == 0:
            eta = tau_0 / SR + K * SR ** (n - 1) + eta_inf  # Herschell-Bulkley extended model
            deta = np.sqrt((dtau_0 / SR) ** 2 + (SR ** (n - 1) * dK) ** 2 + deta_inf ** 2 +
                           ((n - 1) * K * SR ** (n - 1) + tau_0 / SR ** 2) * dSR + K * SR ** (n - 1) * np.log(SR) * dn)
            if debug_mode:
                print('Herschell-Bulkley extended model is used')
        elif n != 0 and K != 0 and eta_inf == 0 and eta_0 == 0 and tau_0 != 0 and lmbda == 0 and a == 0:
            eta = tau_0 / SR + K * SR ** (n - 1)  # Herschell-Bulkley model
            deta = np.sqrt((dtau_0 / SR) ** 2 + (SR ** (n - 1) * dK) ** 2 +
                           ((n - 1) * K * SR ** (n - 1) + tau_0 / SR ** 2) * dSR + K * SR ** (n - 1) * np.log(SR) * dn)
            if debug_mode:
                print('Herschell-Bulkley model is used')
        else:
            raise ValueError('No model was found for your material')

        return eta, deta

    else:
        raise ValueError('Inputs SR, n, K, eta_inf, eta_0, tau_0, lmbda, and a must be numeric.')
