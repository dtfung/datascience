# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:17:36 2016

@author: donaldfung
"""

""" Retrieve and process raw data and create csv and sqlite database"""

import quandl
import sqlite3
import settings

HEADERS = [
    "Name",
    "Ticker",
    "PE_Ratio",
    "Volume", 
    "Ebitda",
    
]


def get_data(ticker = None):
    
    # quandl key
    api_key = settings.api_key
    quandl.ApiConfig.api_key = api_key
    
    # get codes
    stock_price_code = settings.stock_price_code
    pe_ratio_code = settings.pe_ratio_code
    
    # store codes
    codes = [stock_price_code, pe_ratio_code]
    
    # empty array using for storing raw data
    data_list = []
    
    for value in codes:
        # get data using Quandl Python module
        data = quandl.get(value)
        
        # store data in array
        data_list.append(data)

    return data_list
    
data = get_data('AAPL')
pe = data[1]
print (pe.head(20))

data = get_data('T')
pe = data[1]
print (pe.head(20))

data = get_data('INTL')
pe = data[1]
print (pe.head(20))
    