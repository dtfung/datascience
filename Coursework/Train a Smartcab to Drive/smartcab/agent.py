import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)
        
        # Initialize any additional variables here
        self.actions = [None,'forward','left','right']
        self.lastState = None
        self.lastAction = None
        self.lastReward = None
    
        self.qTable = {}
        self.epsilon = .05
        self.alpha = 0.7
        self.gamma = 0.1
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
                
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Update state
        self.state = (inputs.get('light'),inputs.get('oncoming'), inputs.get('left'), inputs.get('right'), self.next_waypoint)
        
        if self.lastState is None:
            action = random.choice(self.actions)
            reward = self.env.act(self, action)
            
        else:
            action = self.choose_action(self.state)
            reward = self.env.act(self, action)
            self.qLearn(self.lastState, self.lastAction, self.lastReward, self.state)
                         
        self.lastState = self.state
        self.lastAction = action
        self.lastReward = reward
    
    # Find the max state-action value in the current state and use it to update the Q table
    def qLearn(self, lastState, lastAction, lastReward, state):
        # get the max Q for the current state here
        maxQnew = max([self.getQ(state, action) for action in self.actions])
        # call method to update the Q table here
        self.updateQ(lastState, lastAction, lastReward, maxQnew)

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

    """returns state-action values"""
    def getQ(self, state, action):
        return self.qTable.get((state, action), 0.0)
    
    def updateQ(self, state, action, reward, value):
        """Update Q Values for the current state and action"""
        oldValue = self.qTable.get((state, action), 0.0)
        self.qTable[(state, action)] = oldValue + self.alpha *(reward + (self.gamma * value) - oldValue)
        print('Updated Q for previous state is = {}'.format(self.qTable[(state, action)]))
 
    
def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()
    a = e.create_agent(LearningAgent)
    e.set_primary_agent(a, enforce_deadline = True)

    # Now simulate it   
    sim = Simulator(e, update_delay = .08)
    sim.run(n_trials= 100)
    

if __name__ == '__main__':
    run()
