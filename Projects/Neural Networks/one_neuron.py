# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 20:10:19 2016

@author: donaldfung
"""
from numpy import array, exp, random, dot


class NeuralNetwork():
    """A single neuron neural network"""
    
    def __init__(self):
        """ Randomly initialize weights"""
        random.seed(1)
        self.synaptic_weights = 2 * random.random((3, 1)) - 1
        
        # training set inputs
        self.training_input = None
        # training set ouput
        self.training_output = None
        
    def __calc_weighted_sum(self):
        """Calculate the dot product"""
        x = dot(self.training_input, self.synaptic_weights)
        return x
        
    def __sigmoid_function(self, x):
        """
        Use sigmoid function to normalize output.
        
        function takes output as parameter   
        """
        normalized_output = 1 / (1 + exp(-x))
        return normalized_output
        
    def __predict_output(self):
        """Predict output"""

        # get weighted sum
        x = self.__calc_weighted_sum()
        # normalize x using sigmoid function
        output = self.__sigmoid_function(x)
        return output
        
    def train(self, training_input, training_output, iterations):
        """Train neural network using back propagation"""

        # assign value to training set property
        self.training_input = training_input  
        
        # assign value to output property
        self.training_output = training_output
        
        # Step 1: Predict output
        output = self.__predict_output()
        
        # Step 2: Calculate error
        


if __name__ == "__main__":
    """
    training set.  There are four examples, each consisting of 3 input values.
    There's one output
    """
    training_input = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    training_output = array([[0, 1, 1, 0]]).T
    
    # Initialise a single neuron neural network
    neural_network = NeuralNetwork()  
    
    # number of iterations
    iterations = 100
    
    # train network
    neural_network.train(training_input, training_output, iterations)
    