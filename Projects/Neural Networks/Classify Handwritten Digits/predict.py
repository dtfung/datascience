# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 10:33:03 2016

@author: donaldfung
"""

""" Attempt to classify handwritten digits from the MNIST data set using a multilayer perceptron (MLP).
    
    The MLP network layout
    ======================
    
    Input Layer: consists of 28 x 28 = 784 input neurons (encode a 28 x 28 greyscale image)
    Hidden Layers: 1 layer with 30 neurons
    Output Layer: 10 neurons

    Approach
    ========
    
    1. Initialize weights and biases using a Gaussian distribution
    2. Train over mini-batches (shuffle data first)
    3. Feedforward output (normalize output with Sigmoid function)
    4. Use backpropagation to calculate gradient of the cost function (or a change in weights and biases)
    5. Update weights and biases using stochastic gradient descent (SGD)
"""

import random
import numpy as np 
# The assemble file reads the MNIST dataset  
import assemble

class NeuralNetwork():
    
    def __init__(self, layers):
        """
        Notes on Layers
        ======
        The layers attribute is a list containing the number of layers in the network.  
        The number of neurons in each layers is equal to the value of each element in the array.
        
        Eg. layers = [784, 30, 10]
        - Object at index 0 is the input layer.  It contains 784 neurons.
        - Object at index 1 is the hidden layer.  It contains 30 neurons.
        - Object at index 2 is the output layer.  It contains 10 neurons.  
        
        Notes on Biases:
        ================
        The biases in each layer can be represented as a 1-dimensional array.
        The number of elements in this array is directly proportional to the number of neurons.  
        
        Eg.  Biases in the hidden layer == 30 because the hidden layer contains 30 neurons 
        
        Notes on Weights
        ================
        The weights connecting each layer is a matrix of n x m dimensions. 
        'n' refers to the number of neurons in the previous layer.  
        'm' refers to the number of neurons in the current layer.
        
        Eg. The weights connecting the input and hidden layer is a matrix of size 784 x 30.  
            The weights connecting the hidden layer to the output layer is a matrix of size 30 x 10
            
        Weights and biases are initialized randomly using a gaussian distribution
        """ 
        self.layers = layers
        self.biases = [np.random.randn(layer, 1) for layer in layers[1:]]
        self.weights = [np.random.rand(x, y) for x, y in zip(layers[:-1], layers[1:])]
        
    def fit(self, training_set, eta, batch_size, shuffle = False, epochs = 10):
        """This method is where the network training occurs.  If shuffle is set to True, the data is 
        shuffled.  It's then divided in mini-batches. Then we use feedforwarding and backpropagration to 
        update the weights and biases
        """        
        for i in xrange(epochs):
            if shuffle == True:
                np.random.shuffle(training_set)

            mini_batches = [training_set[k:k + batch_size] for k in xrange(0, len(training_set), batch_size)]
            
            for batch in mini_batches:
                 z = self.feedforward(batch)
                 
    def feedforward(batch):
        pass
            
            

# get training, validation and test data
training_data, validation_data, test_data = assemble.load_data_wrapper()    

layers = [784, 30, 10]
mlp = NeuralNetwork(layers).fit(training_set = training_data, eta = .1, batch_size = 10, shuffle = True, epochs = 10)
    


