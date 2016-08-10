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
        rolling_mean = financials.get_rolling_mean(data, n)# get rolling mean
        rolling_std = financials.get_rolling_std(data, n) # get rolling std
        bollinger_upper, bollinger_lower = financials.get_bollinger_bands(data, n) # get bollinger bands
        cumulative_returns = financials.get_cumulative_returns(data) # get cumulative returns
        adj_close_sma = financials.get_close_SMA_ratio(data, n) # get adj.close to SMA ratio
        # add data to dataframe
        df = data[["Adj. Close"]]
        # dictionary of features
        features = {"Rolling_Std": rolling_std, "Rolling_Mean":rolling_mean, "Bollinger_Upper":bollinger_upper, "Bollinger_Lower":bollinger_lower,
        "Cumulative_Returns":cumulative_returns, "Close_SMA":adj_close_sma}
        for key, feature in features.items():
            column = [key]
            discretized_data = prepare.discretize(feature, steps = settings.steps)
            temp_df = discretized_data.to_frame()
            temp_df.columns = [column]
            df = df.join(temp_df, how = "outer")
        self.get_state(df, n)
    
    def get_state(self, df, window):
        df = df.ix[20:, 1:] # exclude price
        for row in df.values:
            state = tuple(row)
            self.learner.update(state)
            
    def get_reward(self, action):
        
        # TODO: check if a position is open
        # TODO: get position info (direction, date, quantity, open price)
        # TODO: calculate reward based on action (if hold, do nothing)
        
        return reward
        