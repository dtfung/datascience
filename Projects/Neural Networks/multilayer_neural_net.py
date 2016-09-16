# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:23:12 2016

@author: donaldfung
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 20:10:19 2016

@author: donaldfung
"""
from numpy import array, exp, random, dot

class NeuralLayer():
    """Neural Network Layer
    
    inputs: 1). number of inputs per neuron,
            2). number of neurons in layer 
    """
    def __init__(self, inputs_per_neuron, neurons):
        self.synaptic_weights = self.__initialise_weights(inputs_per_neuron, neurons)
        
    def __initialise_weights(self, inputs_per_neuron, neurons):
        """ Randomly initialize weights"""
        random.seed(1)
        synaptic_weights = 2 * random.random((inputs_per_neuron, neurons)) - 1
        return synaptic_weights

class NeuralNetwork():
    """A single neuron neural network"""
    
    def __init__(self, number_of_layers):
        pass
        
    def initialize_layer(self):
        """Create a layer with random weights"""
        pass

    def __calc_weighted_sum(self, training_input):
        """Calculate the dot product"""
        x = dot(training_input, self.synaptic_weights)
        return x
        
    def __sigmoid_function(self, x):
        """
        Use sigmoid function to normalize output.
        
        function takes output as parameter   
        """
        normalized_output = 1 / (1 + exp(-x))
        return normalized_output
        
    def predict_output(self, training_input):
        """Predict output"""

        # get weighted sum
        x = self.__calc_weighted_sum(training_input)
        # normalize x using sigmoid function
        output = self.__sigmoid_function(x)
        return output
        
    def __sigmoid_curve_gradient(self, output):
        """Sigmoid Curve Gradient"""
        return output * (1 - output)
        
    def train(self, training_input, training_output, iterations):
        """Train neural network using back propagation"""

        for iteration in xrange(iterations):
            # train over n iterations
        
            # Step 1: Predict output
            output = self.predict_output(training_input)
            
            # Step 2: Calculate error
            error =  training_output - output
            
            # Step 3: Adjust weights
            sigmoid_curve_gradient = self.__sigmoid_curve_gradient(output)
            adj_weights = dot(training_input.T, error * sigmoid_curve_gradient)
            self.synaptic_weights += adj_weights
        
if __name__ == "__main__":
    """
    training set.  There are four examples, each consisting of 3 input values.
    There's one output
    """
    training_input = array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1], [0, 0, 0]])
    training_output = array([[0, 1, 1, 1, 1, 0, 0]]).T
    
    # Initialize layers with random weights
    layer_1 = NeuralLayer(inputs_per_neuron = 3, neurons = 4)
    layer_2 = NeuralLayer(inputs_per_neuron = 4, neurons = 1)
    
    # Initialize a single neuron neural network
    neural_network = NeuralNetwork()  
    
    # number of iterations
    iterations = 60000
    
    # train network
    neural_network.train(training_input, training_output, iterations)
    
    # Trained synaptic weights
    print neural_network.synaptic_weights
    
    # Predict output for test input
    test_input = array([[1, 1, 0]])
    print neural_network.predict_output(test_input)
    