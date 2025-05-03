from mesa import Agent 
import random

# Person agent
class Person(Agent):
    def __init__(self, unique_id, model, education_level, 
                 digital_literacy_level, uses_digital_services):
        self.unique_id = unique_id
        self.model = model
        self.education_level = education_level
        self.digital_literacy_level = digital_literacy_level  
        self.uses_digital_services = bool(uses_digital_services)

    def step(self):
        pass

# Organization agent
class Organization(Agent):
    def __init__(self, unique_id, model, promotion_capacity):
        self.unique_id = unique_id
        self.model = model
        self.promotion_capacity = promotion_capacity  

    def step(self):
        if not getattr(self.model, "testing", False):
            self.promotion_capacity += random.randint(0, 2)

        if self.promotion_capacity <= 0:
            return

        non_users = [
            agent for agent in self.model.people
            if not agent.uses_digital_services
        ]

        non_users.sort(
            key=lambda x: (self.education_priority(x.education_level), x.digital_literacy_level),
            reverse=True
        )

        for person in non_users:
            if self.promotion_capacity > 0 and person.digital_literacy_level >= 5:
                person.uses_digital_services = True
                self.promotion_capacity -= 1


    @staticmethod
    def education_priority(level):
        priority = {
            "High School": 1,
            "Bachelor's": 2,
            "Master's": 3,
            "PhD": 4
        }
        return priority.get(level, 0)


class PolicyAgent(Agent):
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model

    def step(self):
        for person in self.model.people:
            if not person.uses_digital_services:
                person.digital_literacy_level = min(person.digital_literacy_level + 0.5, 10)