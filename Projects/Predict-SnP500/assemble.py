# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:41:52 2016

@author: donaldfung
"""

import pandas as pd
import numpy as np
import features
import settings

class Data():
    def __init__(self):
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def read(self):
        filename = settings.filename
        self.data = pd.read_csv(filename)
        self.sort(self.data)
    
    def sort(self, data):
        data["Date"] = pd.to_datetime(data["Date"])
        data.sort_values(by = "Date", ascending = True, inplace = True)
        self.get_features(data)
        
    def get_features(self, data):
        financials = features.Financials(data)
        tf30 = settings.timeframe[1]
        moving_avg_30d = financials.get_sma(window = tf30)
        standard_dev_30d = financials.get_rolling_std(tf30)
        m30d_sma_std_ratio = financials.get_ratio(moving_avg_30d, standard_dev_30d)
        figures = {"SMA_30d":moving_avg_30d, "STD_30d":standard_dev_30d, "SMA30_STD30":m30d_sma_std_ratio}
        self.add_features(figures)
    
    def add_features(self, figures):
        for key, feature in figures.items():
            column = [key]
            df = feature.to_frame()
            df.columns = [column]
            self.data = self.data.join(df, how = "outer", sort = False)
        self.data.dropna(axis = 0, inplace = True)
        self.extract_X_and_y()
         
    def extract_X_and_y(self):
        feature_list = settings.features
        target = settings.target
        X = self.data[feature_list]
        y = self.data[target]
        X = self.normalize(X)
        self.X_train, self.y_train, self.X_test, self.y_test = self.partition(X, y)
    
    def partition(self, X, y):
        train_length = self.train_set_size(X)
        test_length = int(X.shape[0] * settings.test_set_size)
        X_train = X[:train_length]
        y_train = y[:train_length]
        y_train = y_train.shift(periods = 1)
        y_train.iloc[0]= 0
        X_test = X[-test_length:]
        y_test = y[-test_length:]
        y_test = y_test.shift(periods = 1)
        y_test.iloc[0] = 0
        return X_train, y_train, X_test, y_test

    def normalize(self, data):
        starting_price = data.ix[0, :]
        data = data/starting_price 
        return data
    
    def train_set_size(self, X):
        X = X.shape[0] * settings.train_set_size
        size = np.array([X])
        size = int(np.ceil(size))
        return size 
    
    

