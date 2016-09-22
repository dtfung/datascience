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
        self.weights = [np.random.randn(y, x) for x, y in zip(layers[:-1], layers[1:])]
        
    def fit(self, training_set, test_set, eta, batch_size, shuffle = False, epochs = 10):
        """This method is where the network training occurs.  If shuffle is set to True, the data is 
        shuffled.  It's then divided in mini-batches. Then we use feedforwarding and backpropagration to 
        update the weights and biases
        """ 
        if test_data: n_test = len(test_data)
            
        for i in xrange(epochs):
            # shuffle data set
            if shuffle == True:
                random.shuffle(training_set)
            # create mini batches
            mini_batches = [training_set[k:k + batch_size] for k in xrange(0, len(training_set), batch_size)]
            # update each mini batch
            for mini_batch in mini_batches:
                 self.update_mini_batch(mini_batch, eta)
                 
            if test_data:
                print "Epoch {0}: {1} / {2}".format(
                    i, self.evaluate(test_data), n_test)
            else:
                print "Epoch {0} complete".format(i)

    def update_mini_batch(self, mini_batch, eta):
        changed_biases = [np.zeros(b.shape) for b in self.biases] 
        changed_weights = [np.zeros(w.shape) for w in self.weights]
        
        for x, y in mini_batch:
            delta_w, delta_b = self.backpropagation(x, y)
            changed_biases = [b + changed_b for b, changed_b in zip(changed_biases, delta_b)]
            changed_weights = [w + changed_w for w, changed_w in zip(changed_weights, delta_w)]
        
        # using SGD, update weights and biases
        self.biases = [bias - eta/len(mini_batch) * new_bias for bias, new_bias in zip(self.biases, changed_biases)]
        self.weights = [weight - eta/len(mini_batch) * new_weight for weight, new_weight in zip(self.weights, changed_weights)]
                 
    def feedforward(self, x):
        """Here we compute the weighted output activations for an element through each layer"""
        zs = []
        activation = x
        activations = [x]
        for weight, bias in zip(self.weights, self.biases):
            z = np.dot(weight, activation) + bias
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
        return zs, activations
                 
    def sigmoid(self, z):
        return 1.0/(1.0 + np.exp(-z))
        
    def sigmoid_prime(self, z):
        """Derivative of the sigmoid function."""
        change_z = self.sigmoid(z)
        return change_z * (1 - change_z)
        
    def backpropagation(self, x, y):
        """After feedforwarding, we calculate the error in the output.
        This error is then backpropagated through all the previous layers.
        """
        delta_b = [np.zeros(b.shape) for b in self.biases] 
        delta_w = [np.zeros(w.shape) for w in self.weights]
        
        zs, activations = self.feedforward(x)
        # output error for last layer(output layer)
        delta = (activations[-1] - y) * self.sigmoid_prime(zs[-1])
        
        delta_b[-1] = delta
        delta_w[-1] = np.dot(delta, activations[-2].transpose())
        
        for l in xrange(2, len(self.layers)):
            delta = np.dot(self.weights[-l+1].transpose(), delta) * self.sigmoid_prime(zs[-l])
            delta_b[-l] = delta
            delta_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return delta_w, delta_b
        
    def evaluate(self, test_data):
        test_results = [(np.argmax(self.predict(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results) 
        
    def predict(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a)+b)
        return a
            
# get training, validation and test data
training_data, validation_data, test_data = assemble.load_data_wrapper()    

layers = [784, 30, 10]
mlp = NeuralNetwork(layers).fit(training_set = training_data, test_set = test_data, eta = 3.0, batch_size = 10, shuffle = True, epochs = 10)
#mlp = Network(layers).SGD(training_data, 30, 10, 3.0, test_data)


