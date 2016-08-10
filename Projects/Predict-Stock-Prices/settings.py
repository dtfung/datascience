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
stock_data_db = data_dir + "stockdata" + sql

# database headers
headers = ["id", "Date", "Symbol", "Adj_Close", "Volume",
           "PE_Ratio", "Book_Value", "PB_Ratio", "EPS", 
           "Net_Rev", "Current_Ratio", "Debt_Equity_Ratio"]

# dataframe features
features = ["Adj. Close", "Adj. Volume",
           "PE_Ratio", "Book_Value", "PB_Ratio", "EPS", 
           "Net_Rev", "Current_Ratio", "Debt_Equity_Ratio"]

# a dataset containing ticker, name and sector of all companies listed on the snp500
companies_abridged = data_dir + "constituents.csv"
# data from the above dataset + fundamentals incl pe ratio, earnings per share, book value
companies_detailed = data_dir + "constituents-financials.csv"

# companies to be used in building dataset and training model
company = "INTC" # for now, let's use Intel Corp 

# data ranges
start_date = "2010-01-01"
end_date = "2016-07-31"

# choose data source
datasources = ["Yahoo", "Quandl"]
active_datasource = datasources[1]

# storage options - Use "database" or "csv"
storage_options = ["database", "csv"]
storage_option = storage_options[0]

# how many bins to divide data
steps = 10
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

""" Endpoints 
NOTE:  that endpoints for adj.close and volume are the same
"""
# feature endpoints.  Endpoint for adj.close and volume is the same         
endpoints = {
    "Prices":stock_price_code + company, 
    "PE_Ratio": sf1 + company + "_PE1_MRT",
    "Book_Value": sf1 + company + "_BVPS_ARQ",
    "PB_Ratio": sf1 + company + "_PB_ARQ",
    "EPS": sf1 + company + "_EPSDIL_ARQ",
    "Net_Income": sf1 + company + "_NETINC_ARQ",
    "Current_Ratio": sf1 + company + "_CURRENTRATIO_ARQ",
    "Debt_Equity": sf1 + company + "_DE_ARQ"
             }
"""
-----------------------------------------------------------------------

""" 
"""
YAHOO FINANCE

link: https://pypi.python.org/pypi/yahoo-finance/1.1.4
"""




