# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 21:51:23 2016

@author: donaldfung
"""
import pandas as pd
import numpy as np
import settings

""" DATA PREPROCESSING """

def normalize_data(df = None):
    starting_price = df.ix[0, :]
    df = df/starting_price 
    return df

def fill_missing_values(dataframe):
    # Forward fill missing data
    dataframe.fillna(method = "ffill", inplace = True)
    dataframe.fillna(method = "bfill", inplace = True)
    return dataframe

def discretize(data, steps):
    # Quantile-based discretization function
    factor = pd.qcut(data, q = steps, labels = range(0, 10))
    return factor
    
def train_set_size(X):
    X = X.shape[0] * settings.train_set_size
    size = np.array([X])
    size = int(np.ceil(size))
    return size 
    
