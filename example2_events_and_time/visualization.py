import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load data from the CSV file
    results_df = pd.read_csv("model_results.csv")

    # Configure the chart
    plt.figure(figsize=(10, 6))
    plt.plot(results_df["Step"], results_df["Users"], label="Users", color="blue", marker="o")
    plt.plot(results_df["Step"], results_df["Non-Users"], label="Non-Users", color="red", marker="o")
    plt.title("Digital Service Usage Over Time", fontsize=16)
    plt.xlabel("Step", fontsize=12)
    plt.ylabel("Number of People", fontsize=12)
    plt.legend()
    plt.grid(True)

    # Show the chart
    plt.tight_layout()
    plt.show()
