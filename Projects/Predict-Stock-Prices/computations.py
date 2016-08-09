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
    
    def get_rolling_mean(self, data, window):
        prices = data["Adj. Close"]
        rm = prices.rolling(window, center = False).mean()
        return rm
        
    # compute rolling standard deviation
    def get_rolling_stv(self, data, window):
        prices = data["Adj. Close"]
        return prices.rolling(window, center = False).std()
        
    # compute bollinger bands
    def get_bollinger_bands(self, data, window):
        rolling_means = self.get_rolling_mean(data, window)
        rolling_stv = self.get_rolling_stv(data, window)
        upper_band = rolling_means + rolling_stv * 2
        lower_band = rolling_means - rolling_stv * 2
        return upper_band, lower_band
    
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
