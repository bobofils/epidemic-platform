import numpy as np

def run_sir(population, infected, recovered, beta, gamma, days):

    S = population - infected - recovered
    I = infected
    R = recovered

    results = {
        "days": [],
        "S": [],
        "I": [],
        "R": []
    }

    for t in range(days):

        pop = max(population, 1)

        # dynamique SIR
        new_inf = beta * S * I / pop
        new_rec = gamma * I

        S = S - new_inf
        I = I + new_inf - new_rec
        R = R + new_rec

        # sécurité numérique
        S = max(S, 0)
        I = max(I, 0)
        R = max(R, 0)

        # stockage
        results["days"].append(t)
        results["S"].append(S)
        results["I"].append(I)
        results["R"].append(R)

    return results