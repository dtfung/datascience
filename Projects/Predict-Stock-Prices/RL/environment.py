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
        state = (trade_open, 
                 cum_return, 
                 row["PE Ratio"],
                 row["PB Ratio"],
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
            step = 1 * 10**(num_length - 1)
            bins = np.arange(min_val, max_val, step = step)
            digitize = np.digitize(x, bins)
            df[col] = digitize
        return df
        
    def calc_daily_return(self, price_data, timestep, action):
        """The % daily return based on an action"""

        while price_data.iloc[timestep + 1]:
            # get price
            current_price = price_data.iloc[timestep]
            next_day_price = price_data.iloc[timestep + 1]

            diff = next_day_price - current_price
            daily_return = diff/current_price
            
            if action == "buy":
                if daily_return < 0.0:
                    return daily_return
                else:
                    return abs(daily_return)  
            elif action == "sell":
                if daily_return < 0.0:
                    return abs(daily_return)
                else:
                    return - daily_return      
            else:
                return 0.0
            

            

            


        