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
    
    def __init__(self, company_name):
        """Assign attributes here"""
        self.company_name = company_name
        self.wiki_dbname = 'WIKI/'
        
        # get quandl key
        quandl.ApiConfig.api_key = quandlManager.key
    
    def get_wiki_data(self):
        """Returns a dataframe of stock price data
        
        We use the Wiki EOD Stock Price database found on Quandl
        
        Columns returned
        ================
        Date(Index), Volume, Adj. Close, 
        """
        data = quandl.get(self.wiki_dbname + settings.company_ticker)
        df = data[settings.wiki_columns]
        return data