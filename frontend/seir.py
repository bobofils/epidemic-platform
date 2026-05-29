import numpy as np

# =====================================================
# MODELE SEIR
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
    # ETATS INITIAUX
    # =================================================

    S = (
        population
        - exposed
        - infected
        - recovered
    )

    E = exposed

    I = infected

    R = recovered

    # =================================================
    # RESULTATS
    # =================================================

    results = {

        "days": [],
        "S": [],
        "E": [],
        "I": [],
        "R": []

    }

    # =================================================
    # BOUCLE TEMPORELLE
    # =================================================

    for day in range(days):

        # =============================================
        # EQUATIONS
        # =============================================

        new_exposed = (
            beta * S * I / population
        )

        new_infected = (
            sigma * E
        )

        new_recovered = (
            gamma * I
        )

        # =============================================
        # UPDATE
        # =============================================

        S -= new_exposed

        E += (
            new_exposed
            - new_infected
        )

        I += (
            new_infected
            - new_recovered
        )

        R += new_recovered

        # =============================================
        # SECURITE
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