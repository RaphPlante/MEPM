#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
    %Date: June 13, 2020 - February 13, 2024"""

def comparePlotQ(v_model, Q_model, v_literature, Q_literature, x_lim, y_lim, dQ, mode, myPlot=None):
    # Colors
    blue = [0, 0.4470, 0.7410]
    red = [0.8500, 0.3250, 0.0980]
    
    if mode == 'default':
        plt.rcdefaults()
    else:
        plt.rcParams.update({'text.usetex': True})
    
    if isinstance(Q_model, (int, float)) and isinstance(v_model, (int, float)) and isinstance(Q_literature, (int, float)) and isinstance(v_literature, (int, float)):
        
        if myPlot is None:
            plt.figure(2)
        
        # Plot data and labels
        if np.any(Q_model):
            plt.plot(v_model, Q_model, '-s', linewidth=1.5, color=red)
            t_model = [plt.text(v_model[i], Q_model[i], str(round(Q_model[i], 3)), fontsize=12) for i in range(len(Q_model))]
            for i in range(len(Q_model)):
                if np.any(Q_literature) and Q_model[i] <= Q_literature[i]:
                    t_model[i].set_horizontalalignment('left')
                    t_model[i].set_verticalalignment('top')
                else:
                    t_model[i].set_horizontalalignment('right')
                    t_model[i].set_verticalalignment('bottom')
        
        if np.any(Q_literature):
            plt.plot(v_literature, Q_literature, '-s', linewidth=1.5, color=blue)
            t_lit = [plt.text(v_literature[i], Q_literature[i], str(round(Q_literature[i], 3)), fontsize=12) for i in range(len(Q_literature))]
            for i in range(len(t_lit)):
                if np.any(Q_literature):
                    if Q_model[i] <= Q_literature[i]:
                        t_lit[i].set_horizontalalignment('right')
                        t_lit[i].set_verticalalignment('bottom')
                    else:
                        t_lit[i].set_horizontalalignment('left')
                        t_lit[i].set_verticalalignment('top')
        
        # Error bars
        if dQ != 0:
            plt.errorbar(v_model, Q_model, yerr=dQ, fmt='-', linewidth=1.0, color=red)
        
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
        plt.ylabel('Total mass flow rate [g/s]', fontsize=12)
        if np.any(Q_literature):
            plt.legend(['$Q_{model}$', '$Q_{literature}$'], fontsize=12, loc='southeast')
        
        if mode == 'default':
            plt.gca().set_fontname('Verdana')
        
        plt.hold(False)

"""# Example usage:
v_model = [10, 20, 30, 40]
Q_model = [0.1, 0.2, 0.3, 0.4]
v_literature = [15, 25, 35, 45]
Q_literature = [0.15, 0.25, 0.35, 0.45]
x_lim = [0, 50]
y_lim = [0, 0.5]
dQ = 0.01
mode = 'default'
comparePlotQ(v_model, Q_model, v_literature, Q_literature, x_lim, y_lim, dQ, mode)
plt.show()"""

