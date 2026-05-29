import numpy as np

def run_sir(population, infected, recovered, beta, gamma, days):

    S = population - infected - recovered
    I = infected
    R = recovered

    results = {"days": [], "S": [], "I": [], "R": []}

    for t in range(days):

        new_inf = beta * S * I / max(population, 1)
        new_rec = gamma * I

        S -= new_inf
        I += new_inf - new_rec
        R += new_rec

        S = max(S, 0)
        I = max(I, 0)
        R = max(R, 0)

        results["days"].append(t)
        results["S"].append(S)
        results["I"].append(I)
        results["R"].append(R)

    return results