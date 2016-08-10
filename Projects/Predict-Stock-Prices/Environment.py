# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:34:06 2016

@author: donaldfung
"""
import computations
import predict
import prepare
import assemble
import pandas as pd
class Market():
    def __init__(self):
        self.state = None
        self.learner = predict.Q_Learning()
    
    def get_financials(self, data):
        financials = computations.Financials()
        n = 20 # look back n number of days / window
        volume = data["Adj. Volume"]
        rolling_mean = financials.get_rolling_mean(data, n)# get rolling mean
        upper, lower = financials.get_bollinger_bands(data, n) # get bollinger bands
        daily_returns = financials.get_daily_returns(data) # get daily returns
        cumulative_returns = financials.get_cumulative_returns(data) # get cumulative returns
        adj_close_sma = financials.get_close_SMA_ratio(data, n) # get adj.close to SMA ratio
        # add data to dataframe
        df = data.copy()
        # dictionary of features
        features = {"Rolling_Mean":rolling_mean, "Upper":upper, "Lower":lower,"Daily_Returns":daily_returns,
        "Cumulative_Returns":cumulative_returns, "Close_SMA":adj_close_sma}
        for key, feature in features.items():
            column = [key]
            temp_df = feature.to_frame()
            temp_df.columns = [column]
            df = df.join(temp_df, how = "outer")
    
        
    
        
        