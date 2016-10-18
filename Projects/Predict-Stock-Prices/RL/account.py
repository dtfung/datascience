#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 22:40:19 2016

@author: donaldfung
"""

class OpenPosition():
    
    def __init__(self):
        self.direction = None
        self.trade_open = False
        self.open_price = 0.0
        self.open_profit = 0.0
    
    def calc_daily_return(self, price_data, timestep, action):
        """The % daily return based on an action"""
        # get price
        current_price = price_data.iloc[timestep]
        next_day_price = price_data.iloc[timestep + 1]

        diff = next_day_price - current_price
        daily_return = diff/current_price
        
        if action == "buy":
            if daily_return < 0.0:
                return daily_return
            else:
                return abs(daily_return)  
        elif action == "sell":
            if daily_return < 0.0:
                return abs(daily_return)
            else:
                return - daily_return  
        else:
            return 0.0
            
    def calc_return(self, price_data, timestep, action, action_list):
        # current price
        current_price = price_data.iloc[timestep]
        # handle cases where a trade is open
        if self.trade_open == True:
            # long positions
            if self.direction == "buy":
                if action == "hold": 
                    self.open_profit = (current_price - self.open_price)/self.open_price
                    return action_list, 0.0
                elif action == "sell":
                    # reset direction
                    self.direction = None
                    # set trade open status to false
                    self.trade_open = False
                    reward = (current_price - self.open_price)/self.open_price
                    available_actions = ["buy", "sell", "hold"]
                    return available_actions, reward
            elif self.direction == "sell":
                if action == "buy":
                    self.direction = None
                    # set trade open status to false
                    self.trade_open = False
                    reward = (self.open_price - current_price)/self.open_price
                    available_actions = ["buy", "sell", "hold"]
                    return available_actions, reward
                else: 
                    self.open_profit = (self.open_price - current_price)/self.open_price
                    return action_list, 0.0
        # handle cases where no trade is open
        elif self.trade_open == False: 
            available_actions = self.manage_open_position(price_data, action, action_list, timestep)
            self.open_profit = 0.0
            return available_actions, 0.0
                
    def manage_open_position(self, price_data, action, action_list, timestep):
        # If no positions exists
        if self.trade_open == False:
            # if a buy signal issued
            if action == "buy":
                # set trade open status to true
                self.trade_open = True
                # adjust available list of actions
                available_actions = ["sell", "hold"]
                # set direction
                self.direction = "buy"
                # set open price 
                self.open_price = price_data.iloc[timestep]
                return available_actions
            # if a sell signal issued
            elif action == "sell":
                # set trade open status to true
                self.trade_open = True
                # adjust available list of actions
                available_actions = ["buy", "hold"]
                # set direction
                self.direction = "sell"
                # set open price 
                self.open_price = price_data.iloc[timestep]
                return available_actions
            elif action == "hold":
                return action_list