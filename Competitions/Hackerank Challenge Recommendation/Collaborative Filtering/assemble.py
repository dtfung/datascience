# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 21:21:59 2016

@author: donaldfung
"""
import settings
import pandas as pd
import csv

class UserData():
    
    def __init__(self):
        
        # Store challenges either completed or started but not completed
        self.user_data = {}
        # Store submissions
        self.variables = settings.Variables()
        self.submissions = pd.read_csv(self.variables.submissions)

    def create_user_data(self):
        
        # declare local variables
        hacker_ID_label = self.variables.hacker_id
        contest_ID_label = self.variables.contest_id
        challenge_ID_label = self.variables.challenge_id
        solved_label = self.variables.solved
        
        # retrieve hacker_ID, contest_ID, challenge_ID and solved
        #self.submissions
        #len(self.submissions)
        for i in range(len(self.submissions)):
            
            hacker_ID = (self.submissions.iloc[i][hacker_ID_label])
            contest_ID = self.submissions.iloc[i][contest_ID_label]
            challenge_ID = self.submissions.iloc[i][challenge_ID_label]
            solved = self.submissions.iloc[i][solved_label]
            
            # set hacker ID
            self.user_data.setdefault(hacker_ID, {})
            
            # add challenges and scores
            if (challenge_ID, contest_ID) in self.user_data[hacker_ID] and self.user_data[hacker_ID][challenge_ID, contest_ID] == 0.0:
                self.user_data[hacker_ID][challenge_ID, contest_ID] +=  solved
            else:
                self.user_data[hacker_ID][challenge_ID, contest_ID] = solved 
                
        return self.user_data
        
class Challenges():
    
    def __init__(self):
        
        self.variables = settings.Variables()
        self.challenges_data = pd.read_csv(self.variables.challenges)
        
        self.prep_challenges = {}
        
    def handle_categorical_data(self):
        
        # for domain and subdomain columns, convert text to numbers
        cols = ["domain", "subdomain"]
        for item in cols:
            col = pd.Categorical.from_array(self.challenges_data[item])
            self.challenges_data[item] = col.codes
            
    def normalize(self):
        # columns to normalize
        cols = ["solved_submission_count", "total_submissions_count"]
        from sklearn.preprocessing import MinMaxScaler
        mms = MinMaxScaler()
        self.challenges_data[cols] = mms.fit_transform(self.challenges_data[cols])

    def to_dict(self):
        
        for i in range(len(self.challenges_data)):
            # get values from df
            difficulty = (self.challenges_data.iloc[i]["difficulty"])
            contest_ID = self.challenges_data.iloc[i]["contest_id"]
            challenge_ID = self.challenges_data.iloc[i]["challenge_id"]
            solved_submission_count = self.challenges_data.iloc[i]["solved_submission_count"]
            total_submissions_count = self.challenges_data.iloc[i]["total_submissions_count"]
            
            # set challenge ID and contest ID
            self.prep_challenges.setdefault((challenge_ID, contest_ID),  {})
            
            # add challenges and scores
            self.prep_challenges[challenge_ID, contest_ID] = [difficulty, solved_submission_count, total_submissions_count]

            
            