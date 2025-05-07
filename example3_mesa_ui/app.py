import solara
from solara.website.utils import apidoc
from model import DigitalInclusionModel
import pandas as pd

# -------------------------------
# Run the Model
# -------------------------------

if __name__ == "__main__":
    # Initial configuration
    csv_file = "person_data.csv"  # Input file
    campaign_capacity = 10
    campaign_effectiveness = 1.1  # Increases digital literacy by 10%

    # Create the model
    model = DigitalInclusionModel(csv_file, campaign_capacity, campaign_effectiveness)

    # List to store results
    results = []

    # Run the model for 10 steps
    for step in range(10):
        model.step()

        # Collect data from the model
        total_people = len(model.people)
        users = sum(p.using_digital_services for p in model.people)
        non_users = total_people - users
        capacity = model.bank.campaign_capacity
        usage_ratio = users / total_people if total_people > 0 else 0

        # Save results to a list
        results.append({
            "Step": f"Year {step+1}",
            "Users": users,
            "Non-Users": non_users,
            "Capacity": capacity,
            "Usage Ratio": usage_ratio
        })

    # Save the results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv("model_results.csv", index=False)
    print("Results saved to 'model_results.csv'.")

# -------------------------------
# Load Data and Configure ECharts
# -------------------------------

# Load the model results from the CSV file
model_results = pd.read_csv("model_results.csv")

# Extract data from the DataFrame
years = model_results["Step"].tolist()
users = model_results["Users"].tolist()
non_users = model_results["Non-Users"].tolist()

# Define ECharts options for visualization
options = {
    "title": {"text": "Users vs Non-Users of Digital Services"},
    "tooltip": {},
    "legend": {"data": ["Users", "Non-Users"]},
    "xAxis": {"type": "category", "data": years},
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "Users",
            "type": "bar",
            "data": users,
        },
        {
            "name": "Non-Users",
            "type": "bar",
            "data": non_users,
        },
    ],
}

# -------------------------------
# Solara Component for Visualization
# -------------------------------

@solara.component
def Page():
    with solara.VBox():
        #solara.Markdown("## Evolution of Digital Service Usage")
        solara.FigureEcharts(option=options, responsive=True)
