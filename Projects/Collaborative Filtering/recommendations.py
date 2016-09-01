# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 19:38:58 2016

@author: donaldfung
"""

""" Making Recommendations

This project handles both user-based and item-based filtering

"""

import assemble
import similarities

class Recommendations():
    
    # User Based Recommendations
    

if __name__ == "__main__":
    
    # Returns a dictionary 
    data = assemble.Data()
    user_data = data.user_data
    
    sim = similarities.Correlations()
    print sim.sim_pearson(user_data, "Lisa Rose", "Gene Seymour")
    # Collaborative Filtering technique