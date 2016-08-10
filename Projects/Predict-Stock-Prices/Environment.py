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
import settings

class Market():
    def __init__(self, data):
        self.state = None
        self.data = data
        self.learner = predict.Q_Learning(self.data)
    
    def get_financials(self):
        data = self.data.copy()
        financials = computations.Financials()
        n = 20 # look back n number of days / window
        volume = data["Adj. Volume"]
        rolling_mean = financials.get_rolling_mean(data, n)# get rolling mean
        upper, lower = financials.get_bollinger_bands(data, n) # get bollinger bands
        daily_returns = financials.get_daily_returns(data) # get daily returns
        cumulative_returns = financials.get_cumulative_returns(data) # get cumulative returns
        adj_close_sma = financials.get_close_SMA_ratio(data, n) # get adj.close to SMA ratio
        # add data to dataframe
        df = data[["Adj. Close"]]
        # dictionary of features
        features = {"Volume": volume, "Rolling_Mean":rolling_mean, "Upper":upper, "Lower":lower,"Daily_Returns":daily_returns,
        "Cumulative_Returns":cumulative_returns, "Close_SMA":adj_close_sma}
        for key, feature in features.items():
            column = [key]
            discretized_data = prepare.discretize(feature, steps = 10)
            temp_df = discretized_data.to_frame()
            temp_df.columns = [column]
            df = df.join(temp_df, how = "outer")
        self.get_state(df, n)
    
    def get_state(self, df, window):
        df = df.ix[20:, 1:] # exclude price
        # TODO: supply state to Q-Learning agent
        states = [tuple(row) for row in df.values]
        
        