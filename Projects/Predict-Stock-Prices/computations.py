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
        # shift index by 1 so as to not use current price in calc
        rm = rm.shift(periods = 1)
        return rm
        
    def get_close_SMA_ratio(self, data, window):
        prices = data["Adj. Close"]
        rm = self.get_rolling_mean(data, window)
        ratio = prices[0:] / rm[0:]
        return ratio
        
    # compute rolling standard deviation
    def get_rolling_stv(self, data, window):
        prices = data["Adj. Close"]
        prices = prices.rolling(window, center = False).std()
        prices = prices.shift(periods = 1)
        return 
        
    # compute bollinger bands
    def get_bollinger_bands(self, data, window):
        rolling_means = self.get_rolling_mean(data, window)
        rolling_stv = self.get_rolling_stv(data, window)
        upper_band = rolling_means + rolling_stv * 2
        lower_band = rolling_means - rolling_stv * 2
        return upper_band, lower_band
    
    def get_daily_returns(self, data):
        prices = data["Adj. Close"]
        daily_returns = prices.copy() # copy dataframe
        # computer returns for row 1 onwards
        daily_returns[1:] = (prices[1:] / prices[:-1].values) - 1
        daily_returns.ix[0] = 0 # set daily returns for row 0 to 0
        return daily_returns
        
    def get_cumulative_returns(self, data):
        prices = data["Adj. Close"]
        cumulative_returns = prices.copy()
        cumulative_returns[1:] = (prices[1:] / prices[0] - 1)
        cumulative_returns[0] = 0
        return cumulative_returns
