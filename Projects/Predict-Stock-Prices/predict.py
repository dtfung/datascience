# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:05:10 2016

@author: donaldfung

Contributors: Deepak Mahtani, Blayne Chong, Donald Fung
"""

import assemble
import settings
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
                .pipe(company.calc_pcashflow_ratio))
    return df
    
def partition(df):
    # get size of train and test sets
    train_size = int(df.shape[0] * 0.8)
    test_size = int(df.shape[0] * 0.1)
    
    train = df.iloc[:train_size]
    validation = df.iloc[train_size:train_size + test_size]
    test = df.iloc[-test_size:]

    # target label valus
    y_train = train.loc[:, ("Adj. Close")]
    y_val = validation.loc[:, ("Adj. Close")]
    y_test = test.loc[:, ("Adj. Close")]
                      
    # feature data
    X_train = train.drop("Adj. Close", axis = 1)
    X_val = validation.drop("Adj. Close", axis = 1)
    X_test = test.drop("Adj. Close", axis = 1)
    return X_train, y_train, X_val, y_val, X_test, y_test
    
def feature_scale(X_train, X_val, X_test):
    "Normalize all columns"""
    from sklearn.preprocessing import MinMaxScaler
    mms = MinMaxScaler()
    
    X_train_std = mms.fit_transform(X_train)
    X_val_std = mms.fit_transform(X_val)
    X_test_std = mms.fit_transform(X_test)
    return X_train_std, X_val_std, X_test_std
    
    
def predict(df):
    
    # partition data
    X_train, y_train, X_val, y_val, X_test, y_test = partition(df)
    
    # normalize features
    X_train_std, X_val_std, X_test_std = feature_scale(X_train, X_val, X_test)
     
    
    # get time frame
    time_frame = settings.time_frame
    print time_frame
    

if __name__ == "__main__":
    
    df = preprocess_data()
    predict(df)


    
    
                
