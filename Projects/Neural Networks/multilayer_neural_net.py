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
        self.synaptic_weights = self.__initialize_weights(inputs_per_neuron, neurons)
        
    def __initialize_weights(self, inputs_per_neuron, neurons):
        """ Randomly initialize weights"""
        random.seed(1)
        synaptic_weights = 2 * random.random((inputs_per_neuron, neurons)) - 1
        return synaptic_weights

class NeuralNetwork():
    """A Multi-Layer Neural Network"""
    
    def __init__(self, layer1, layer2):
        self.layer1 = layer1
        self.layer2 = layer2
        
    def __sigmoid_function(self, x):
        """
        Use sigmoid function to normalize output.
        
        function takes output as parameter   
        """
        normalized_output = 1 / (1 + exp(-x))
        return normalized_output
        
    def predict_output(self, training_input):
        """Predict output"""
        # normalize x using sigmoid function
        output1 = self.__sigmoid_function(dot(training_input, self.layer1.synaptic_weights))
        # layer2's input is the output of layer1
        output2 = self.__sigmoid_function(dot(output1, self.layer2.synaptic_weights))
        return output1, output2
        
    def __sigmoid_curve_gradient(self, output):
        """Sigmoid Curve Gradient"""
        return output * (1 - output)
        
    def train(self, training_input, training_output, iterations):
        """Train neural network using back propagation"""

        for iteration in xrange(iterations):
            # get outputs.  
            output1, output2 = self.predict_output(training_input)
            
            # Layer 2 error 
            error2 = training_output - output2
            sigmoid_curve_gradient2 = self.__sigmoid_curve_gradient(output2)
            # change 
            delta2 = error2 * sigmoid_curve_gradient2
            
            # Layer 1 error
            error1 = dot(delta2, self.layer2.synaptic_weights.T)
            sigmoid_curve_gradient1 = self.__sigmoid_curve_gradient(output1)
            # change
            delta1 = error1 * sigmoid_curve_gradient1
        
            self.layer1.synaptic_weights += dot(training_input.T, delta1)
            self.layer2.synaptic_weights += dot(output1.T, delta2)
        
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
    neural_network = NeuralNetwork(layer_1, layer_2)  
    
    # number of iterations
    iterations = 60000
    
    # train network
    neural_network.train(training_input, training_output, iterations)
    
    # Trained synaptic weights
    
    # Predict output for test input
    test_input = array([[1, 1, 0]])
    hidden_layer, output =  neural_network.predict_output(test_input)
    print output
    