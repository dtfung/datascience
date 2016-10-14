# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:05:10 2016

@author: donaldfung

Contributors: Deepak Mahtani, Blayne Chong, Donald Fung
"""

import assemble
import pandas as pd

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
                .pipe(company.calc_pcashflow_ratio)
                .pipe(company.normalize)
                )
    return df
    
def partition(df):
    # get size of train and test sets
    train_size = int(df.shape[0] * 0.8)
    test_size = int(df.shape[0] * 0.1)
    
    train = df.iloc[:train_size]
    validation = df.iloc[train_size:train_size + test_size]
    test = df.iloc[-test_size:]
    return train, validation, test
    
    
def predict(df):
    
    # partition data
    train, validation, test = partition(df)

if __name__ == "__main__":
    
    df = preprocess_data()
    predict(df)


    
    
                
