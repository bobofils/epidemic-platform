import numpy as np

# =====================================================
# MODELE SEIR STABLE (PRODUCTION)
# =====================================================

def run_seir(
    population,
    exposed,
    infected,
    recovered,
    beta,
    sigma,
    gamma,
    days
):

    # =================================================
    # INITIALISATION
    # =================================================

    S = population - exposed - infected - recovered
    E = exposed
    I = infected
    R = recovered

    # =================================================
    # STOCKAGE
    # =================================================

    results = {
        "days": [],
        "S": [],
        "E": [],
        "I": [],
        "R": []
    }

    # =================================================
    # SIMULATION
    # =================================================

    for day in range(days):

        # =============================================
        # DYNAMIQUE EPIDEMIQUE
        # =============================================

        new_exposed = beta * S * I / max(population, 1)
        new_infected = sigma * E
        new_recovered = gamma * I

        # =============================================
        # UPDATE
        # =============================================

        S = S - new_exposed
        E = E + new_exposed - new_infected
        I = I + new_infected - new_recovered
        R = R + new_recovered

        # =============================================
        # SECURITE NUMERIQUE
        # =============================================

        S = max(S, 0)
        E = max(E, 0)
        I = max(I, 0)
        R = max(R, 0)

        # =============================================
        # SAVE
        # =============================================

        results["days"].append(day)
        results["S"].append(S)
        results["E"].append(E)
        results["I"].append(I)
        results["R"].append(R)

    return results