import numpy as np

def run_seir(population, exposed, infected, recovered, beta, sigma, gamma, days):

    S = population - exposed - infected - recovered
    E = exposed
    I = infected
    R = recovered

    results = {"days": [], "S": [], "E": [], "I": [], "R": []}

    for t in range(days):

        new_exposed = beta * S * I / max(population, 1)
        new_infected = sigma * E
        new_recovered = gamma * I

        S -= new_exposed
        E += new_exposed - new_infected
        I += new_infected - new_recovered
        R += new_recovered

        S = max(S, 0)
        E = max(E, 0)
        I = max(I, 0)
        R = max(R, 0)

        results["days"].append(t)
        results["S"].append(S)
        results["E"].append(E)
        results["I"].append(I)
        results["R"].append(R)

    return results