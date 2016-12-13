# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 00:20:45 2016

@author: donaldfung
"""

import settings
import pandas as pd
import numpy as np
import random

def load_files():
    """Read train and test files
    
    Return
    ======
    training data - A Pandas dataframe of shape (42,000, 785).  The first column, 'label'
    represents the digit drawn by the user).
    The remaining data represents the pixel values of each image.  
    
    test data - A Pandas dataframe of shape (28,000, 784).  The data represents the pixel values
    of each image
    """
    train = pd.read_csv(settings.training_data_filepath)
    test = pd.read_csv(settings.test_data_filepath)
    
    # get training, validation and testing data
    training_data, validation_data, test_data = preproccess_files(train, test)
    return training_data, validation_data, test_data 

def encode_data(i):
    """Convert label into a 10 dimensioanl vector"""
    e = np.zeros((10, 1))
    e[i] = 1.0
    return e
    
def preproccess_files(train, test):
    """The class label is found in the train file under the column called 'label'.  
    The Numpy representation of this column is extracted and assigned to a new 
    variable called 'class_labels'.  'class_labels' is then 
    encoded into a 10 dimensional np.ndarray of 0s and 1s.  The 'label' column is dropped from
    the train dataframe.  The Numpy representations of the train and test dataframes
    are normalized, and reshaped into 784 dimensional Numpy arrays.  A validation set is
    created from the training data.  It's approximately 20% the size of the training data.
    
    Return 
    =======
    training data - A list containing 33,600 tuples '(x, y)'. 'x' is a 784 dimensional np.ndarray
    containing the pixels of the input image.  The 'y' value is a 10 dimensional vector 
    representation of the digit drawn by the user.  
    
    validation data - A list containing 8,400 tuples '(x, y)'.  'x' is a 784 dimensional np.ndarray
    containing the pixels of the input image.  The 'y' value is a 10 dimensional vector 
    representation of the digit drawn by the user. 
    
    test data - A list containing 28,000 tuples '(x)'.  'x' is a 784 dimensional np.ndarray
    containing the pixels of the input image.  
    """
    
    # extract label
    class_labels = train["label"].values
    
    # encode label values
    class_labels = [encode_data(i) for i in class_labels]
    
    # drop label column
    train.drop(["label"], axis = 1, inplace = True)
    
    # shape
    cols = train.shape[1]
    
    # return Numpy representation of train and test dataframes 
    train = train.values
    test = test.values
    
    # normalize training and test data sets
    train = [x / np.linalg.norm(x) for x in train]
    test = [x / np.linalg.norm(x) for x in test]
    
    # reshape training and test datasets
    training_inputs = [np.reshape(x, (cols, 1)) for x in train]
    test_data = [np.reshape(x, (cols, 1)) for x in test]
    
    # now join class labels to training data
    training_data = zip(training_inputs, class_labels)
        
    # shuffle train set
    random.shuffle(training_data)
    
    # create validation set (20% of training set size)
    training_data = training_data[8400:]
    validation_data = training_data[:8400]
    
    return training_data, validation_data, test_data 