# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 17:36:43 2016

@author: donaldfung
"""
import weightInit
import numpy as np
import costFunctions
import matplotlib.pyplot as plt
import pandas as pd

class MultilayerPerceptron():
    
    def __init__(self, layers):
        """Initialize weights, biases and layers"""
        self.weights, self.biases = weightInit.RandomGaussian().init_w_and_b(layers)
        self.layers = layers
        
    def fit(self, training_set, test_set, val_set, use_test_set, eta, mini_batch_size, epochs, shuffle):
        """Shuffle and split training data into mini batches.  Then begin the training process"""
        

        if use_test_set == True:
            # join val set to test set
            training_set += val_set
            
        cost = []        
        # shuffle training set
        for i in xrange(0, epochs):
            if shuffle == True:
                np.random.shuffle(training_set)
            
            # create mini-batches
            batches = [training_set[batch:batch + mini_batch_size] for batch in xrange(0, len(training_set), mini_batch_size)]
            
            # loop over mini-batches
            for batch in batches:
                self.update_batch(batch, eta)
                
            if use_test_set == False:
                # Evaluate cost
                cost.append(self.calc_cost(val_set))
                print "cost added"
                
        if use_test_set == True:
            self.evaluate(test_set)
        else:
            plt.plot(range(0, epochs), cost)
            plt.title("Cost over time")
            plt.xlabel('Epochs')
            plt.ylabel('Cost')
            plt.show()
            
    def update_batch(self, batch, eta):
        # create empty list to store the weight and bias updates
        delta_weights = [np.zeros(weight.shape) for weight in self.weights]
        delta_biases = [np.zeros(bias.shape) for bias in self.biases]
        
        # loop over mini-batch
        for x, y in batch:
            # get output
            a, z = self.feedforwarding(x, y)
            # get change in weights and biases
            delta_w, delta_b = self.backpropagation(a, y, z)
            # add small change in weight and bias
            delta_weights = [weight + w for weight, w in zip(delta_weights, delta_w)]
            delta_biases = [bias + b for bias, b in zip(delta_biases, delta_b)]
            
        # update weights and biases 
        self.biases = [bias - eta/len(batch) * new_bias for bias, new_bias in zip(self.biases, delta_biases)]
        self.weights = [weight - eta/len(batch) * new_weight for weight, new_weight in zip(self.weights, delta_weights)]
        
    def feedforwarding(self, x, y):
        zs = []
        activation = x
        activations = [x]
        for weight, bias in zip(self.weights, self.biases):
            z = np.dot(weight, activation) + bias
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
        return activations, zs
        
    def sigmoid(self, z):
        """ Sigmoid function"""
        a = 1.0/(1.0 + np.exp(-z))
        return a    

    def backpropagation(self, a, y, z):
        """Using z and a, we can calculate error and backpropagate the error 
        through the network"""
        
        # create empty list to store the weight and bias updates
        delta_weights = [np.zeros(weight.shape) for weight in self.weights]
        delta_biases = [np.zeros(bias.shape) for bias in self.biases]
        
        # error in output layer 
        delta = costFunctions.QuadraticCost().current_layer_delta(a[-1], y, z[-1])
        delta_weights[-1] = np.dot(delta, a[-2].transpose())
        delta_biases[-1] = delta
        
        # backprop error
        for l in range(2, len(self.layers)):
            delta = costFunctions.QuadraticCost().previous_layer_delta(delta, z[-l], self.weights[-l + 1])
            delta_weights[-l] = np.dot(delta, a[-l - 1].transpose())
            delta_biases[-l] = delta
            
        return delta_weights, delta_biases
        
    def predict(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a)+b)
        return a
        
    def calc_cost(self, data):
        cost = 0.0
        for x, y in data:
            a = self.predict(x)
            cost += costFunctions.QuadraticCost().calc_cost(a, y)/len(data)
        return cost
        
    def evaluate(self, test_data):
        test_results = [np.argmax(self.predict(x)) for x in test_data]
        
        # save results
        d = {'Label': test_results}
        df = pd.DataFrame(d)
        
        # set index
        df.index = np.arange(1, len(test_results) + 1)
        
        # rename index
        df.index.name = 'ImageId'
        df.to_csv("results")
        return test_results
        