import random

class Person:
    def __init__(self, prob_stopping_use, prob_starting_use):
        self.prob_stopping_use = prob_stopping_use
        self.prob_starting_use = prob_starting_use
        self.using_digital_services = random.choice([True, False]) 

    def step(self):
        if self.using_digital_services:
         
            self.using_digital_services = not (random.random() < self.prob_stopping_use)
        else:

            self.using_digital_services = random.random() < self.prob_starting_use

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
    model = DigitalServicesModel(
        num_agents=100,
        prob_stopping_use=random.uniform(0.1, 0.5),
        prob_starting_use=random.uniform(0.1, 0.5)
    )
    model.run(steps=5)
