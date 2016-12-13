#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 04:00:53 2016

@author: donaldfung
"""
import settings

class DynaQ():
    
    def __init__(self):
        self.t_table = {}
        self.epsilon = settings.epsilon

    def update_table(self, state, action, timestep):
        self.t_table[(state, action)] = timestep
                     
    def get_t(self, state, action):
        return self.t_table.get((state, action), 0.0)
    
    def calc_exploration_bonus(self, current_timestep, state, action):
        # check for state and action pair
        t = self.get_t(state, action)
        if t > 0:
            # calculate time elapsed since last occurance of state, action pair
            n = current_timestep - t
            # calculate exploration bonus 
            
            ex_bonus = self.epsilon * (abs(n)**0.5)
        else:
            ex_bonus = 0.0
        # update table 
        self.update_table(state, action, current_timestep)
        return ex_bonus
        
    
        