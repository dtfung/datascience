#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:26:20 2016

@author: donaldfung
"""

import random
import settings 
import sys
import pickle
sys.path.insert(0, 'RL/')
from environment import Environment

class Qlearning():
    
    def __init__(self, alpha, gamma, epsilon, data, is_train, qtable):
        """Declare attributes here"""
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.data = data
        self.trade_open = False
        self.cum_return = 0
        self.loss = []
        self.win = []
        self.hold = []
        self.timestep = 0
        self.actions = ["buy", "sell", "hold"]
        self.last_state = None
        self.last_action = None
        self.last_reward = None
        self.qtable = qtable
        self.env = None
        self.helpers = Helpers()
        self.is_train = is_train
        
    def reset(self):
        self.timestep = 0
        self.loss = []
        self.win = []
        self.hold = []

        if self.epsilon > 0.05:
            self.epsilon -= .001
        
    def get_state(self):
        """Get new state"""
        
        self.env = Environment()
        #df = self.env.discretize(self.data)
        df = self.data.copy()
        losses = []
        wins = []
        holds = []

        # get epochs
        if self.is_train:
            
            epochs = settings.epochs
        else:
            epochs = 1
            
        for i in xrange(0, epochs):
            for i in xrange(df.shape[0] - 1):
                # get ith row
                row = df.iloc[i]
                # compile state
                state = self.env.get_state(row, self.trade_open, self.cum_return)
                
                self.update(state)
            
            losses.append(sum(self.loss))
            wins.append(sum(self.win))
            holds.append(sum(self.hold))
            
            print sum(self.win)
            print "holding sum is", sum(self.hold)
            print "loss sum is", sum(self.loss)
            # reset variables
            self.reset()
            
            if self.is_train:
                self.helpers.save(self.qtable)
            

    def update(self, state):
        
        if self.timestep == 0:
            # randomize action
            action = random.choice(self.actions)
            reward = 0
        else:
            action = self.select_action(state)
        
            reward = self.env.calc_daily_return(self.data["Adj. Close"], self.timestep, action)
            
            # TODO: update Q table
            self.updateQ(last_state = self.last_state,
                         last_action = self.last_action,
                         last_reward = self.last_reward,
                         current_state = state)
            
            if reward < 0:
                self.loss.append(1)
            elif reward > 0:
                self.win.append(1)
            elif reward == 0:
                self.hold.append(1)
                
        # save state, action and reward
        self.last_reward = reward
        self.last_action = action
        self.last_state = state
        
        # increment time step
        self.timestep += 1
        
    def updateQ(self, last_state, last_action, last_reward, current_state):
        
        # get max Q for current state and action
        maxQ = max([self.getQ(current_state, action) for action in self.actions]) 
        
        # get Q for last state and action
        last_Q = self.getQ(last_state, last_action)
        
        # update Q for last state and action
        self.qtable[(last_state, last_action)] = last_Q + self.alpha * (last_reward + (self.gamma * maxQ) - last_Q)
        
    def getQ(self, state, action):
        return self.qtable.get((state, action), 0.0)
        
    def select_action(self, state):
        
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
        
class Helpers():
    
    def partition(self, df):
        # get size of train and test sets
        train_size = int(df.shape[0] * 0.9)
        test_size = int(df.shape[0] * 0.1)
        
        train = df.iloc[:train_size]
        test = df.iloc[-test_size:]
        return train, test
    
    def load(self):
        qtable = pickle.load(open("RL/memory/qtable.pkl", "rb"))
        return qtable
        
    def save(self, qtable):
        out = open("RL/memory/qtable.pkl", "wb")
        pickle.dump(qtable, out)
        out.close()