# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:17:36 2016

@author: donaldfung
"""

""" Use this file to interact with dataset

    Main uses include:
        1. Retrieving data from an external source
        2. Opening, updating, creating database or csv files
"""

from yahoo_finance import Share
import quandl
import settings
import plots
import computations
import prepare
import pandas as pd
import sqlite3

class Data(object):
    def __init__(self, company, storage_option):
        self.company = company
        self.storage_option = storage_option
        self.dataframe = None
        self.conn = None
        self.features = settings.features
        self.headers = settings.headers
        self.endpoints = settings.endpoints
        self.start_date = settings.start_date
        self.end_date = settings.end_date
        
    def get_data(self):
        try:
            self.dataframe = self.create_dataframe()
        except:
            print "error getting data"
            
    def create_dataframe(self):
        quandl.ApiConfig.api_key = settings.api_key
        price_enpoint = self.endpoints["Prices"]
        results = quandl.get(price_enpoint, start_date = self.start_date, end_date = self.end_date)
        df = results[["Adj. Close", "Adj. Volume"]]
        
        #rolling_mean =  # TODO: calculate rolling mean
        return df
        
    def save_data(self):
        if self.storage_option == "database":
            db = settings.stock_data_db
            self.conn = sqlite3.connect(db)
            # TODO: add column names
            self.dataframe.to_sql(db, self.conn)
        elif self.storage_option == "csv":
            # TODO: save dataframe to csv
            pass
class Database(object):
    def __init__(self):
        # declare properties
        self.database = settings.stock_data_db
        self.connection = sqlite3.connect(self.database)
        
    def retrieve_table(self, table):
        self.connection = sqlite3.connect(self.database)
        query = """CREATE TABLE IF NOT EXISTS {} (
        id INTEGER, 
        Symbol TEXT, 
        Adj_Close REAL,
        Volume REAL,
        PE_Ratio REAL, 
        Book_Value REAL, 
        PB_Ratio REAL,
        EPS REAL, 
        Net_Revenue REAL, 
        CurrentRatio REAL, 
        Debt_Equity_Ratio RATIO)""".format(table)
        try:
            self.connection.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError:
            print "table exists"
        query = "SELECT * FROM {t}".format(t = table)
        result = self.connection.execute(query)
        self.connection.close()
        return result
        
    def create_column(self):
        pass
    
    def create_table(self, name):
        self.connection = sqlite3.connect(self.database)
        """ Create new table with 'id' column """
        table_name = name
        new_field = 'id' # name of the column
        field_type = 'integer'  # column data type
        c = self.connection.cursor()
        c.execute('CREATE TABLE {tn} ({nf} {ft})'.format(tn=table_name, nf=new_field, ft=field_type))
        self.connection.commit()
        self.connection.close()
        
def create_csv_files():
    # Define data range
    start_date = settings.start_date
    end_date = settings.end_date
    # TODO: specify features and create files 
    """ NOTE: Code below creates csv file for closing prices only """
    dates = pd.date_range(start_date, end_date)
    # create empty dataframe with dates as index
    closing_prices = pd.DataFrame(index = dates)
    # dataframe of company name, ticker and industry
    companies = pd.read_csv(settings.companies_abridged)
    tickers = companies["Symbol"]
    name = companies["Name"]
    companies = dict(zip(name, tickers))
    # active data source
    datasource = settings.active_datasource
    
    for name, ticker in companies.items():
        print "getting stock data"
        try:
            data = get_data_from_datasource(datasource, ticker, start_date, end_date)
            closing_prices = adjusted_close(closing_prices, data, ticker, provider = datasource)
        except:
            print "Error getting data for ", name, ticker
    # fill in empty values
    closing_prices = prepare.fill_missing_values(closing_prices)
    # save dataframe
    save_dataframe(closing_prices)
    print "csv successfully saved!" 
        
def save_dataframe(df = None):
    closing_prices = settings.closing_prices_data + settings.csv
    df.to_csv(closing_prices, sep=',', encoding='utf-8')
    
def adjusted_close(df1, df2, ticker, provider):
    if provider == "Yahoo":
        # extract adjusted closing price 
        columns = ["Date", "Adj_Close"]
        df_temp = pd.DataFrame(df2, columns=columns)
        df_temp = df_temp.rename(columns = {"Adj_Close": ticker})
        # set index to be the date column
        df_temp = df_temp.set_index("Date")
        # join dataframes
        df1 = df1.join(df_temp, how = 'inner')
        # drop rows with NaN values
        #df1 = df1.dropna()
        df1 = prepare.fill_missing_values(df1)
    elif provider == "Quandl":
        columns = ["Adj. Close"]
        df_temp = pd.DataFrame(df2, columns=columns)
        df_temp = df_temp.rename(columns = {"Adj. Close": ticker})
        df1 = df1.join(df_temp, how = 'outer')
    return df1
    
if __name__ == "__main__":
    """ Takes a list of companies and gets data for them.  The data
    is then stored in a database for later use.  
    
    Input: A list of company stock ticker symbols
    """
    data = Data(settings.company, settings.storage_option)
    data.get_data()

#print data.median()
#plots.plot_rolling_mean(dataframe = data, ticker = "AAL", window = 20)
#plots.plot_stock_price_data(data)
#returns = computations.compute_daily_returns(data)
#data = computations.normalize_data(data)
#cum_returns = computations.compute_cumulative_returns(data, time = -20)
#print cum_returns