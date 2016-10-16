#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:26:20 2016

@author: donaldfung
"""

import random 
from environment import Environment

class Qlearning():
    
    def __init__(self, alpha, gamma, epsilon, data):
        """Declare attributes here"""
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.data = data
        self.trade_open = False
        self.cum_return = 0
        self.timestep = 0
        self.actions = ["buy", "sell", "hold"]
        self.last_state = None
        self.last_action = None
        self.last_reward = None
        self.qtable = {}
        
    def get_state(self):
        """Get new state"""
        
        env = Environment()
        df = env.discretize(self.data)
        
        for i in xrange(df.shape[0]):
            # get ith row
            row = df.iloc[i]
            # compile state
            state = env.get_state(row, self.trade_open, self.cum_return)
            
            self.update(state)

    def update(self, state):
        
        if self.timestep == 0:
            # randomize action
            action = random.choice(self.actions)
            reward = .1
        else:
            action = random.choice(self.actions)
        
            reward = .1
            
            # TODO: update Q table
            self.updateQ(last_state = self.last_state,
                         last_action = self.last_action,
                         last_reward = self.last_reward,
                         current_state = state)
            
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
        self.qtable[(last_state, last_action)] = ((1 - self.alpha) * last_Q) + self.alpha * (last_reward + (self.gamma * maxQ))
        
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
        
        

    # TODO: calculate reward