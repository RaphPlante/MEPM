#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
    %Date: June 13, 2020 - February 13, 2024"""

def comparePlotVisco(SR_model, eta_model, SR_literature, eta_literature, x_lim, y_lim, deta, dSR, mode, i=None, myPlot=None):
    # Colors
    blue = [0, 0.4470, 0.7410]
    red = [0.8500, 0.3250, 0.0980]
    
    if mode == 'default':
        plt.rcdefaults()
    else:
        plt.rcParams.update({'text.usetex': True})
    
    if isinstance(eta_model, (int, float)) and isinstance(SR_model, (int, float)) and isinstance(eta_literature, (int, float)) and isinstance(SR_literature, (int, float)):
        
        if myPlot is None:
            plt.figure(i + 2)
        
        # Plot data and labels
        if np.any(eta_model):
            plt.loglog(SR_model, eta_model, '-s', linewidth=1.5, color=red)
            t_model = [plt.text(SR_model[i], eta_model[i], str(round(eta_model[i], 2)), verticalalignment='bottom', horizontalalignment='left', fontsize=12) for i in range(len(eta_model))]
        
        if np.any(eta_literature):
            plt.loglog(SR_literature, eta_literature, '-s', linewidth=1.5, color=blue)
            t_lit = [plt.text(SR_literature[i], eta_literature[i], str(round(eta_literature[i], 2)), verticalalignment='top', horizontalalignment='right', fontsize=12) for i in range(len(eta_literature))]
        
        # Error bars
        if deta != 0:
            plt.errorbar(SR_model, eta_model, yerr=deta, xerr=dSR, fmt='-o', linewidth=1.0, color=red)
        
        # Axis limits
        if np.any(x_lim):
            plt.xlim(x_lim)
        if np.any(y_lim):
            plt.ylim(y_lim)
        
        # Appearance
        plt.minorticks_on()
        plt.tick_params(axis='both', which='major', labelsize=12)
        
        # Axis labels, legend
        plt.xlabel('Process-related apparent shear rate [1/s]', fontsize=12)
        plt.ylabel('Process-related apparent viscosity [Pa.s]', fontsize=12)
        if np.any(eta_literature):
            plt.legend(['$\eta_{app,model}$', '$\eta_{app,literature}$'], fontsize=12, loc='southwest')
        
        if mode == 'default':
            plt.gca().set_fontname('Verdana')
        
        plt.hold(False)

"""# Example usage:
SR_model = [10, 20, 30, 40]
eta_model = [0.1, 0.2, 0.3, 0.4]
SR_literature = [15, 25, 35, 45]
eta_literature = [0.15, 0.25, 0.35, 0.45]
x_lim = [0, 50]
y_lim = [0, 0.5]
deta = 0.01
dSR = 0.1
mode = 'default'
comparePlotVisco(SR_model, eta_model, SR_literature, eta_literature, x_lim, y_lim, deta, dSR, mode)
plt.show()"""

