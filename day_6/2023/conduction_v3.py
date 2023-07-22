#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from tridiagonal import solve_tridiagonal

# ----------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------

if __name__ == "__main__":

    dx = 0.25

    # set x with 1 ghost cell on both sides:
    x = np.arange(-dx, 10 + 2 * dx, dx)

    # make an altitude array for plotting:
    alt = 100.0 + x * 50.0

    t_lower = 200.0

    nPts = len(x)

    # set default coefficients for the solver:
    a = np.zeros(nPts) + 1
    b = np.zeros(nPts) - 2
    c = np.zeros(nPts) + 1
    d = np.zeros(nPts)

    # boundary conditions (bottom - fixed):
    a[0] = 0
    b[0] = 1
    c[0] = 0
    d[0] = t_lower

    # top - zero gradient (Tn - Tn-1 = 0):
    a[-1] = -1
    b[-1] = 1
    c[-1] = 0
    d[-1] = 0.0

    # create plot:
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111)

    for ut in range(0,24,1):

        # UT-dependent heating function:
        heat = 5.0 * np.sin(ut * np.pi / 24.0)
        # at night, there is still chemistry, which adds heat:
        if (heat < 1.0):
            heat = 1.0

        # add sources:
        l = ((x > 1.0) & (x < 7.5))
        d[l] = -heat * (10.0 - x[l])/10.0
    
        # solve for Temperature:
        t = solve_tridiagonal(a, b, c, d)

        ax.plot(t, alt)

    plotfile = 'conduction_v3.png'
    print('writing : ',plotfile)    
    fig.savefig(plotfile)
    plt.close()
    
    
    
