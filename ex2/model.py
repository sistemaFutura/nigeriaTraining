from mesa import Model
from ex2.agent import Person, PolicyAgent, Organization
from mesa.datacollection import DataCollector  
import pandas as pd 


class DigitalInclusionModel(Model):
    def __init__(self, csv_file, num_organizations, initial_capacity):
        super().__init__()
        self.agent_list = []
        self.people = []
        self.organizations = []

        data = pd.read_csv(csv_file)
        for _, row in data.iterrows():
            person = Person(
                unique_id=row["ID"],
                model=self,
                education_level=row["Education Level"],
                digital_literacy_level=row["Digital Literacy Level"],
                uses_digital_services=row["Uses Digital Services"]
            )
            self.agent_list.append(person)
            self.people.append(person)

        for i in range(num_organizations):
            org = Organization(
                unique_id=f"org_{i}",
                model=self,
                promotion_capacity=initial_capacity
            )
            self.agent_list.append(org)
            self.organizations.append(org)

        self.policy = PolicyAgent(unique_id="policy_1", model=self)
        self.agent_list.append(self.policy)

        self.datacollector = DataCollector(
            {
                "Users of Digital Services": lambda m: sum(p.uses_digital_services for p in m.people),
                "Non-Users": lambda m: sum(not p.uses_digital_services for p in m.people),
                "Total Promotion Capacity": lambda m: sum(o.promotion_capacity for o in m.organizations)
            }
        )

    def step(self):
        self.policy.step()
        for org in self.organizations:
            org.step()
        for person in self.people:
            person.step()
        self.datacollector.collect(self)
