import random
from mesa import Agent

# Define the Person
class Person(Agent):
    # Initialize the person: what do they start with?
    def __init__(self, prob_stopping_use, 
                 digital_literacy_level, using_digital_services):
        self.prob_stopping_use = prob_stopping_use
        self.using_digital_services = using_digital_services
        self.digital_literacy_level = digital_literacy_level  

    # How does the person change over time?  Each time period, we call "Step" once

    def step(self):
        if self.using_digital_services:
            self.using_digital_services = not (random.random() < self.prob_stopping_use)
        else:
            self.using_digital_services = random.random() < self.digital_literacy_level

# Define the Bank
class Bank(Agent):
    # Initialize the bank: what do they start with?
    def __init__(self, campaign_capacity, campaign_effectiveness, people):
        self.campaign_capacity = campaign_capacity  
        self.campaign_effectiveness = campaign_effectiveness
        self.people = people

    def step(self):
        non_users = [agent for agent in self.people if not agent.using_digital_services]

        to_sample = min(len(non_users), self.campaign_capacity)
        if to_sample > 0:
            campaign_members  = random.sample(non_users, to_sample)
            for person in campaign_members:
                person.digital_literacy_level = max(person.digital_literacy_level*self.campaign_effectiveness, 1)
