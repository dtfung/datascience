# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:16:58 2016

@author: donaldfung
"""

import settings
import assemble
import Environment

class Q_Learning():
    def __init__(self):
        # Initialize variables here
        pass
    
    def update(self, state):
        # Get new state from environment
        pass

def run():
    #   Get stock price data
    data = assemble.Data(settings.company, settings.storage_option)
    df = data.create_dataframe()
    #   Setup environment
    env = Environment.Market()
    env.get_financials(df)
if __name__ == "__main__":
    run()
    