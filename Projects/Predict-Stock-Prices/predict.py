# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:16:58 2016

@author: donaldfung
"""

import settings
import assemble
import Environment

class Q_Learning():
    def __init__(self, data):
        # Initialize variables here
        self.prices = data["Adj. Close"]
        self.count = 0
        
    def update(self, state):
        """ Get new state from environment
        
        input:  state = (volume, rolling_mean, upper, lower,  cumulative returns close_sma)
                type = tuple
        """
        
        
            
            return

def run():
    #   Get stock price data
    data = assemble.Data(settings.company, settings.storage_option)
    df = data.create_dataframe()
    #   Setup environment
    env = Environment.Market(df)
    env.get_financials()
    
if __name__ == "__main__":
    run()
    