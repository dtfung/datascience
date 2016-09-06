# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 01:01:44 2016

@author: donaldfung
"""

""" Decision Trees """
import assemble
import pandas as pd
import numpy as np
import math
import settings

class DecisionTree():
    def __init__(self, data):
        self.data = data
        
    def calc_entropy(self, column):
        counts = np.bincount(column)
        probabilities = counts / float(len(column))
        entropy = 0
        for prob in probabilities:
            if prob > 0:
                entropy += prob * math.log(prob, 2)
        return -entropy
    
    def calc_information_gain(self, split_name, target_name):
        entropy_T = self.calc_entropy(self.data[target_name])
        median = self.data[split_name].median()
        left_split = self.data[self.data[split_name] <= median]
        right_split = self.data[self.data[split_name] > median]
        subset_entropies = 0
        for subset in [left_split, right_split]:
            prob = (subset.shape[0] / float(self.data.shape[0]))
            subset_entropies += prob * self.calc_entropy(subset[target_name])
        info_gain = entropy_T - subset_entropies
        return info_gain
        
def main():
    prep = assemble.Preprocessing()
    prep.read_file()
    prep.convert_categorical_variables()
    data = prep.data
    tree = DecisionTree(data)
    information_gains = []
    columns = settings.columns_subset
    for col in columns:
        info_gain = tree.calc_information_gain(split_name = col, target_name = "high_income")
        information_gains.append(info_gain)
    max_info_gain = information_gains.index(max(information_gains))
    best_split = columns[max_info_gain]
          
if __name__ == "__main__":
    main()

    
    