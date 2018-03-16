#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STSCI 4780 Assignment 04 Problem 2 

Inference with the Cauchy distribution: 
Plot posterior PDFs of the location of Cauchy-distributed data with a known scale parameter
used with the UnivariateBayesianInference class.

Created March 9, 2018 by Jiajun Gu (jg882)
"""

import numpy as np
import scipy
from scipy import stats, special, integrate
from scipy.stats import cauchy
import matplotlib.pyplot as plt

from univariate_bayes import UnivariateBayesianInference


plt.ion()


class CauchyLocationInference(UnivariateBayesianInference):
    """
    Implement inference for the location of Cauchy-distributed data 
    with a known scale parameter.
    """

    def __init__(self, d, x, prior, x0_u = 1e5, x0_l=-1e5, nx0=1e6):
        """
        Define a posterior PDF for a Cauchy location parameter.

        Parameters
        ----------
        d : float
            scale parameter
            
        x : float array
            the location of rays issuing from (x0,d) with a uniformly distributed angle

        prior : const or function
            Prior PDF for the rate, as a constant for flat prior, or
            a function that can evaluate the PDF on an array
        """
        self.d = d
        self.x = x
        self.x0vals = np.linspace(x0_l, x0_u, nx0)

        # Pass the info to the base class initializer.
        super().__init__(self.x0vals, prior, self.lfunc)

    def lfunc(self, x0vals):
        """
        Evaluate the Cauchy likelihood function on a grid of x0.
        """
       
        x0vals_mat = np.array([x0vals,]*len(self.x)) # matrix with each row as x0vals
        x_mat = np.array([self.x,]*len(x0vals))
        x_mat = x_mat.transpose() # matrix with each column as x
       
        lfunc_mat = 1/((x_mat-x0vals_mat)**2+self.d**2) # matrix with each column representing 
                                                        # how likely each x is given certain x0
        
        return lfunc_mat.prod(axis=0)
        
        
