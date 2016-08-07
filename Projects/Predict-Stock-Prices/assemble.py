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
    
    count = 0
    for name, ticker in companies.items():
        if count < 2:
            # get stock data from YAHOO!
            yahoo = Share(ticker)
            historical_data = yahoo.get_historical(start_date, end_date)
            # create a dataframe with this data
            df2 = pd.DataFrame(data = historical_data)
            closing_prices = adjusted_close(closing_prices, df2, ticker)
            
            count += 1
    closing_prices = normalize_data(closing_prices)
    return closing_prices
    
def normalize_data(df = None):
    #first = df.iloc[[0]].values
    
    #print first
    #df = df / first
    from sklearn import preprocessing

    x = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
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
print data[:100]
print data.shape
