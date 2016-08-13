import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        
        # TODO: Initialize any additional variables here
        self.actions = [None,'forward','left','right'] # a list of possible actions the agent could take
        self.lastState = None
        self.lastAction = None
        self.lastReward = None
    
        self.qTable = {} # a dictionary used to store Q values
        self.epsilon = .05 # introduce exploration
        self.alpha = 0.7 # learning rate
        self.gamma = 0.1 # discount rate
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

        #print('epsilon is now equal to: {}'.format(self.epsilon))
                
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs.get('light'),inputs.get('oncoming'), inputs.get('left'), inputs.get('right'), self.next_waypoint)
        
        # TODO: Select action according to your policy
        
        # Random actions to choose from
        # action = random.choice(self.directions) 
        
        # Execute action and get reward
        #reward = self.env.act(self, action)
        
        # TODO: Learn policy based on state, action, reward
        
        if self.lastState is None:
            action = random.choice(self.actions)
            reward = self.env.act(self, action)
            #self.qLearn(self.lastState, self.lastAction, reward, self.state)
            
        else:
            action = self.choose_action(self.state)
            reward = self.env.act(self, action)
            self.qLearn(self.lastState, self.lastAction, self.lastReward, self.state)
                         
        self.lastState = self.state
        self.lastAction = action
        self.lastReward = reward
        
        #print ("LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward))  # [debug]
    
    # Find the max state-action value in the current state and use it to update the Q table
    def qLearn(self, lastState, lastAction, lastReward, state):
        
        # get the max Q for the current state here
        maxQnew = max([self.getQ(state, action) for action in self.actions])
        
        # call method to update the Q table here
        self.updateQ(lastState, lastAction, lastReward, maxQnew)
        
    # returns action which maximizes Q for the current state
    def choose_action(self, state):
        
        q = [self.getQ(state, a) for a in self.actions]
        maxQ = max(q)
        
        if random.random() < self.epsilon:
            #print('random action taken')
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

    """returns state-action values"""
    def getQ(self, state, action):
        return self.qTable.get((state, action), 0.0)  # return 0.0 if no value exists
    
    def updateQ(self, state, action, reward, value):

        """Update Q Values for the current state and action"""
        oldValue = self.qTable.get((state, action), 0.0)
        #print('oldValue = {}'.format(oldValue))
        self.qTable[(state, action)] = oldValue + self.alpha *(reward + (self.gamma * value) - oldValue)
        print('Updated Q for previous state is = {}'.format(self.qTable[(state, action)]))
 
    
def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline = True)  # set agent to track

    # Now simulate it   
    sim = Simulator(e, update_delay = .08)  # reduce update_delay to speed up simulation
    sim.run(n_trials= 100)  # press Esc or close pygame window to quit
    

if __name__ == '__main__':
    run()
