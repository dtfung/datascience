# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 22:16:58 2016

@author: donaldfung
"""

import settings
import assemble
import Environment
import random
import pandas as pd
import prepare
import computations
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsClassifier

class Models():
    def __init__(self, data):
        self.data = data
        
    def partition_dataset(self):
        self.data.dropna(inplace = True) # remove rows with NaN values
        # Extract features into a new dataframe
        features = settings.features
        X = self.data[features]
        # get label
        y = self.data["Adj. Close"]
        
        train_set_size = prepare.train_set_size(X)
        test_set_size = int(X.shape[0] * settings.test_set_size)
        X_train = X[:train_set_size]
        y_train = y[:train_set_size]
        X_test = X[-test_set_size:]
        y_test = y[-test_set_size:]
        self.fit_model(X_train, y_train, X_test, y_test)
    
    def fit_model(self, X_train, y_train, X_test, y_test):
        # basic Linear Regression 
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_train_pred = lr.predict(X_train)
        y_test_pred = lr.predict(X_test)
        train_error = mean_absolute_error(y_train, y_train_pred)
        test_error = mean_absolute_error(y_test, y_test_pred)
        print test_error
        print train_error

class Q_Learning():
    def __init__(self, data):
        # Initialize variables here
        self.data = data
        self.prices = data["Adj. Close"]
        self.actions = ["buy", "hold", "sell"] 
        self.lastState = None
        self.lastAction = None
        self.lastReward = None
        self.qTable = {}
        self.epsilon = 0.01 # exploration rate
        self.alpha = 0.5 # learning rate
        self.gamma = 0.5 # discount rate
        self.crash = []
        
        
        self.performance = Performance()
    
        
    def update(self, state, count):
        self.performance.trades += 1
        if self.lastState is None: 
            action = random.choice(self.actions) # random action chosen on first move
            """ for now, assume commission fees, dividend payouts aren't included """
            reward = self.get_reward(action, count)
        else:
            action = self.choose_action(state)
            #print "action = ", action
            """ for now, assume commission fees, dividend payouts aren't included """
            reward = self.get_reward(action, count)
            # update Q-table
            try:
                self.qLearn(self.lastState, self.lastAction, self.lastReward, state)
            except:
                self.crash.append((action, reward))
        self.lastState = state
        self.lastAction = action
        self.lastReward = reward 
        
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
    
    def get_reward(self, action, count):
        financials = computations.Financials()
        daily_returns_list = financials.get_daily_returns(self.data) # list of daily return
        if count < len(daily_returns_list - 1):
            daily_return = daily_returns_list.ix[count + 1] # return for a chosen day
            if daily_return == 0.0:
                return 0
            elif action == "buy" and daily_return < 0:
                self.performance.losses += 1
                return daily_return
            elif action == "buy" and daily_return > 0:
                self.performance.wins+=1
                return daily_return
            elif action == "sell" and daily_return < 0:
                self.performance.wins+=1
                return daily_return
            elif action == "sell" and daily_return > 0:
                self.performance.losses += 1
                return - daily_return
            elif action == "hold":
                self.performance.hold += 1 
                return 0 
        
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
        
class Performance():
    def __init__(self):
        self.losses = 0
        self.wins = 0
        self.hold = 0
        self.trades = 0
        self.win_loss_ratio = 0.0
    
    def show(self):
        print "Losses%:",self.losses/self.trades
        print "Wins%:",self.wins/self.trades
        print "Hold%:",self.hold/self.trades
        self.win_loss_ratio = self.wins/self.losses
        print self.win_loss_ratio
              
def run():
    #   Get stock price data
    data = assemble.Data(settings.company, settings.storage_option)
    df = data.create_dataframe()
    #   Setup environment
    env = Environment.Market(df)
    env.get_financials()
    
if __name__ == "__main__":
    run()
    
