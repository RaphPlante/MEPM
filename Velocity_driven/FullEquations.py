#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

v = 10
n = 0.44
k = 730
eta_inf = 0
alpha = 1
L = 18.87
D = 0.510
d_p = 9.62
P_amb = 101325

P = (8 * L * alpha * v / D**2) * (((3 * n + 1) / n) * (k * (alpha * v / D)**(n - 1) + eta_inf)) + P_amb

print(f'Piston pressure: {P / 1000:.1f} kPa')


