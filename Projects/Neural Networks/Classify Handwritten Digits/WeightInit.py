# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 14:13:17 2016

@author: donaldfung
"""
import numpy as np

class InitWeightsAndBiases():
    """Choose from several initialization methods for weights and biases"""
    
    def __init__(self, layers):
        self.layers = layers
    
    def gaussian_dist_root(self):
        """ A slightly modified version using a gaussian distribution.  
        
        Here we divide the weights by the square root of the size of the input layer.  
        Note that this only applies to the weight initializations, not biases        
        
        """
        biases = [np.random.randn(layer, 1) for layer in self.layers[1:]]
        weights = [np.random.randn(y, x)/np.sqrt(x) for x, y in zip(self.layers[:-1], self.layers[1:])]
        return weights, biases
    
    def gaussian_dist(self):
        """ Returns a gaussian distribution of weights and biases"""
        biases = [np.random.randn(layer, 1) for layer in self.layers[1:]]
        weights = [np.random.randn(y, x) for x, y in zip(self.layers[:-1], self.layers[1:])]
        return weights, biases
        
    