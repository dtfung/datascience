# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 22:49:33 2016

@author: donaldfung
"""

""" DATE PREPROCESSING """

def normalize_data(df = None):
    starting_price = df.ix[0, :]
    df = df/starting_price 
    return df
    
""" FINANCIAL CALCULATIONS """

def compute_daily_returns(dataframe):
    daily_returns = dataframe.copy() # copy dataframe
    # computer returns for row 1 onwards
    daily_returns[1:] = (dataframe[1:] / dataframe[:-1].values) - 1
    daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
    return daily_returns
    
def compute_cumulative_returns(dataframe, time):
    t = time
    cumulative_returns = dataframe.copy() # copy dataframe
    cumulative_returns.ix[t, :] = (dataframe.ix[t, :] / dataframe.ix[0, :] - 1)
    returns = cumulative_returns.ix[t, :]
    return returns
