# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 22:14:41 2016

@author: donaldfung


Reference:

Segaran, Toby. (2007). Programming Collective Intelligence. O'Reilly Media - 
http://shop.oreilly.com/product/9780596529321.do
"""

class Correlations():
    
    def sim_pearson(self, user_data, object1, object2):
        # get similar items 
        sim = {}
        for item in user_data[object1]:
            if item in user_data[object2]:
                sim[item] = 1
                
        # number of elements
        n = len(sim)
        
        # if no similarities, return 0
        if n == 0: return 0
            
        # add up preferences
        sum1 = sum([user_data[object1][item] for item in sim])
        sum2 = sum([user_data[object2][item] for item in sim]) 
        
        # Sum up the squares
        sum_sq_1 = sum([pow(user_data[object1][item],2) for item in sim])
        sum_sq_2 = sum([pow(user_data[object2][item],2) for item in sim])
        
        # Sum up the products
        pSum = sum([user_data[object1][item]*user_data[object2][item] for item in sim]) 
        
        # Calculate Pearson score
        num = pSum - (sum1 * sum2)/n
        
        den = ((sum_sq_1 - (sum1**2)/n) * (sum_sq_2 - (sum2**2)/n))**.5
        if den == 0: 
            return 0
        r = num/den
        
        return r
        
    def euclidean_distance(self, challenges, object1, object2):
        total = 0
        for i, item in enumerate(challenges[object2]):
            total += (challenges[object1][i] - item) ** 2
        
        # assign higher values for similar challenges by adding 1 to the function and inverting it
        r = 1/(1 + (total ** 0.5))
        return r
        
        