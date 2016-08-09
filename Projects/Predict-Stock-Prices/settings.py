# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:09:17 2016

@author: donaldfung
"""

""" GENERAL SETTINGS """
import key

# data directory
data_dir = "data/"

# file extensions
csv = ".csv"
sql = ".db"

# csv filenames
stock_data_csv = data_dir + "closing_prices" + csv

# csv filenames in list
list_of_csv_filenames = [stock_data_csv]

# database filename
stock_data_db = data_dir + "stock-data" + sql

# a dataset containing ticker, name and sector of all companies listed on the snp500
companies_abridged = data_dir + "constituents.csv"
# data from the above dataset + fundamentals incl pe ratio, earnings per share, book value
companies_detailed = data_dir + "constituents-financials.csv"

# companies to be used in building dataset and training model
companies = ["INTC, GM"] # for now, let's use Intel Corp and General Motors

# data ranges
start_date = "2010-01-01"
end_date = "2016-07-31"

# choose data source
datasources = ["Yahoo", "Quandl"]
active_datasource = datasources[1]

# storage options - Use "database" or "csv"
storage_options = ["database", "csv"]
storage_option = storage_options[0]


""" 
----------------------------------------------------------------------
QUANDL DATABASES """

# API Key
api_key = key.get_key() 

""" Wiki EOD Stock Prices 
End of day stock prices, dividends and splits for 3,000 US companies, 
curated by the Quandl community and released into the public domain 
"""
stock_price_code = "WIKI/"

""" Core US Fundamentals Data

7,000+ companies, point-in-time, inc/exc restatements, active/delisted,
up to 11 years history, 101 indicators, expanding coverage, daily updates.
"""
sf1 = "SF1/"

"""
-----------------------------------------------------------------------

""" 
"""
YAHOO FINANCE

link: https://pypi.python.org/pypi/yahoo-finance/1.1.4
"""



""" QUANDL CODES """
"""
# PE ratio code
pe_ratio_code = sf1 + ticker + "_PE1_MRT"
# enterprise value code
ev_code = sf1 + ticker + "_EV"
# ebitda code
ebitda_code = sf1 + ticker + "_EBITDA_ART"
# eps code
eps_code = sf1 + ticker + "_EPSGROWTH1YR_ART"
# dividends per share
dps_code = sf1 + ticker + "_DPS_MRT"

# 2-day net price change
# 10-day volatility
# 50-day oving avg
# 10-day moving avg
# quick ratio
"""




