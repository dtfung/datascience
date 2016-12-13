# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 01:30:28 2016

@author: donaldfung
"""

import assemble
import model

def run():
    
    # get data
    training_data, validation_data, test_data = assemble.load_files()
    
    # layers
    layers = [784, 30, 10]
    # initialize neural network
    mlp = model.MultilayerPerceptron(layers)
    mlp.fit(training_set = training_data, 
            test_set = test_data,
            val_set = validation_data,
            use_test_set = True,
            eta = 3.0,
            mini_batch_size = 10,
            epochs = 50,
            shuffle = True)

if __name__ == "__main__":
    
    run()
    