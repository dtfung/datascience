# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 10:33:03 2016

@author: donaldfung
"""

""" Attempt to classify handwritten digits from the MNIST data set using a multilayer perceptron (MLP).
    
    The MLP network layout
    ______________________
    
    Input Layer: consists of 28 x 28 = 784 input neurons (encode a 28 x 28 greyscale image)
    Hidden Layers: 1 layer with 30 neurons
    Output Layer: 10 neurons

    Approach
    ________
    
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
        self.layers = layers


# get training, validation and test data
training_data, validation_data, test_data = assemble.load_data_wrapper()    
    


