#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 15:28:21 2016

@author: donaldfung
"""

import sqlite3
import pandas as pd
import settings

class Database(): 
    def check_table_exists(self, company_info):
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        query = "SELECT * FROM " + table_name
        try:
            results = c.execute(query).fetchall()
            conn.close()
            return results
        except:
            return None
    
    def date_last_updated(self, company_info):
        """Gets the date that the table was last updated"""
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        query = "SELECT Date FROM " + table_name
        dates = c.execute(query).fetchall()
        last_date = dates[-1][0]
        conn.close()
        return last_date
        
    def create(self, company_info):
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        query = """CREATE TABLE """ + table_name + """(
        Date text,
        Share_Price float,
        Net_Income float,
        COGS float,
        Gross_Profit float,
        Research_And_Development float,
        Revenue float,
        EPS float, 
        DPS float,
        Shares_Outstanding float,
        Cash float,
        Current_Assets float,
        Intangibles float, 
        Total_Assets float,
        Current_Liabilities float,
        Long_Term_Debt float,
        Retained_Earnings float,
        Total_Liabilities float,
        Long_Term_Liabilities float,
        Stockholders_Equity float,
        Current_Ratio float,
        PE_Ratio float,
        PB_Ratio float,
        Debt_to_Equity_Ratio float,
        Book_Value_Per_Share float
        );"""
        try:
            c.execute(query)
            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            pass
        
    def fetch(self, company_info):
        """Get data from database"""
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        query = "SELECT * from " + table_name
        data = c.execute(query).fetchall()
        df = self.prepare_fetched_data(data)
        conn.close()
        return df
        
    def prepare_fetched_data(self, data):
        """Fetching data returns a tuple of values from the database.  We will need
        to put this data into a dataframe to be able to use it"""
        # get original list of columns
        cols = settings.sf1_columns[:]
        # add ratio column labels to this list
        cols.extend(["PE Ratio", "Book Value/Share", "PB Ratio", "NC Debt:Equity Ratio"])
        # date
        cols.insert(0, "Date")
        # create dataframe
        df = pd.DataFrame.from_records(data = data)
        # old cols
        old_cols = df.columns
        df.rename(columns=dict(zip(old_cols, cols)), inplace=True)
        df.set_index("Date", inplace = True)
        return df
        
    def insert(self, company_info, financials):
        """Insert new record into database"""
        self.create(company_info)
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        for index, row in financials.iterrows():
            query = """INSERT INTO """ + table_name + """ VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            args = (
                    index.strftime("%Y/%m/%d"),
                    row["Share Price"],
                    row["Net Income"],
                    row["Cost of Goods Sold"],
                    row["Gross Profit"],
                    row["R&D"],
                    row["Revenue"],
                    row["EPS"],
                    row["DPS"],
                    row["Shares Outstanding"],
                    row["Cash"],
                    row["Current Assets"],
                    row["Intangibles"],
                    row["Total Assets"],
                    row["Current Liabilities"],
                    row["Long Term Debt"],
                    row["Retained Earnings"],
                    row["Total Liabilities"],
                    row["Long Term Liabilities"],
                    row["Stockholders Equity"],
                    row["Current Ratio"],
                    row["PE Ratio"],
                    row["PB Ratio"],
                    row["NC Debt:Equity Ratio"],
                    row["Book Value/Share"]
                    )
            c.execute(query, args)
        conn.commit()
        conn.close()
        
    def update(self, company_info):
        """Update company with new data"""
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        query = "UPDATE " + table_name
        c.execute(query)
        conn.commit()
        conn.close()
        
    def delete(self, company_info):
        conn = sqlite3.connect("Company.sqlite")
        c = conn.cursor()
        table_name = self.select_ticker(company_info)
        query = "DELETE from " + table_name
        c.execute(query)
        conn.commit()
        conn.close()
        
    def select_ticker(self, company_info):
        """Returns the ticker to be used as the table name.
        Also handles cases where a ticker symbol may conflict with SQL query statements"""
        if company_info["Ticker"] in ["ALL", "ELSE"]:
            return settings.conflicting_tickers[company_info["Ticker"]]
        else:
            return company_info["Ticker"]

        
        