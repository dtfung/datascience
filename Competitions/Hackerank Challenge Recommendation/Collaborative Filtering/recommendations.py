# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 19:38:58 2016

@author: donaldfung

Reference:

Segaran, Toby. (2007). Programming Collective Intelligence. O'Reilly Media - 
http://shop.oreilly.com/product/9780596529321.do
"""

""" Making Recommendations

item-based filtering

"""

import assemble
import similarities
import pandas as pd
import os.path
import csv
import settings

class Recommendations():
    
    def __init__(self):
        self.similar_items = None
        self.output = pd.DataFrame()
        self.n = 10
    
    def top_matches(self, data, object1, correlation_func):
      
      # get correlation scores
      scores = [(correlation_func(data, object1, object2), object2) for object2 in data if object2 != object1]
    
      # Sort the list so the highest scores appear at the top
      scores.sort()
      scores.reverse()
      return scores
      
    """ Item-Based Filtering """
        
    def transform_data(self, data):
        result = {}
        for object1 in data:
            for item in data[object1]:
                result.setdefault(item, {})
                
                # Flip 
                result[item][object1] = data[object1][item]
        return result
    
    def get_similar_items(self, data, correlation_func):
        result = {}
        count = 0
        
        for item in data:
            scores = self.top_matches(data, item, correlation_func)
            result[item] = scores
            count += 1
        return result
        
    def compile_recommendations(self, user_data, challenges_dict, corr_func):
        count = 0
        
        for hacker, challenges_attempted in user_data.items():
            recommendations = []
            for challenge in challenges_dict:
                # Check for challenges that the hacker has attempted, but not solved
                if challenge in challenges_attempted:
                    scores = []
                    for attempted_challenge in challenges_attempted:
                        # check if user solved challenge or not
                        solved = user_data[hacker][attempted_challenge]
                        if challenge == attempted_challenge and solved == 0:
                            # get correlation score:
                            for chal in challenges_attempted:
                                if chal != challenge:
                                    score = corr_func(challenges_dict, chal, challenge)
                                    scores.append(score)
                    # add this challenge to recommended challenges
                    if len(scores) >= 1:
                        recommendations.append((max(scores), challenge))
                # Check for challenges that the hacker hasn't attempted and get avg correlation 
                else:
                    # get correlation between new challenge to challenges that user has attempted
                    scores = []
                    for attempted_challenge in challenges_attempted:
                        score = corr_func(challenges_dict, attempted_challenge, challenge)
                        scores.append(score)
                    recommendations.append((max(scores), challenge))
            # get top 10 recommendations for a hacker
            recommendations.sort()
            recommendations.reverse()
            recommendations = recommendations[:10]
            for i, challenge in enumerate(recommendations):
                if i == 0:
                    self.output.loc[count, i] = hacker
                else:
                    self.output.loc[count, i] = challenge[1][0]
            count += 1
            print "{} item added to output!".format(count)
        self.output.to_csv("processed_data/output.csv", index = False, header = False)

def run():
    
    data = assemble.UserData()
    # create dictionary of user history
    user_data = data.create_user_data()
    
    # init classes to handle correlations
    sim = similarities.Correlations()
    rec = Recommendations()
    
    # normalize challenges data
    challenges = assemble.Challenges()
    challenges.normalize()
    
    # extract into dictionary
    challenges.to_dict()
    
    # get hacker recommendations
    rec.compile_recommendations(user_data, challenges.prep_challenges, sim.euclidean_distance)
                
if __name__ == "__main__":
    
    run()
    
    
    
    
    
    