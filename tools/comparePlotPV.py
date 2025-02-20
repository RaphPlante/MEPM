#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
    %Date: June 13, 2020 - February 13, 2024"""

def comparePlotPV(v_model, P_model, v_literature, P_literature, x_lim, y_lim, dP, mode, myPlot=None):
    # Colors
    blue = [0, 0.4470, 0.7410]
    red = [0.8500, 0.3250, 0.0980]
    
    if mode == 'default':
        plt.rcdefaults()
    else:
        plt.rcParams.update({'text.usetex': True})
    
    if isinstance(P_model, (int, float)) and isinstance(v_model, (int, float)) and isinstance(P_literature, (int, float)) and isinstance(v_literature, (int, float)):
        
        if myPlot is None:
            plt.figure(1)
        
        # Plot data and labels
        if np.any(P_model):
            plt.loglog(v_model, P_model, '-s', linewidth=1.5, color=red)
            t_model = [plt.text(v_model[i], P_model[i], str(round(P_model[i], 0)), fontsize=12) for i in range(len(P_model))]
            for i in range(len(P_model)):
                if np.any(P_literature) and P_model[i] <= P_literature[i]:
                    t_model[i].set_horizontalalignment('left')
                    t_model[i].set_verticalalignment('top')
                else:
                    t_model[i].set_horizontalalignment('right')
                    t_model[i].set_verticalalignment('bottom')
        
        if np.any(P_literature):
            plt.loglog(v_literature, P_literature, '-s', linewidth=1.5, color=blue)
            t_lit = [plt.text(v_literature[i], P_literature[i], str(round(P_literature[i], 0)), fontsize=12) for i in range(len(P_literature))]
            for i in range(len(t_lit)):
                if np.any(P_literature) and P_model[i] <= P_literature[i]:
                    t_lit[i].set_horizontalalignment('right')
                    t_lit[i].set_verticalalignment('bottom')
                else:
                    t_lit[i].set_horizontalalignment('left')
                    t_lit[i].set_verticalalignment('top')
        
        # Error bars
        if dP != 0:
            plt.errorbar(v_model, P_model, yerr=dP, fmt='-', linewidth=1.0, color=red)
        
        # Axis limits
        if np.any(x_lim):
            plt.xlim(x_lim)
        if np.any(y_lim):
            plt.ylim(y_lim)
        
        # Appearance
        plt.minorticks_on()
        plt.tick_params(axis='both', which='major', labelsize=12)
        
        # Axis labels, legend
        plt.xlabel('Nozzle exit velocity [mm/s]', fontsize=12)
        plt.ylabel('Required pressure [kPa]', fontsize=12)
        if np.any(P_literature):
            plt.legend(['$P_{model}$', '$P_{literature}$'], fontsize=12, loc='southeast')
        
        if mode == 'default':
            plt.gca().set_fontname('Verdana')
        
        plt.hold(False)

"""# Example usage:
v_model = [10, 20, 30, 40]
P_model = [100, 200, 300, 400]
v_literature = [15, 25, 35, 45]
P_literature = [150, 250, 350, 450]
x_lim = [0, 50]
y_lim = [0, 500]
dP = 10
mode = 'default'
comparePlotPV(v_model, P_model, v_literature, P_literature, x_lim, y_lim, dP, mode)
plt.show()"""

