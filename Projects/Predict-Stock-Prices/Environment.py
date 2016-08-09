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
    
    def get_financials():
        financials = computations.Financials()
        
        #self.learner.update(state)
        
        