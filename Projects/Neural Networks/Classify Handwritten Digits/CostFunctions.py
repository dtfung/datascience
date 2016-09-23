# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:21:39 2016

@author: donaldfung
"""
import numpy as np

class QuadraticCost():

    def calc_delta(self, a, y, z):
        delta = (a - y) * self.sigmoid_prime(z)
        return delta

    def sigmoid(self, z):
        return 1.0/(1.0 + np.exp(-z))
        
    def sigmoid_prime(self, z):
            """Derivative of the sigmoid function."""
            change_z = self.sigmoid(z)
            return change_z * (1 - change_z)
            
class CrossEntropy():
    
    def calc_delta(self, a, y, z):
        delta = a - y
        return delta