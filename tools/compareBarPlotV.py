#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
    %Date: June 13, 2020 - February 13, 2024"""

def compareBarPlotV(v_real, v_desired, dv_real, mode, i=None, myPlot=None):
    # Colors
    red = [0.8500, 0.3250, 0.0980]
    darkRed = [0.64, 0.08, 0.18]
    
    if mode == 'default':
        plt.rcdefaults()
    else:
        plt.rcParams.update({'text.usetex': True})
    
    if isinstance(v_real, (int, float)) and isinstance(v_desired, (int, float)):
        nozzleNumber = np.arange(1, len(v_real) + 1)
        
        if i is not None and myPlot is None:
            plt.figure(i + 3)
        
        # Plot desired speed line
        plt.plot([0, nozzleNumber[-1] + 1], [v_desired, v_desired], '--', linewidth=1.0, color='k')
        plt.hold(True)
        plt.plot([0, nozzleNumber[-1] + 1], [np.mean(v_real), np.mean(v_real)], '--', linewidth=1.0, color='r')
        
        # Bar plot
        plt.bar(nozzleNumber, v_real, width=0.2, color='b', linewidth=1.5)
        for j in range(len(v_real)):
            plt.text(nozzleNumber[j], v_real[j], str(round(v_real[j], 2)), va='bottom', ha='center', fontsize=12, color=red)
        
        # Error bars
        if dv_real != 0:
            plt.errorbar(nozzleNumber, v_real, yerr=dv_real, fmt='none', ecolor='k')
        
        # Appearance
        plt.minorticks_off()
        plt.tick_params(axis='both', which='major', labelsize=12)
        
        # Axis labels, legend
        plt.xlabel('Nozzle number', fontsize=12)
        plt.ylabel('Nozzle exit velocity [mm/s]', fontsize=12)
        plt.legend(['Desired velocity', 'Average velocity'], fontsize=10, loc='southeast')
        
        plt.hold(False)

"""# Example usage:
v_real = [10, 20, 30, 40]
v_desired = 25
dv_real = 1
mode = 'default'
i = 1
compareBarPlotV(v_real, v_desired, dv_real, mode, i)
plt.show()"""

