# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 19:42:27 2016

@author: donaldfung
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 18:09:48 2016

@author: donaldfung
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Adaline():
    """An Adaptive Linear Neuron (Adaline)
    
    Inputs:
        Learning rate (eta)
        Number of epochs
        
    Output: 
        Binary class predictions 
    """    
    def __init__(self, eta, n_epochs, shuffle):
        self.eta = eta
        self.n_epochs = n_epochs
        self.avg_cost = []
        self.shuffle = shuffle
        
    def fit(self, X, y):
        """Train Adaline
        
        1). Use linear activation function to predict outputs
        2). A cost function introduced.  We will attempt to minimize this
        3). Update weights using Batch Gradient Descent
        """
        # initialize weights to zero
        self.weights_ = np.zeros(1 + X.shape[1])
        
        for i in xrange(self.n_epochs):
            # shuffle data
            if self.shuffle == True:
                X, y = self._shuffle(X, y)
                
            cost = []
            for xi, yi in zip(X, y):
                # predict output
                output = self.predict(xi)
                
                # calculate error
                error = yi - output
                
                # calculate weight change
                update = self.eta * xi.dot(error)
                
                # update weights
                self.weights_[1:] += update
                self.weights_[0] += self.eta * error
                
                # update cost 
                cost.append((error**2) / 2.0)
            # calculate average cost per epoch
            self.avg_cost.append(sum(cost) /len(cost))
        return self
    
    def predict(self, X):
        # find dot product
        z = np.dot(X, self.weights_[1:]) + self.weights_[0]
        
        # return 1 if dot wi * xi > 0, else return -1
        #z = np.where(z >= 0.0, 1, -1)
        return z
        
    def _shuffle(self, X, y):
        r = np.random.permutation(len(X))
        X = X[r]
        y = y[r]
        return X, y
          
def read_file():
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data")
    return df
    
if __name__ == "__main__":
    
    # Read Iris data set
    df = read_file()
    X = df.iloc[:100, [0, 2]].values
    y = df.iloc[:100, 4].values
    y = np.where(y == "Iris-Versicolor", 1, -1)
    
    # learning rate
    eta = .01
    n_epochs = 12
    
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (8,4))
    ada1 = Adaline(eta = .01, n_epochs = 10, shuffle = True).fit(X, y)
    ax[0].plot(range(1, len(ada1.avg_cost) + 1), np.log10(ada1.avg_cost), marker = 'o')
    ax[0].set_xlabel('Epochs')
    ax[0].set_ylabel('log(Sum-squared-error)')
    ax[0].set_title('Adaline - Learning Rate  0.01')
    
    ada2 = Adaline(eta = 0.0002, n_epochs = 10, shuffle = True).fit(X, y)
    ax[1].plot(range(1, len(ada2.avg_cost) + 1), np.log10(ada2.avg_cost), marker = 'o')
    ax[1].set_xlabel('Epochs')
    ax[1].set_ylabel('log(Sum-Squared-error)')
    ax[1].set_title('Adaline - Learning Rate 0.0002')
    plt.show()