# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:05:55 2016

@author: donaldfung
"""

filename = "Data/YAHOO-INDEX_GSPC.csv"
timeframe = [5, 30, 365]
features = ["SMA_30d","STD_30d","SMA30_STD30"]
target = "Adjusted Close"
train_set_size = .8
test_set_size = .2