from ex2.model import DigitalInclusionModel


if __name__ == "__main__":
    csv_file = "person_data.csv"
    num_organizations = 3
    initial_capacity = 10

    model = DigitalInclusionModel(csv_file, num_organizations, initial_capacity)

    for step in range(10):
        model.step()
        data = model.datacollector.get_model_vars_dataframe()

        total_people = len(model.people)
        users = sum(p.uses_digital_services for p in model.people)
        non_users = total_people - users
        capacity = sum(o.promotion_capacity for o in model.organizations)
        usage_ratio = users / total_people if total_people > 0 else 0

        print(f"Step {step}: Users = {users}, Non-Users = {non_users}, Capacity = {capacity}, Usage Ratio = {usage_ratio:.2%}")


