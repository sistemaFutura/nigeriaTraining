# limits_to_success_vaccine_v2.py
"""
Pure-Python ‘Limits to Growth vaccine-uptake model
with a baseline campaign to avoid zero-demand dead start
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def simulate_vaccine_uptake(
        beta: float = .4,           # social-proof sensitivity  [1/yr]
        gamma: float = 2.0,           # hesitancy growth factor
        capacity: int = 25_000,       # max doses/yr
        base_campaign: int = 1000,       # <-- set >0 for Option B
        U0: int = 100_000,         # initial reachable pop
        V0: int = 0,              
        t_max: int = 20, dt: int = 1
) -> pd.DataFrame:
    steps = t_max // dt + 1
    t = np.arange(0, t_max + dt, dt, dtype=int)

    U = np.empty(steps)
    V = np.empty(steps)
    R = np.empty(steps)
    H = np.empty(steps)

    U[0], V[0] = U0, V0

    for i in range(1, steps):
        coverage = V[i-1] / (U[i-1] + V[i-1])
        H[i-1] = 1 - np.exp(-gamma * coverage)

        demand = base_campaign + beta * V[i-1] * (1 - H[i-1])
        R[i-1] = min(capacity, demand, U[i-1])      # can’t vaccinate more than U

        U[i] = U[i-1] - R[i-1] * dt
        V[i] = V[i-1] + R[i-1] * dt

    # final auxiliaries
    coverage_last = V[-1] / (U[-1] + V[-1])
    H[-1] = 1 - np.exp(-gamma * coverage_last)
    R[-1] = min(capacity, base_campaign + beta * V[-1] * (1 - H[-1]), U[-1])

    return pd.DataFrame({
        "time": t,
        "Unvaccinated": U,
        "Vaccinated": V,
        "Vaccination_rate": R,
        "Hesitancy_fraction": H
    })


if __name__ == "__main__":
    # ——— Choose option by tweaking V0 or base_campaign ———
    df = simulate_vaccine_uptake(
        V0=1_000,          # Option A: seed stock
        base_campaign=0    # Option B: set this to e.g. 500 if you prefer
    )

    print(df.head())

    # ---- Plot stocks ----
    plt.figure(figsize=(8, 4))
    plt.plot(df.time, df.Unvaccinated, label="Unvaccinated")
    plt.plot(df.time, df.Vaccinated,   label="Vaccinated")
    plt.xlabel("Year"); plt.ylabel("People")
    plt.title("HPV Vaccine Uptake (Limits to Success)")
    plt.legend(); plt.tight_layout()

    # ---- Plot flow + hesitancy ----
    plt.figure(figsize=(8, 4))
    plt.plot(df.time, df.Vaccination_rate,   label="Vaccination rate")
    plt.plot(df.time, df.Hesitancy_fraction, label="Hesitancy fraction")
    plt.xlabel("Year")
    plt.ylabel("Rate (people/year) | Fraction (0–1)")
    plt.title("Flow & Auxiliary")
    plt.legend(); plt.tight_layout()

    plt.show()

    df.to_csv("vaccine_limits_results_v2.csv", index=False)
    print("Done → vaccine_limits_results_v2.csv")
