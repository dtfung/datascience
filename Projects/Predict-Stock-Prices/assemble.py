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

class Data():
    def __init__(self, company, storage_option):
        self.company = company
        self.storage_option = storage_option
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
        
if __name__ == "__main__":
    data = Data(settings.company, settings.storage_option)
    data.get_data()