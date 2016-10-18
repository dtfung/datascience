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
from account import OpenPosition

class Qlearning():
    
    def __init__(self, alpha, gamma, epsilon, data, is_train, qtable, dynaQ_online):
        """Declare attributes here"""
        # hyperparameters
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        # data
        self.data = data
        self.is_train = is_train
        # metrics
        self.loss = []
        self.win = []
        self.hold = []
        self.timestep = 0
        # actions
        self.actions = ["buy", "sell", "hold"]
        self.last_state = None
        self.last_action = None
        self.last_reward = None
        # Q-table
        self.qtable = qtable
        # class instances
        self.env = Environment()
        self.open_positions = OpenPosition()
        self.helpers = Helpers()
        # dyna
        self.dynaQ_online = dynaQ_online
           
    def reset(self):
        """Reset a few variables"""
        self.timestep = 0
        self.loss = []
        self.win = []
        self.hold = []
        self.epsilon = settings.epsilon
        self.open_positions.direction = None
        self.open_positions.trade_open = False
        self.open_positions.open_price = 0.0
        self.open_profit = 0.0

    def reduce_exploration(self):
        """gradually reduce exploration rate over time"""
        if self.epsilon > 0.05:
            self.epsilon -= .001
        
    def get_state(self):
        """Get new state"""
        df = self.data.copy()
        losses = []
        wins = []
        holds = []

        # get epochs
        if self.dynaQ_online == True:
            epochs = 1
        else:
            if self.is_train:
                epochs = settings.epochs
            else:
                # epoch size if test set is used
                epochs = 1
        for i in xrange(0, epochs):
            for i in xrange(df.shape[0] - 1):
                # get ith row
                row = df.iloc[i]
                # compile state
                state = self.env.get_state(row, self.open_positions.trade_open, self.open_positions.open_profit)
                self.update(state)
                # reduce exploration rate
                self.reduce_exploration()
            
            losses.append(sum(self.loss))
            wins.append(sum(self.win))
            holds.append(sum(self.hold))
            
            print "total wins:", sum(self.win)
            print "no action sum:", sum(self.hold)
            print "total losses", sum(self.loss)
            # reset variables
            self.reset()
            print len(self.qtable)
            
            if self.is_train:
                self.helpers.save(self.qtable)
            
    def update(self, state):
        
        if self.timestep == 0:
            # randomize action
            action = random.choice(self.actions)
            # handle open positions
            self.actions = self.open_positions.manage_open_position(self.data["Adj. Close"], 
                                                                    action, 
                                                                    self.actions, 
                                                                    self.timestep)
            reward = 0
        else:
            action = self.select_action(state)
            self.actions, reward = self.open_positions.calc_return(self.data["Adj. Close"], self.timestep, action, self.actions)
            
            reward = self.open_positions.calc_daily_return(self.data["Adj. Close"], self.timestep, action)
            
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
        qtable = pickle.load(open("RL/memory/qtable_cum_returns.pkl", "rb"))
        return qtable
        
    def save(self, qtable):
        out = open("RL/memory/qtable_cum_returns.pkl", "wb")
        pickle.dump(qtable, out)
        out.close()

        
    