# Imports.  The heart of an agent based model needs ALMOST NOTHING
import random

# Define the Agent
class Person:
    # Initialize the agent: what do they start with?
    def __init__(self, prob_stopping_use, prob_starting_use):
        self.prob_stopping_use = prob_stopping_use
        self.prob_starting_use = prob_starting_use
        self.using_digital_services = random.choice([True, False]) 

    # How does the agent change over time?  Each time period, we call "Step" once
    def step(self):
        if self.using_digital_services:
            self.using_digital_services = not (random.random() < self.prob_stopping_use)
        else:
            self.using_digital_services = random.random() < self.prob_starting_use

# Define a model to hold the agents
class DigitalServicesModel:

    def __init__(self, num_agents, prob_stopping_use, prob_starting_use):
        self.num_agents = num_agents
        self.agents = [Person(prob_stopping_use, prob_starting_use) for _ in range(num_agents)]

    def step(self):
        for agent in self.agents:
            agent.step()

    def run(self, steps):
        for i in range(steps):
            self.step()
            
            using_services = sum(1 for agent in self.agents if agent.using_digital_services)

            print(f"Step {i + 1}: Using Digital Services = {using_services}, Not Using = {self.num_agents - using_services}")



if __name__ == "__main__":
    # Create our model, with initial data
    model = DigitalServicesModel(
        num_agents=100,
        prob_stopping_use=0.4,
        prob_starting_use=0.2
    )
    # Run the model!
    model.run(steps=10)
