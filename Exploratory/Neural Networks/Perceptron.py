# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 22:23:19 2016

@author: donaldfung
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 20:10:19 2016

@author: donaldfung
"""
import numpy as np
import pandas as pd

class Perceptron():
    """A Perceptron model
    
    Mimics a single nueron in the brain    
    """
    def __init__(self, eta, n_iter):
        # learning rate
        self.eta = eta
        
        # iterations
        self.n_iter = n_iter

    def __calc_weighted_sum(self, training_input):
        """Calculate the dot product"""
        x = np.dot(training_input, self.synaptic_weights_[1:] + self.synaptic_weights_[0])
        return x
        
    def predict(self, training_input):
        """Predict output"""

        # get weighted sum
        x = self.__calc_weighted_sum(training_input)
        predictions = np.where(x >= 0.0, 1, -1)
        return predictions
        
    def fit(self, X, y):
        """Train neural network"""
        
        # Randomly initialize weights
        self.synaptic_weights_ = np.zeros(1 + X.shape[1])
        
        # errors
        self.errors_ = []

        # train over n iterations
        for iteration in xrange(self.n_iter):
            cum_error = 0
            for xi, target in zip(X, y):
                # Step 1: Predict output
                output = self.predict(xi)
                
                # Step 2: Calculate error
                error =  target - output
            
                # Step 3: Adjust weights
                update = (self.eta * error)
                cum_error += int(update != 0.0)
                self.synaptic_weights_[1:] += update * xi
                self.synaptic_weights_[0] += update
            self.errors_.append(cum_error)
        
def load_dataset():
    """Load Iris dataset"""
    
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data")
    # extract only data for Versicolor and Setosa for testing
    y = df.iloc[0:100, 4].values
    y = np.where(y == "Iris-Versicolor", 1, -1)
    X = df.iloc[0:100, [0, 2,]].values
    return X, y
        
if __name__ == "__main__":
 
    # Load Iris Dataset
    X, y = load_dataset()
    
    # number of iterations
    iterations = 10
    
    # eta / learning rate
    lr = 0.1
    
    # Initialise a single neuron neural network
    nn = Perceptron(eta = lr, n_iter = iterations)  
    
    # train network
    nn.fit(X, y) 
    
    # plot graph of miscalculations
    import matplotlib.pyplot as plt
    plt.plot(range(1, len(nn.errors_) + 1), nn.errors_, marker = 'o')
    plt.xlabel("Epochs")
    plt.ylabel("Errors")
    plt.show()
    
    