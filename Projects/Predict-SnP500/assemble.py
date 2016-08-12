# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:41:52 2016

@author: donaldfung
"""

import pandas as pd
import features
import settings

class Data():
    def __init__(self):
        self.data = None
        self.X = None
        self.y = None
        
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
        self.X, self.y = self.extract_X_and_y()
         
    def extract_X_and_y(self):
        feature_list = settings.features
        target = settings.target
        X = self.data[feature_list]
        y = self.data[target]
        X = self.normalize(X)
        return X, y

    def normalize(self, data):
        starting_price = data.ix[0, :]
        data = data/starting_price 
        return data
    
    

