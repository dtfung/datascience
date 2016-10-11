# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:41:52 2016

@author: donaldfung

Contributors: Deepak Mahtani, Blayne Chong, Donald Fung
"""
import quandl
import quandlManager
import settings

class CompanyData():
    
    def __init__(self):
        """Assign attributes here"""

        # get quandl key
        quandl.ApiConfig.api_key = quandlManager.key
    
    def get_wiki_data(self):
        """Returns a dataframe of stock price data
        
        We use the Wiki EOD Stock Price database found on Quandl
        
        Columns returned
        ================
        Date(Index), Volume, Adj. Close, 
        """
        data = quandl.get(settings.wiki_dbname + settings.company_ticker,
                          start_date = settings.start_date,
                          end_date = settings.end_date)
        # filter columns
        df = data[settings.wiki_columns]
        return df
        
    def get_fundamentals(self):
        """Returns a dataframe containing stock fundamentals.
        
        Check settings.py for the full list         
        """
        # get data
        data = quandl.get(settings.sf1_codes,
                          start_date = settings.start_date,
                          end_date = settings.end_date)
        return data
    
    def rename_columns(self, df):
        """Rename columns.  Quandl returns some default column names, but
        we replace these with custom ones found in settings.py"""
        df = df.copy()
        # get columns
        cols = df.columns
        new_columns = {}
        # pair old column names with new ones
        for i, col in enumerate(cols):
            new_columns[col] = settings.sf1_columns[i]
        # rename columns
        df.rename(columns = new_columns, inplace = True)
        return df
        
    def cal_pe_ratio(self, df):
        """Calculate the price to earnings ratio
        
        Formula: current price/last reported eps figure
        """
        #TODO: apply formula
        pass
        