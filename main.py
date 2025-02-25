"""
**************************************************************************
 main script
 Last updated : 2025-02-24
**************************************************************************
 Description : General script that talks to other scripts, queries the database and interacts with the user. 
 Also provides user feedback.

 Instructions:
       This script must be used with the materialsDB.xls database.
       Follow the instructions in the Matlab console.

 Authors: Jean-François Chauvette, David Brzeski, Anirban, Raphaël Plante
 Date: 2020-05-29
**************************************************************************
"""

from Velocity_driven import generateP, calculateQ
from tools import readMaterial, comparePlotPV, comparePlotVisco, comparePlotQ
import numpy as np
import os
import sys
import openpyxl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import xlrd


# Constants
P_amb = 101325  # Ambient pressure [Pa]
alpha = 26  # Number of nozzles
debug_mode = True
graph_mode = 'S'  # Plotting mode
#     P = Pressure vs. Speed
#     V = Viscosity vs. Shear rate
#     S = Printing Speed vs. nozzle ID number
#     Q = Mass flow rate vs. printing speed


# Nozzle geometry
D = np.zeros((2, alpha))
D[0, :] = np.array([0.257193333, 0.25623, 0.25612, 0.256406667, 0.25561, 0.25561, 0.25612, 0.255536667, 0.255376667,
                    0.25357, 0.25459, 0.25561, 0.2551, 0.25663, 0.25459, 0.2551, 0.25255, 0.25408, 0.25357, 0.25459,
                    0.25816, 0.25459, 0.25663, 0.25765, 0.25714, 0.25459])
D[1, :] = np.ones(alpha) * 0.001  # Error on the nozzle diameters

# D = np.array([[0.257193333, 0.25623, 0.25612, 0.256406667, 0.25561, 0.25561, 0.25612, 0.255536667, 0.255376667,
#                0.25357, 0.25459, 0.25561, 0.2551, 0.25663, 0.25459, 0.2551, 0.25255, 0.25408, 0.25357, 0.25459,
#                0.25816, 0.25459, 0.25663, 0.25765, 0.25714, 0.25459],
#               [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001,
#                0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]])
# D[0, 6] = 1*D[0, 6]
# D = np.array([[np.ones(alpha)*0.250], [np.ones(alpha)*0.001]])
# diameter is clogged

D_avg = np.array([np.mean(D[0, :]), np.mean(D[1, :])]
                 )  # Average diameter and error
L = np.array([6.5, 0.01])  # Nozzle length and error

# Desired printing speed [mm/s]
v = np.array([50, 100, 150, 200, 250])


def open_material_file():
    """
    Opens a file explorer window to select the material database file (Excel).

    Returns:
        tuple: A tuple containing the selected file path or None if cancelled,
               and a list of material sheet names (if a file was chosen).
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls")])
    if filepath:
        workbook = xlrd.open_workbook(filepath)
        sheet_names = workbook.sheet_names()
        return filepath, sheet_names
    else:
        return None, None


if __name__ == "__main__":
    material_file_path, sheet_names = open_material_file()

    if material_file_path is None:
        print("User selected Cancel.")
    else:
        print(f"Opening: {material_file_path}...")


# User input for material selection
        while True:
            try:
                choices = [str(i) for i in range(
                    1, len(sheet_names) + 1)]  # 1-based indexing
                sheet_num_str = input(
                    "Choose a material number (1-{}): ".format(len(sheet_names)))
                # Convert to 0-based indexing for sheet access
                sheet_num = int(sheet_num_str) - 1
                if 0 <= sheet_num < len(sheet_names):
                    material = sheet_names[sheet_num]
                    break
                else:
                    print("Invalid material number. Please choose a number between 1 and {}.".format(
                        len(sheet_names)))
            except ValueError:
                print("Invalid input. Please enter a number.")

        print(f"User selected {material}")
        # Assuming you have a function to read data from specific sheet
        rho, w, f, n, K, eta_inf, eta_0, tau_0, lmbda, a = readMaterial.readMaterial(
            material_file_path, material)
        # Process or display retrieved data (replace with your logic)

        print("Retrieved material properties:")
        print(f"- Density: {rho}")
        print(f"- Weight fraction: {w}")
        # ... (add print statements for other properties)
        # Initialize arrays for results
        P = np.zeros(len(v))
        eta = np.zeros((len(v), alpha))
        SR = np.zeros((len(v), alpha))
        Q = np.zeros((len(v), alpha))
        dP = np.zeros((len(v), alpha))
        dRi = np.zeros((len(v), alpha))
        deta = np.zeros((len(v), alpha))
        dSR = np.zeros((len(v), alpha))

    # def compute_overall_p(v, rho, D_avg, L, n, K, eta_0, eta_inf, tau_0, lambda_, a, P_amb, debug_mode=False):
        """
        Computes overall pressure for each velocity in v and retrieves viscosity/shear rate data.

        Args:
            v (numpy.ndarray): Array of desired nozzle exit speeds.
            rho (float): Fluid density.
            D_avg (float): Average nozzle diameter.
            L (float): Nozzle length.
            n (float): Power law exponent.
            K (float): Consistency coefficient.
            eta_0 (float): Zero shear rate viscosity.
            eta_inf (float): Infinite shear rate viscosity.
            tau_0 (float): Characteristic relaxation time.
            lambda_ (float): Pressure coefficient.
            a (float): Shape factor.
            P_amb (float): Ambient pressure.
            debug_mode (bool, optional): Enable debug output (defaults to False).

        Returns:
            tuple: Tuple containing:
                - P (numpy.ndarray): Array of calculated overall pressures.
                - eta (numpy.ndarray): Array of viscosity values for each P/v combination.
                - SR (numpy.ndarray): Array of shear rate values for each P/v combination.
                - Q (numpy.ndarray): Array of mass flow rates for each P/v combination (optional, might depend on generateP).
                - dP (numpy.ndarray): Array of pressure derivatives (optional, might depend on generateP).
                - dRi (numpy.ndarray): Array of internal resistance derivatives (optional, might depend on generateP).
                - deta (numpy.ndarray): Array of viscosity derivatives (optional, might depend on generateP).
                - dSR (numpy.ndarray): Array of shear rate derivatives (optional, might depend on generateP).
        """

        for i in range(len(v)):
            try:
                newP, newEta, newSR, newQ, newdP, newdRi, newdEta, newdSR = generateP.generateP(
                    rho, v[i], D, L, n, K, eta_0, eta_inf, tau_0, lmbda, a, P_amb, debug_mode)
                P[i] = newP
                eta[i] = newEta
                SR[i] = newSR
                Q[i] = newQ
                dP[i] = newdP
                dRi[i] = newdRi
                deta[i] = newdEta
                dSR[i] = newdSR

            except ValueError as e:
                if str(e) == "Pressure could not be computed due to invalid Reynolds number":
                    print(e)
                else:
                    raise e  # Re-raise other ValueErrors

    # Return results (adjust based on generateP)
        # return P, eta, SR, Q, dP, dRi, deta, dSR

      # Compute P, eta, SR, and Q for each printing speed v
        # for i, speed in enumerate(v):
        #     # Compute P, eta, SR, and Q for the given speed and material properties
        #     # (Assuming the generateP function is implemented to calculate these values)
        #     # P[i], eta[i, :], SR[i, :], Q[i, :] = generateP(rho, speed, D_avg, L, n, K, eta_0, eta_inf, tau_0,
        #     #                                               lambda, a, P_amb, debug_mode)
        #     pass

       # Perform plotting based on graph_mode

        P = P/1000  # convert Pa to kPa and plot
        dP = dP/1000  # convert Pa to kPa and plot

        if 'P' in graph_mode:
            # Plot pressure vs. printing speed
            comparePlotPV.comparePlotPV(v, P)

        if 'V' in graph_mode:
            # Plot viscosity vs. shear rate for each nozzle
            comparePlotVisco.comparePlotVisco(np.mean(SR, 1), np.mean(eta, 1))

        if 'S' in graph_mode:
            # Plot printing exit velocity vs. nozzle ID number
            v_all = [v[0]]*26
            plt.bar(list(range(1, alpha+1)), v_all,
                    width=0.2, color='r', linewidth=1.5)
            plt.xlabel('Nozzle ID Number')
            plt.ylabel('Nozzle exit velocity (mm/s)')
            # plt.title('Printing pressure vs. Nozzle ID Number')
            plt.show()

        if 'Q' in graph_mode:
            # Plot mass flow rate vs. printing speed
            comparePlotQ.comparePlotQ(v, np.sum(Q, 1)*rho*1e-6)

else:
    print("Invalid material number.")
