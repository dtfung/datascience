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
        self.learner = None
        
    def get_learning_method(self):
        approach = settings.approach
        if approach == "model_based":
            return settings.Approach.model_based   
        else:
            return settings.Approach.model_free
    
    def get_financials(self):
        data = self.data.copy()
        financials = computations.Financials() # init Financials class 
        # window sizes
        t5 = settings.time_frame[0] # 5 day window
        t30 = settings.time_frame[1] # 30 day window
        t360 = settings.time_frame[2] # 1 year window
        """ Features """
        # moving averages
        moving_average_five_day = financials.get_rolling_mean(data, t5) # 5 day SMA
        moving_average_thirty_day = financials.get_rolling_mean(data, t30) # 30 day SMA
        moving_average_one_year = financials.get_rolling_mean(data, t360) # 1 yr SMA
        # rolling standard deviations
        rolling_std_five_day = financials.get_rolling_std(data, t5) # 5 day rolling STD
        rolling_std_thirty_day = financials.get_rolling_std(data, t30) # 30 day rolling STD
        rolling_std_one_year = financials.get_rolling_std(data, t360) # 1 year STD
        # bollinger bands
        bollinger_upper_five_day, five_daybollinger_lower_five_day = financials.get_bollinger_bands(data, t5) # 5 day
        bollinger_upper_thirty_day, five_daybollinger_lower_thirty_day = financials.get_bollinger_bands(data, t30) # 30 day
        bollinger_upper_one_year, five_daybollinger_lower_one_year = financials.get_bollinger_bands(data, t360) # 1 yr
        # ratios
        adj_close_sma = financials.get_close_SMA_ratio(data, t30) # get adj.close to SMA ratio
        sma5_to_sma30 = financials.get_ratio(moving_average_five_day, moving_average_thirty_day)  # ratio between 5 day SMA and 30 day SMA
        std5_to_std30 = financials.get_ratio(rolling_std_five_day, rolling_std_thirty_day) # ration between 5 day STD and 30 day STD
        
        # add data to dataframe
        df = data.copy()
        '''
                    
                    
                    "Bollinger_Upper_5d":bollinger_upper_five_day,
                    "Bollinger_Upper_30d":bollinger_upper_thirty_day,
                    "Bollinger_Upper_1yr":bollinger_upper_one_year,
                    "Bollinger_Lower_5d":five_daybollinger_lower_five_day,
                    "Bollinger_Lower_30d":five_daybollinger_lower_thirty_day,
                    "Bollinger_Lower_1yr":five_daybollinger_lower_one_year,
                    ,'''
        features = {
                    "SMA_5d":moving_average_five_day,
                    
                    "SMA_30d":moving_average_thirty_day,
                    "SMA_1yr":moving_average_one_year,
                    "STD_5d":rolling_std_five_day,
                    "STD_30d":rolling_std_thirty_day,
                    "STD_1yr":rolling_std_one_year, 
                    "Close_SMA":adj_close_sma,
                    "SMA5_to_SMA30":sma5_to_sma30,
                    "std5_to_std30":std5_to_std30
                    }
        self.add_features(dataframe = df, features = features)
        
    def add_features(self, dataframe, features):
        approach = self.get_learning_method() # get learning approach
        if approach == settings.Approach.model_free:
            for key, feature in features.items():
                column = [key]
                discretized_data = prepare.discretize(feature, steps = settings.steps)
                temp_df = discretized_data.to_frame()
                temp_df.columns = [column]
                dataframe = dataframe.join(temp_df, how = "outer")
            #scores = prepare.feature_selection(dataframe)
            self.learner = predict.Q_Learning(self.data)
            self.get_state(dataframe)
        else:
            for key, feature in features.items():
                column = [key]
                temp_df = feature.to_frame()
                temp_df.columns = [column]
                dataframe = dataframe.join(temp_df, how = "outer")
            dataframe=dataframe.dropna()   
            dataframe=prepare.normalize_data(dataframe)
            self.learner = predict.Models(data = dataframe)
            self.learner.partition_dataset()
            
    def get_state(self, df):
        df = df.dropna()
        features = settings.features
        df = df[features]
        count = 0
        for row in df.values:
            state = tuple(row)
            self.learner.update(state, count)
            count += 1
        self.learner.performance.show()