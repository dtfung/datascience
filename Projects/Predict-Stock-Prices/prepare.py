# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 21:51:23 2016

@author: donaldfung
"""
import pandas as pd
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