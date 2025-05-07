# limits_to_success_bass.py
"""
HPV Vaccine-uptake SD model
using a Bass-diffusion stock-and-flow structure so
coverage approaches the ceiling smoothly.

dV/dt = R = (p + q*V/N) * U        (Bass flow, capped by capacity)
U     = N*max_coverage - V         (reachable but unvaccinated)

If capacity is low the curve flattens earlier; if capacity is high
the Bass dynamics dominate and produce the familiar logistic S-curve.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def simulate_bass_vaccine_model(
        p: float = 0.001,       # external pressure (per day)
        q: float = 0.40,        # social-proof strength
        capacity: int = 25_000, # health-system throughput (doses/day)
        max_coverage: float = 0.80,  # reachable share of population (0–1)
        N: int = 1_000_000,     # reachable population size
        V0: int = 0,            # initially vaccinated persons
        t_max: int = 730,       # horizon (days)
        dt: int = 1             # step (days)
) -> pd.DataFrame:
    steps = int(t_max/dt) + 1
    t = np.arange(0, t_max + dt, dt, dtype=int)

    V = np.empty(steps)
    U = np.empty(steps)
    R = np.empty(steps)

    V[0] = V0
    U[0] = N * max_coverage - V0

    for i in range(1, steps):
        bass_flow = (p + q * V[i-1] / N) * U[i-1]
        R[i-1] = min(capacity, bass_flow)

        dV = R[i-1] * dt
        V[i] = V[i-1] + dV
        U[i] = max(N * max_coverage - V[i], 0)   # can’t go below 0

    # final flow value for completeness
    bass_flow = (p + q * V[-1] / N) * U[-1]
    R[-1] = min(capacity, bass_flow)

    return pd.DataFrame({
        "time": t,
        "Vaccinated": V,
        "Unvaccinated": U,
        "Vaccination_rate": R
    })


if __name__ == "__main__":
    # ---- run baseline ----
    df = simulate_bass_vaccine_model()

    final_cov = df.Vaccinated.iloc[-1] / (df.Vaccinated.iloc[0] + df.Unvaccinated.iloc[0])
    print(f"Final coverage after two years: {final_cov:.2%}  "
          f"(should approach max_coverage = 80%)")

    # ---- plot stocks ----
    plt.figure(figsize=(8, 4))
    plt.plot(df.time, df.Unvaccinated, label="Unvaccinated")
    plt.plot(df.time, df.Vaccinated,   label="Vaccinated")
    plt.xlabel("Day"); plt.ylabel("People")
    plt.title("Stocks – Vaccine Uptake (Bass diffusion, limit 80 %)")
    plt.legend(); plt.tight_layout()

    # ---- plot flow ----
    plt.figure(figsize=(8, 4))
    plt.plot(df.time, df.Vaccination_rate)
    plt.xlabel("Day"); plt.ylabel("People / day")
    plt.title("Daily Vaccination Rate")
    plt.tight_layout()

    plt.show()
