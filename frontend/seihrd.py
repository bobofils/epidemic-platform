import numpy as np

# =====================================================
# MODELE SEIHRD STABLE
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

    S = population - exposed - infected
    E = exposed
    I = infected
    H = 0
    R = 0
    D = 0

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

        # =========================
        # FORCES EPIDEMIQUES
        # =========================

        new_exposed = beta * S * I / max(population, 1)
        new_infected = sigma * E
        new_recovered = gamma * I
        new_hospitalized = hosp_rate * I
        new_deaths = death_rate * H
        hospital_recovery = 0.05 * H

        # =========================
        # MISE A JOUR
        # =========================

        S = S - new_exposed
        E = E + new_exposed - new_infected
        I = I + new_infected - new_recovered - new_hospitalized
        H = H + new_hospitalized - new_deaths - hospital_recovery
        R = R + new_recovered + hospital_recovery
        D = D + new_deaths

        # =========================
        # SECURITE (IMPORTANT)
        # =========================

        S = max(S, 0)
        E = max(E, 0)
        I = max(I, 0)
        H = max(H, 0)
        R = max(R, 0)
        D = max(D, 0)

        # =========================
        # STOCKAGE
        # =========================

        results["days"].append(day)
        results["S"].append(S)
        results["E"].append(E)
        results["I"].append(I)
        results["H"].append(H)
        results["R"].append(R)
        results["D"].append(D)

    return results