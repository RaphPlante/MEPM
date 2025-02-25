#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MaxNLocator

"""Author: David Brzeski, Jean-François Chauvette, Raphaël Plante
    %Date: June 13, 2020 - February 13, 2024"""


def comparePlotPV(v, P, x_lim=None, y_lim=None, dP=0, mode='default', my_plot=None):
    if my_plot is None:
        fig, my_plot = plt.subplots()

    red = [0.8500, 0.3250, 0.0980]

    if P is not None and v is not None:
        my_plot.loglog(v, P, '-s', linewidth=1.5, color=red,
                       label='$P_{model}$' if mode == 'latex' else 'P_{model}')
        if np.any(dP):
            my_plot.errorbar(v, P, yerr=dP,
                             fmt='o', color=red, linewidth=1)

        for x, y in zip(v, P):
            my_plot.text(x, y, f'{y:.0f}', fontsize=12,
                         ha='left', va='top', color=red)

    # Set x-axis to log scale and custom ticks
    my_plot.set_xscale('log')
    custom_xticks = sorted(set(v))  # Custom ticks from v data
    my_plot.set_xticks(custom_xticks)  # Set custom ticks for x-axis
    # Use normal formatting for x-axis ticks
    my_plot.get_xaxis().set_major_formatter(ScalarFormatter())
    my_plot.get_xaxis().get_major_formatter().set_scientific(
        False)  # Turn off scientific formatting for x-axis

    # Set y-axis ticks with logarithmic scale, limit the number of ticks
    my_plot.yaxis.set_major_locator(
        MaxNLocator(nbins=len(v)+1))  # Limit y-axis ticks
    # Use normal formatting for y-axis ticks
    my_plot.get_yaxis().set_major_formatter(ScalarFormatter())
    my_plot.get_yaxis().get_major_formatter().set_scientific(
        False)  # Turn off scientific formatting for y-axis

    # Set the labels for the axes (if necessary)
    my_plot.set_xlabel('Nozzle exit velocity [mm/s]', fontsize=12)
    my_plot.set_ylabel('Required pressure [kPa]', fontsize=12)
    my_plot.grid(True, which="both", ls="--")

    # Print tick values in the console
    x_ticks = my_plot.get_xticks()
    y_ticks = my_plot.get_yticks()

    # Format the ticks as desired (you can format them with scientific notation if you like)
    print("X-axis ticks:")
    for tick in x_ticks:
        print(f"{tick:.2f}")  # Adjust formatting as needed

    print("Y-axis ticks:")
    for tick in y_ticks:
        print(f"{tick:.2f}")  # Adjust formatting as needed

    plt.show()
