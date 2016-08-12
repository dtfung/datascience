# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 12:05:10 2016

@author: donaldfung
"""
import assemble
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

class Model():
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        
    def predict(self):
        lr = LinearRegression()
        lr.fit(self.X_train, self.y_train)
        y_train_pred = lr.predict(self.X_train)
        y_test_pred = lr.predict(self.X_test)
        train_error = mean_absolute_error(self.y_train, y_train_pred)
        test_error = mean_absolute_error(self.y_test, y_test_pred)
        print test_error
        print train_error
 

def run():
    data = assemble.Data()
    data.read()
    
if __name__ == "__main__":
     run()