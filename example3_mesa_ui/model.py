from mesa import DataCollector
from agent import Person, Bank 
import pandas as pd 
from mesa import Model

class DigitalInclusionModel(Model):
    def __init__(self, csv_file, campaign_capacity, campaign_effectiveness):
        self.people = []

        data = pd.read_csv(csv_file)

        # Read the people from file
        for _, row in data.iterrows():
            person = Person(
                prob_stopping_use=float(row["Stopping Probability"]),
                digital_literacy_level=float(row["Digital Literacy Level"]),
                using_digital_services=bool(row["Uses Digital Services"])
            )
            self.people.append(person)

        # Create the bank
        self.bank = Bank(campaign_capacity=campaign_capacity, campaign_effectiveness = campaign_effectiveness, people = self.people)

        # Create a mesa data collector: to help us keep track of data per tick
        self.datacollector = DataCollector(
            {
                "Users of Digital Services": lambda m: sum(p.using_digital_services for p in m.people),
                "Non-Users": lambda m: sum(not p.using_digital_services for p in m.people),
                "Total Promotion Capacity": lambda m: m.bank.campaign_capacity
            }
        )

    def step(self):
        self.bank.step()
        for person in self.people:
            person.step()
        self.datacollector.collect(self)
