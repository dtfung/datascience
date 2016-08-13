# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:05:55 2016

@author: donaldfung
"""

filename = "Data/YAHOO-INDEX_GSPC.csv"
timeframe = [5, 30, 365]
target = "Adjusted Close"
volume = "Volume"
train_set_size = .8
test_set_size = .2

"""
"SMA_30d","STD_30d", "Boll_upper30", "Boll_lower30","SMA5_STD5"
"""
features = ["SMA30_STD30", "close_sma_ratio",
            "sma_5_30_ratio", "std5_to_std30",
            "SMA_5d", "SMA_30d", "SMA_365d",
            "STD_30d", "STD_30d", "STD_365d",
            "Boll_upper5","Boll_upper30", "Boll_upper365",
            "Boll_lower5","Boll_lower30","Boll_lower365" 
            ]
