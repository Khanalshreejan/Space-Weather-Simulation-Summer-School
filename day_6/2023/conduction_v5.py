#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from tridiagonal import solve_tridiagonal

# ----------------------------------------------------------------------
# Solve the heat conduction equation, assuming:
#   1. steady-state
#   2. top boundary is zero gradient
#   3. source term is time-dependent
#   4. bottom BC is time dependent
# ----------------------------------------------------------------------

if __name__ == "__main__":

    # tidal characteristics:
    ampDiurnal = 50.0 # in K
    phaseDiurnal = 15.0 # in hours, where peak occurs
    ampSemi = 3.0 # in K
    phaseSemi = 12.0 # in hours, where peak occurs
    
    dx = 0.025

    # set x with 1 ghost cell on both sides:
    x = np.arange(-dx, 10 + 2 * dx, dx)

    nDays = 30
    dtime = 1.0 # hours
    times = np.arange(0, nDays * 24.0, dtime)

    period = 27.0 * 24.0  # in hours
    f107 = 100.0 + 15.0 * np.sin(times / period * 2.0 * np.pi)

    # Create 2d arrays for plotting:
    nTimes = len(times)
    nAlts = len(x)
    temp2d = np.zeros((nAlts, nTimes))
    alt2d = np.zeros((nAlts, nTimes))
    time2d = np.zeros((nAlts, nTimes))
    
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

    for i, time in enumerate(times):

        ut = time % 24.0
        # UT-dependent heating function:
        peakEnergy = f107[i] / 2.0
        heat = peakEnergy * np.sin(ut * np.pi / 24.0)
        # at night, there is still chemistry, which adds heat:
        if (heat < 25.0):
            heat = 25.0

        unmodeled = np.random.normal(1.0, 0.1)
        heat = heat * unmodeled
            
        # add sources:
        l = ((x > 1.0) & (x < 7.5))
        d[l] = -heat * (10.0 - x[l])/10.0 * (dx ** 2)

        # time-dependent bottom BC:
        ut2rad = np.pi / 12.0
        diurnal = ampDiurnal * np.cos((ut - phaseDiurnal) * ut2rad)
        semi = ampSemi * np.cos(2 * (ut - phaseSemi) * ut2rad)
        gravity_wave = np.random.normal(0.0, 5.0)
        t_lower = 200.0 + diurnal + semi + gravity_wave
        d[0] = t_lower
        
        # solve for Temperature:
        t = solve_tridiagonal(a, b, c, d)

        # fill in arrays for plotting
        temp2d[:, i] = t
        alt2d[:, i] = alt
        time2d[:, i] = time/24.0

    # create plot:
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111)
    ax.contourf(time2d, alt2d, temp2d)    

    plotfile = 'conduction_v5.png'
    print('writing : ',plotfile)    
    fig.savefig(plotfile)
    plt.close()
    
    
    
