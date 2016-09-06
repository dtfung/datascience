# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 01:21:35 2016

@author: donaldfung
"""

import settings
import pandas as pd

class Preprocessing():
    
    def __init__(self):
        self.data = None
        self.columns = settings.columns
        
    def read_file(self):
        self.data = pd.read_csv(settings.filename, names = self.columns)
        
    def convert_categorical_variables(self):
        for item in self.columns:
            col = pd.Categorical.from_array(self.data[item])
            self.data[item] = col.codes
            
     
        