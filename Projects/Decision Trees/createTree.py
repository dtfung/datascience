# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 01:01:44 2016

@author: donaldfung
"""

""" Decision Trees using the ID3 algorithm"""
import assemble
import pandas as pd
import numpy as np
import math
import settings

class DecisionTree():
    def __init__(self):
        self.tree = {}
        self.nodes = []
        
    def calc_entropy(self, column):
        counts = np.bincount(column)
        probabilities = counts / float(len(column))
        entropy = 0
        for prob in probabilities:
            if prob > 0:
                entropy += prob * math.log(prob, 2)
        return -entropy
      
    def calc_info_gain(self, data, split_name, target_label):
        entropy_T = self.calc_entropy(data[target_label])
        median = data[split_name].median()
        left_split = data[data[split_name] <= median]
        right_split = data[data[split_name] > median]
        subset_entropy = 0
        for item in [left_split, right_split]:
            prob = item.shape[0] / float(data.shape[0])
            entropy = self.calc_entropy(item[target_label])
            subset_entropy += prob * entropy
        info_gain = entropy_T - subset_entropy
        return info_gain
    
    def find_best_column(self, data, columns, target_label):
        information_gain = []
        for col in columns:
            info_gain = self.calc_info_gain(data, col, "high_income")
            information_gain.append(info_gain)
            max_gain_index = information_gain.index(max(information_gain))
            best_column = settings.columns_subset[max_gain_index] 
        return best_column
        
    def id3(self, data, columns, target_label, tree):
        # get unique values from target column
        unique_targets = pd.unique(data[target_label])
        # add a new node to the nodes list
        self.nodes.append(len(self.nodes) + 1)
        # add value to tree for new node
        tree["number"] = self.nodes[-1]
        # set value for label in tree
        if len(unique_targets) == 1:
            if 0 in unique_targets:
                tree["label"] = 0
            elif 1 in unique_targets:
                tree["label"] = 1
            return
        # find best column
        best_column = self.find_best_column(data, columns, target_label)
        # get column median
        column_median = data[best_column].median()
        # add these values to tree
        tree["median"] = column_median
        tree["column"] = best_column
        
        # split using the median
        left_split = data[data[best_column] <= column_median]
        right_split = data[data[best_column] > column_median]
        split_dict = [["left", left_split], ["right", right_split]]
        # repeat this function on splits
        for name, split in split_dict:
            tree[name] = {}
            self.id3(split, columns, target_label, tree[name])
            
    def print_with_depth(self, string, depth):
        prefix = "    " * depth
        print("{0}{1}".format(prefix, string)) 
    
    def print_node(self, tree, depth):
        if "label" in tree:
            self.print_with_depth("Leaf: Label {0}".format(tree["label"]), depth)
            return
        self.print_with_depth("{0} > {1}".format(tree["column"], tree["median"]), depth)
        branches = [tree["left"], tree["right"]]
        for branch in branches:
            self.print_node(branch, depth+1)
            
    def predict(self, tree, row):
        if "label" in tree:
            return tree["label"]
        
        column = tree["column"]
        median = tree["median"]
        
        if row[column] <= median:
            return self.predict(tree["left"], row)
        elif row[column] > median:
            return self.predict(tree["right"], row)
    
    def batch_predict(self, tree, df):
        return df.apply(lambda x: self.predict(tree, x), axis = 1)
            
                        
def main():
    prep = assemble.Preprocessing()
    prep.read_file()
    prep.convert_categorical_variables()
    dtree = DecisionTree()
    dtree.id3(prep.data.iloc[:100], settings.columns_subset, "high_income", dtree.tree)
    df = pd.DataFrame([dtree])
    df.to_csv("tree.csv")
    # dummy data
    new_data = pd.DataFrame([
    [40,0],
    ])
    # Assign column names to the data.
    new_data.columns = ["age", "marital_status"]

    

    predictions = dtree.batch_predict(dtree.tree, new_data)
    dtree.print_node(dtree.tree, 0)
    
if __name__ == "__main__":
    main()

    
    