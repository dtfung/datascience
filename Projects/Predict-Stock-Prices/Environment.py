# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:34:06 2016

@author: donaldfung
"""
import computations
import predict

class Market():
    def __init__(self):
        self.state = None
        self.learner = predict.Q_Learning()
    
    def get_financials(self, data):
        financials = computations.Financials()
        n = 20 # look back n number of days / window
        rolling_mean = financials.get_rolling_mean(data, n)# get rolling mean
        upper, lower = financials.get_bollinger_bands(data, n) # get bollinger bands
        #self.learner.update(state)
        
        