# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:05:10 2016

@author: donaldfung

Contributors: Deepak Mahtani, Blayne Chong, Donald Fung
"""

import assemble
import settings
import model
import pandas as pd
import os
import numpy as np

def preprocess_data():
    
    # initialize company class
    company = assemble.CompanyData()
    
    # get price data
    price_data = company.get_wiki_data()
    
    # get fundamentals
    fundamentals_data = company.get_fundamentals()
    
    # rename columns
    fundamentals = (fundamentals_data.pipe(company.rename_columns))
    
    # date of first reported quarterly
    first_date = fundamentals.index[0]
    
    # combine dataframes
    df = (pd.concat([price_data, fundamentals], axis = 1)
                .pipe(company.remove_rows, first_date)
                .fillna(method = 'ffill')
                .pipe(company.calc_pe_ratio)
                .pipe(company.calc_book_value_pershare)
                .pipe(company.calc_pb_ratio)
                .pipe(company.calc_ps_ratio)
                .pipe(company.calc_pcashflow_ratio))
    
    # save
    df.to_csv("processed_data/df.csv", index = False)
    return df
    
if __name__ == "__main__":
    
    # if data exists, load it
    if os.path.isfile("processed_data/df.csv"):
        df = pd.read_csv("processed_data/df.csv", index_col=0)
        df.index = pd.to_datetime(df.index)
    else:
        df = preprocess_data()
        
    rl = model.Qlearning(alpha = settings.alpha, 
                         gamma = settings.gamma,
                         epsilon = settings.epsilon,
                         data = df).get_state()
    


    
    
                
