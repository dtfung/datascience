# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 01:58:56 2016

@author: donaldfung
"""
import numpy as np

class QuadraticCost():
    
    def current_layer_delta(self, a, y, z):
        delta = (a - y) * self.sigmoid_prime(z)
        return delta
        
    def previous_layer_delta(self, delta, z, w):
        delta = np.dot(w.transpose(), delta) * self.sigmoid_prime(z)
        return delta
        
    def sigmoid(self, z):
        a = 1.0/(1.0 + np.exp(-z))
        return a 
        
    def sigmoid_prime(self, z):
        delta_a = self.sigmoid(z) * (1 - self.sigmoid(z))
        return delta_a
        
    def calc_cost(self, a, y):
        cost = 0.5 * np.linalg.norm(a - y)**2
        return cost