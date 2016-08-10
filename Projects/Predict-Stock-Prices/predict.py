# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:16:58 2016

@author: donaldfung
"""

import settings
import assemble
import Environment
import random
    
class Q_Learning():
    def __init__(self, data):
        # Initialize variables here
        self.prices = data["Adj. Close"]
        self.actions = ["buy", "hold", "sell"] 
        self.lastState = None
        self.lastAction = None
        self.lastReward = None
        self.qTable = {}
        self.epsilon = 0.05 # exploration rate
        self.alpha = 0.1 # learning rate
        self.gamma = 0.1 # discount rate
        
    def update(self, state):
        """ Get new state from environment
        
        input:  state = (volume, rolling_mean, upper, lower,  cumulative returns close_sma)
                type = tuple
        """
        # TODO: first move
        if self.lastState is None: 
            action = random.choice(self.actions) # random action chosen on first move
            # TODO: calculate reward
            """ for now, assume commission fees, dividend payouts aren't included """
            reward = 0
        
        else:
            action = self.choose_action(state)
            # TODO: calculate reward
            """ for now, assume commission fees, dividend payouts aren't included """
            reward = random.choice(range(0.00001, 1))
            # TODO: update q-table with last state, action, reward and current state
            
            self.qLearn(self.lastState, self.lastAction, self.lastReward, self.state)
            
        self.lastState = state
        self.lastAction = action
        self.lastReward = reward 
        print reward
        print action
        
    def choose_action(self, state):
        q = [self.getQ(state, a) for a in self.actions]
        maxQ = max(q)
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

                action = self.actions[i]
        return action
        
    # Find the max state-action value in the current state and use it to update the Q table
    def qLearn(self, lastState, lastAction, lastReward, state):
        # get the max Q for the current state here
        maxQnew = max([self.getQ(state, action) for action in self.actions])
        # call method to update the Q table here
        self.updateQ(lastState, lastAction, lastReward, maxQnew)
    
    def getQ(self, state, action):
        return self.qTable.get((state, action), 0.0)
    
    def updateQ(self, state, action, reward, maxQnew):
        # Update Q Values for the last state and action
        oldValue = self.qTable.get((state, action), 0.0)
        self.qTable[(state, action)] = oldValue + self.alpha * (reward + (self.gamma * maxQnew) - oldValue)
        
class Models():
    def __init__(self, options, data):
        self.models = options
        self.data = data
        
    def partition_dataset(self, data):
        pass
    

def run():
    #   Get stock price data
    data = assemble.Data(settings.company, settings.storage_option)
    df = data.create_dataframe()
    #   Setup environment
    env = Environment.Market(df)
    env.get_financials()
    
if __name__ == "__main__":
    run()
    