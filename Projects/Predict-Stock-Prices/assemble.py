# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:17:36 2016

@author: donaldfung
"""

""" Retrieve and process raw data and create csv and sqlite database"""

from yahoo_finance import Share
import settings
import pandas as pd

def get_data():
    
    # Define data range
    start_date = settings.start_date
    end_date = settings.end_date
    dates = pd.date_range(start_date, end_date)
    
    # create empty dataframe with dates as index
    closing_prices = pd.DataFrame(index = dates)
    
    # dataframe of company name, ticker and industry
    companies = pd.read_csv(settings.companies_abridged)
    tickers = companies["Symbol"]
    name = companies["Name"]
    companies = dict(zip(name, tickers))
    
    for name, ticker in companies.items():
        
        # get stock data from YAHOO!
        yahoo = Share(ticker)
        historical_data = yahoo.get_historical(start_date, end_date)
        
        # create a dataframe with this data
        df2 = pd.DataFrame(data = historical_data)
        
        closing_prices = adjusted_close(closing_prices, df2, ticker)
    
    return closing_prices
    
def normalize_data(df = None):
    
    df = df / df.ix[0, :]
    return df
    
def adjusted_close(df1 = None, df2 = None, ticker = None):
    
    # extract adjusted closing price 
    columns = ["Date", "Adj_Close"]
    df_temp = pd.DataFrame(df2, columns=columns)
    df_temp = df_temp.rename(columns = {"Adj_Close": ticker})
    
    # set index to be the date column
    df_temp = df_temp.set_index("Date")

    # join dataframes
    df1 = df1.join(df_temp, how = 'inner')
    
    # drop rows with NaN values
    df1 = df1.dropna()
    return df1
    
    
data = get_data()
print data[:1000]
print data.shape
