# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 22:14:41 2016

@author: donaldfung
"""

class Correlations():
    
    def sim_pearson(self, prefs, object1, object2):
        # get similar items 
        sim = {}
        for item in prefs[object1]:
            if item in prefs[object2]:
                sim[item] = 1
                
        # number of elements
        n = len(sim)
        
        # if no similarities, return 0
        if n == 0: return 0
            
        # add up preferences
        sum1 = sum([prefs[object1][item] for item in sim])
        sum2 = sum([prefs[object2][item] for item in sim]) 
        
        # Sum up the squares
        sum_sq_1 = sum([pow(prefs[object1][item],2) for item in sim])
        sum_sq_2 = sum([pow(prefs[object2][item],2) for item in sim])
        
        # Sum up the products
        pSum = sum([prefs[object1][item]*prefs[object2][item] for item in sim]) 
        
        # Calculate Pearson score
        num = pSum - (sum1 * sum2)/n
        
        den = ((sum_sq_1 - (sum1**2)/n) * (sum_sq_2 - (sum2**2)/n))**.5
        if den == 0: 
            return 0
        r = num/den
        
        return r