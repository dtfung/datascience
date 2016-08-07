# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:09:17 2016

@author: donaldfung
"""

""" STORE ALL FILE NAMES HERE """
import key

# data 
data_dir = "data"


# parameters

# stock ticker
ticker = "AAPL"

""" QUANDL DATABASES """

""" Wiki EOD Stock Prices 
End of day stock prices, dividends and splits for 3,000 US companies, 
curated by the Quandl community and released into the public domain 
"""
wiki = "WIKI/"

""" Core US Fundamentals Data

7,000+ companies, point-in-time, inc/exc restatements, active/delisted,
up to 11 years history, 101 indicators, expanding coverage, daily updates.
"""
sf1 = "SF1/"

# API Key
api_key = key.get_key() 

""" QUANDL CODES """

# stock price code
stock_price_code = wiki + ticker
# PE ratio code
pe_ratio_code = sf1 + ticker + "_PE1_MRT"


