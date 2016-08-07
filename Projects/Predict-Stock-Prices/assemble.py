# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:17:36 2016

@author: donaldfung
"""

""" Retrieve and process raw data and create csv and sqlite database"""

from yahoo_finance import Share
import settings
import pandas as pd
from sklearn import preprocessing
import sqlite3

def get_data():
    # check if csv exists
    closing_prices = settings.closing_prices_data
    try:
        data = pd.read_csv(closing_prices)
        if data:
            print "successfully loaded closing prices!"
            return data
    except:
        print "no csv file"
        
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
    # save dataframe
    save_dataframe(closing_prices)
    print "csv successfully saved!"
    # save database
    #create_database(closing_prices)
    #print "databased successfully saved!"  
    return closing_prices
    
def normalize_data(df = None):
    x = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    return df
    
def save_dataframe(df = None):
    closing_prices = settings.closing_prices_data + settings.csv
    df.to_csv(closing_prices, sep='\t', encoding='utf-8')

def create_database(df = None):
    closing_prices = settings.closing_prices_data + settings.sql
    conn = sqlite3.connect(closing_prices)
    df.to_sql(closing_prices, conn)
    
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

