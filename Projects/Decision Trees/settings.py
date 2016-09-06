# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 01:05:24 2016

@author: donaldfung
"""

filename = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
columns = ["age", "workclass", "fnlwgt", "education", "education_num",
                   "marital_status", "occupation", "relationship", "race", "sex", 
                   "capital_gain", "capital_loss", "hours_per_week", "native_country", 
                   "high_income"]
                   
columns_subset = ["age", "workclass", "education_num", 
               "marital_status", "occupation", "relationship", 
               "race", "sex", "hours_per_week", "native_country"]