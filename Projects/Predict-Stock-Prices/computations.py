# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 22:49:33 2016

@author: donaldfung
"""
 
""" FINANCIAL CALCULATIONS """
import pandas as pd

class Financials():
    def __init__(self):
        pass
    
    def rolling_mean(self, data, window):
        prices = data["Adj. Close"]
        rm = prices.rolling(window, center = False).mean()
        return rm
        
    # computer rolling standard deviation
    def rolling_stv(self, data, window):
        return pd.rolling_std(data, window)
    
    def compute_daily_returns(self, dataframe):
        daily_returns = dataframe.copy() # copy dataframe
        # computer returns for row 1 onwards
        daily_returns[1:] = (dataframe[1:] / dataframe[:-1].values) - 1
        daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
        return daily_returns
        
    def compute_cumulative_returns(self, dataframe, time):
        t = time
        cumulative_returns = dataframe.copy() # copy dataframe
        cumulative_returns.ix[t, :] = (dataframe.ix[t, :] / dataframe.ix[0, :] - 1)
        returns = cumulative_returns.ix[t, :]
        return returns
