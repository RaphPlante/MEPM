#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# Data for figure 1
d = np.array([150, 200, 250, 330])  # µm

n_25 = np.array([0.3670, 0.4864, 0.6469, 0.6814])
K_25 = np.array([2983, 1774, 1239, 1670])

n_b = np.array([np.nan, 0.4012, 0.5867, 0.5551])
K_b = np.array([np.nan, 3189, 1693, 2716])

# Figure 1
plt.figure(1)

plt.plot(d, n_25, 'ko-', label='n - 25 wt.%')
plt.plot(d, K_25, 'ks--', label='K - 25 wt.%')
plt.plot(d, n_b, 'ro-', label='n - Benchmark')
plt.plot(d, K_b, 'rs--', label='K - Benchmark')

lgd0 = plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=4)
plt.xlim([150, 350])
plt.xlabel('Nozzle diameter, D [$\mu$m]', fontsize=12)
plt.ylabel('Flow consistency index, K [Pa.s$^n$]', fontsize=12)

plt.gca().tick_params(axis='y', colors='k')
plt.gca().tick_params(axis='y', colors='r')
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=12)

plt.ylabel('Flow behaviour index, n [-]', fontsize=12)

# Figure 2
plt.figure(2)

n_25_a = np.array([0.3634, 0.5224, 0.5424])
k_25_a = np.array([13600, 3013, 3080])
n_30_a = np.array([0.3698, 0.4629, 0.4495])
k_30_a = np.array([15150, 3885, 3643])
n_b_a = np.array([0.274, 0.0851, 0.0742])
k_b_a = np.array([6352, 3790, 3600])

plt.subplot(1, 2, 1)
X = ['25%', '30%', 'Bench.']
Y = np.vstack((n_25_a, n_30_a, n_b_a))

graph1 = plt.bar(X, Y.T)
graph1[0].set_color('r')
graph1[1].set_color('b')
graph1[2].set_color('g')
plt.ylabel('Flow behaviour index, n [-]', fontsize=12)
plt.legend(['Capillary data', 'Rheometer data', 'Combined model'], fontsize=10)

plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=12)

plt.subplot(1, 2, 2)
XX = ['25%', '30%', 'Bench.']
YY = np.vstack((k_25_a, k_30_a, k_b_a)) / 1000

graph2 = plt.bar(XX, YY.T)
graph2[0].set_color('r')
graph2[1].set_color('b')
graph2[2].set_color('g')
plt.ylabel('Flow consistency index, K [Pa.s$^n$] $\times$10$^3$', fontsize=12)

plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
plt.show()

