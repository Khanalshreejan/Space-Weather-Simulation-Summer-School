#!/usr/bin/env python
"""Space 477: Python: I

cosine approximation function
"""
__author__ = 'Shreejan Khanal'
__email__ = 'shreejan.khanal2@mavs.uta.edu'

from math import factorial
from math import pi


def cos_approx(x, accuracy=10):
    """
    Taylor series expansion of Cosine function
    arguments
    x (float)
    To evaluate cosine of 
    accuracy (int):
        (default : 10) number of Taylor series coefficients to use.
    Returns:
        (floats): 
    """
    series_list=[(-1)**n/factorial(2*n)*(x**(2*n)) for n in range(accuracy)]
    return (sum(series_list))
    #for n in range(accuracy):
    
        #series_list=[(-1)**n/factorial(2*n)*(x**(2*n))]
    #return (sum(series_list))
# Will only run if this is run from command line as opposed to imported
if __name__ == '__main__':  # main code block
    print("cos(0) = ", cos_approx(0))
    print("cos(pi) = ", cos_approx(pi))
    print("cos(2*pi) = ", cos_approx(2*pi))
    #print("cos(4*pi) = ", cos_approx(4*pi))
    print("more accurate cos(2*pi) = ", cos_approx(2*pi, accuracy=50))
