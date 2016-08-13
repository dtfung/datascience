# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:41:52 2016

@author: donaldfung
"""

import pandas as pd
import numpy as np
import features
import settings
import predict

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
        t5 = settings.timeframe[0]
        t30 = settings.timeframe[1]
        t365 = settings.timeframe[2]
        moving_avg_5d = financials.get_sma(window = t5)
        moving_avg_30d = financials.get_sma(window = t30)
        moving_avg_365d = financials.get_sma(window = t365)
        standard_dev_30d = financials.get_rolling_std(t30)
        standard_dev_5d = financials.get_rolling_std(t5)
        standard_dev_365d = financials.get_rolling_std(t365)
        bollinger_upper5, bollinger_lower5 = financials.get_bollinger_bands(t5) 
        bollinger_upper30, bollinger_lower30 = financials.get_bollinger_bands(t30)
        bollinger_upper365, bollinger_lower365 = financials.get_bollinger_bands(t365) 
        m30d_sma_std_ratio = financials.get_ratio(moving_avg_30d, standard_dev_30d)
        sma_5_365_ratio = financials.get_ratio(moving_avg_5d, moving_avg_365d)
        sma_5_30_ratio = financials.get_ratio(moving_avg_5d, moving_avg_365d)
        std5_to_std30 = financials.get_ratio(standard_dev_5d, standard_dev_30d)
        m5d_sma_std_ratio = financials.get_ratio(moving_avg_5d, standard_dev_5d)
        close_sma_ratio = financials.get_close_SMA_ratio(t30)
        
        """
                    "Boll_upper30":bollinger_upper30,
                    "Boll_lower30":bollinger_lower30,
                    "sma_5_365_ratio":sma_5_365_ratio,
                    "sma_5_30_ratio":sma_5_30_ratio,
                    "SMA5_STD5":m5d_sma_std_ratio
        """
        figures = {
                    "SMA_5d":moving_avg_5d,
                    "SMA_30d":moving_avg_30d,
                    "SMA_365d":moving_avg_365d,
                    "STD_5d":standard_dev_5d,
                    "STD_30d":standard_dev_30d,
                    "STD_365d":standard_dev_365d,
                    "Boll_upper5":bollinger_upper5,
                    "Boll_lower5":bollinger_lower5,
                    "Boll_upper30":bollinger_upper30,
                    "Boll_lower30":bollinger_lower30,
                    "Boll_upper365":bollinger_upper365,
                    "Boll_lower365":bollinger_lower365,
                    "SMA30_STD30":m30d_sma_std_ratio,
                    "close_sma_ratio":close_sma_ratio,
                    "sma_5_30_ratio":sma_5_30_ratio,
                    "std5_to_std30":std5_to_std30
                    }
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
        model = predict.Model(self.X_train, self.y_train, self.X_test, self.y_test)
        model.predict()
    
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
    
    

