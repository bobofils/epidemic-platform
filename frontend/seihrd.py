import numpy as np

# =====================================================
# MODELE SEIHRD
# =====================================================

def run_seihrd(
    population,
    exposed,
    infected,
    beta,
    sigma,
    gamma,
    hosp_rate,
    death_rate,
    days
):

    S = population - infected - exposed
    E = exposed
    I = infected
    H = 0
    R = 0
    D = 0

    dt = 1

    results = {

        "days": [],
        "S": [],
        "E": [],
        "I": [],
        "H": [],
        "R": [],
        "D": []

    }

    for day in range(days):

        # =============================================
        # EQUATIONS
        # =============================================

        new_exposed = (
            beta * S * I / population
        )

        new_infected = sigma * E

        new_recovered = gamma * I

        new_hospitalized = hosp_rate * I

        new_deaths = death_rate * H

        hospital_recovery = 0.05 * H

        # =============================================
        # UPDATE
        # =============================================

        S -= new_exposed

        E += (
            new_exposed - new_infected
        )

        I += (
            new_infected
            - new_recovered
            - new_hospitalized
        )

        H += (
            new_hospitalized
            - new_deaths
            - hospital_recovery
        )

        R += (
            new_recovered
            + hospital_recovery
        )

        D += new_deaths

        # =============================================
        # SAVE
        # =============================================

        results["days"].append(day)

        results["S"].append(max(S, 0))

        results["E"].append(max(E, 0))

        results["I"].append(max(I, 0))

        results["H"].append(max(H, 0))

        results["R"].append(max(R, 0))

        results["D"].append(max(D, 0))

    return results