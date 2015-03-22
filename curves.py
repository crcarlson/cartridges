# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 13:41:10 2015

@author: Christopher R. Carlson, crcarlson@gmail.com
"""

from pylab import exp as py_exp

def sigmoid(x, alpha, x_0 = 0.0):
    """Sigmoid function
    The sigmoid is defined from -inf to inf
    For alpha = 1, the sigmoid goes from 0 to 1 over a range of +-6
    The sigmoid is symetric
    The sigmoid is = 1/2 at x = x_0

    Notes:
        For the sigmoid to fit within a range of +-R, alpha = 6/R
        So for s(x) to transition from 0 to 1 over the range of +- 0.5,
        then alpha = 6.0 / 0.5 = 12.0
    """
    return 1 / ( 1 + py_exp(-alpha*(x-x_0)))


