from model import DigitalInclusionModel
from visualization import graph_it
import pandas as pd

if __name__ == "__main__":
    csv_file = "person_data.csv"
    campaign_capacity = 10
    campaign_effectiveness = 1.1 # increases the digital literacy of a person by 10%

    model = DigitalInclusionModel(csv_file, campaign_capacity, campaign_effectiveness)
    results_df = None

    for step in range(10):
        model.step()

        # Collect additional data
        total_people = len(model.people)
        users = sum(p.using_digital_services for p in model.people)
        non_users = total_people - users
        capacity = model.bank.campaign_capacity
        usage_ratio = users / total_people if total_people > 0 else 0

        # Share the outccomes
        print(f"Step {step}: Users = {users}, Non-Users = {non_users}, Capacity = {capacity}, Usage Ratio = {usage_ratio:.2%}")

    graph_it(model.datacollector.get_model_vars_dataframe())
