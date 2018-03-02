#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 03 Problem 4 

The normal-normal conjugate model

Jiajun Gu (jg882)
"""

import numpy as np
import numpy.testing as npt
import scipy
from scipy import stats, integrate
import matplotlib.pyplot as plt

plt.ion()


# Problem 4.1

## Generate samples
N = 100 #
mu = 3
sigma = 10
d = stats.norm.rvs(mu,sigma,size=N)

## Define prior
mu0 = 10
w0 = 5
prior = stats.norm(mu0,w0)

## Calculate conjugate posterior
w = sigma/np.sqrt(N)
B = w**2/(w**2+w0**2)
mu_post = np.mean(d)+B*(mu0-np.mean(d))
w_post = w*np.sqrt(1-B)
posterior = stats.norm(mu_post,w_post)

## Plot posterior PDF
mus_max = 20
mus_no = 1001
mus = np.linspace(0., mus_max, mus_no)
post1 = posterior.pdf(mus)
plt.plot(mus, post1, 'b-', lw=2, alpha=0.6, label='Conjugate distribution')
plt.xlabel('$\mu$', fontsize=16)
plt.ylabel('p($\mu$|D,$\sigma$,$\mathcal{C}$)', fontsize=16)


# Problem 4.2

## Calculate likelihood function
likelihood = 1/sigma**N/(2*np.pi)**(N/2)*np.exp(-N*np.var(d)/2/sigma**2)*np.exp(-N*(mus-np.mean(d))**2/2/sigma**2)

## Calculate prior * likelihood
pml = prior.pdf(mus)*likelihood


## Normalize pml using trapezoid rule
delta = mus_max/(mus_no-1)
integ_trapz = (sum(pml) - 1/2*pml[0] - 1/2*pml[mus_no-1])*delta
post2 = pml/integ_trapz

## Plot
plt.plot(mus, post2, 'r-', lw=2, linestyle='--', alpha=0.7, label='Trapezoid rule')
plt.legend()


# Problem 4.3

## Test
def test_trapz_approx():
    """
    Check whether trapezoid rule integration matches 
    the result given by mumpy.trapz.
    Require 1% relative accuracy.
    """
    npt.assert_allclose(integ_trapz, np.trapz(pml)*delta, rtol=.01)
    
## Test
def test_post_match():
    """
    Check whether the two posterior PDFs 
    match over the grid of mu values.
    Require 10% relative accuracy.
    """
    npt.assert_allclose(post1, post2, rtol=.1)