# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 18:28:44 2016

@author: donaldfung
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot_stock_price_data(dataframe):
    ax = dataframe.plot(title = "Stock Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()
    
def plot_selected_stocks(dataframe, columns, start_index, end_index):
    # Plot desired columns over index values in the given range
    plot_stock_price_data(dataframe.ix[start_index:end_index, columns], title = "Selected Data")
    
def plot_rolling_mean(dataframe, ticker, window):
    # Plot stock data
    ax = dataframe[ticker].plot(title = ticker + "rolling mean", label = ticker)
    # Computer rolling mean using an n-sized window
    rolling_mean = pd.rolling_mean(dataframe[ticker], window)
    # Add rolling mean to plot
    rolling_mean.plot(label = "Rolling mean", ax = ax)
    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc = "upper left")
    plt.show()
    
    
    