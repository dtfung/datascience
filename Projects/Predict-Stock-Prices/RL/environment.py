#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 15:23:22 2016

@author: donaldfung
"""

import numpy as np

class Environment():
    
    def __init__(self):
        pass

    def get_state(self, row, trade_open, cum_return):
        """Get new state"""
        state = (
                 trade_open,
                 cum_return,
                 row["PE Ratio"],
                 row["PB Ratio"],
                 row["PCF Ratio"],
                 row["PS Ratio"])
        return state

    def discretize(self, data):
        """Group continuous values into bins"""

        df = data.copy() 
        cols = df.columns
        for col in cols:
            x = df[col]
            min_val = min(x)
            max_val = max(x)
            
            # get length of number
            num_length = len(str(abs(min_val)).split(".")[0])
            # calculate step size
            if num_length == 1:
                step = 1
            if num_length == 2:
                step = 2
            if num_length == 3:
                step = 5
            elif num_length > 3:
                step = 1 * 10**(num_length - 1)
            bins = np.arange(min_val, max_val, step = step)
            digitize = np.digitize(x, bins)
            df[col] = digitize
        return df
        
    
                
            
            
        
            

            

            


        