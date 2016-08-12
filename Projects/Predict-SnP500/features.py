# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:03:47 2016

@author: donaldfung
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 22:49:33 2016

@author: donaldfung
"""
import settings 

class Financials():
    def __init__(self, data):
        self.data = data
        self.target = settings.target
        self.prices = self.data[self.target]
    
    def get_sma(self, window):
        rm = self.prices.rolling(window, center = False).mean()
        rm = rm.shift(periods = 1)
        return rm
        
    def get_close_SMA_ratio(self, window):
        rm = self.get_rolling_mean(self.data, window)
        ratio = self.prices[0:] / rm[0:]
        return ratio
    
    def get_ratio(self, ma1, ma2):
        ratio = ma1/ma2
        return ratio
        
    # compute rolling standard deviation
    def get_rolling_std(self, window):
        prices = self.prices.rolling(window, center = False).std()
        prices = prices.shift(periods = 1)
        return prices
        
    # compute bollinger bands
    def get_bollinger_bands(self, window):
        rolling_means = self.get_rolling_mean(self.data, window)
        rolling_std = self.get_rolling_std(self.data, window)
        upper_band = rolling_means + rolling_std * 2
        lower_band = rolling_means - rolling_std * 2
        return upper_band, lower_band
    
    def get_daily_returns(self):
        daily_returns = self.prices.copy()
        daily_returns[1:] = (self.prices[1:] / self.prices[:-1].values) - 1
        daily_returns.ix[0] = 0
        return daily_returns
        
    def get_cumulative_returns(self):
        cumulative_returns = self.prices.copy()
        cumulative_returns[1:] = (cumulative_returns[1:] / cumulative_returns[0] - 1)
        cumulative_returns[0] = 0
        return cumulative_returns
