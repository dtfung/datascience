# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 17:38:37 2016

@author: donaldfung
"""
import numpy as np

class RandomGaussian():
    
    def init_w_and_b(self, layers):
        """Initialize weights and biases using a gaussian distribution"""
        weights = [np.random.randn(y, x) for x, y in zip(layers[:-1], layers[1:])]
        biases = [np.random.randn(l, 1) for l in layers[1:]]
        return weights, biases