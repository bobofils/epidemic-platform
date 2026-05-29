import numpy as np

def run_seihrd(population, exposed, infected, beta, sigma, gamma, hosp_rate, death_rate, days):

    S = population - exposed - infected
    E = exposed
    I = infected

    # IMPORTANT: init hospitalisé réaliste
    H = max(1, int(0.01 * infected))
    R = 0
    D = 0

    results = {
        "days": [], "S": [], "E": [], "I": [], "H": [], "R": [], "D": []
    }

    for t in range(days):

        pop = max(population, 1)

        new_exposed = beta * S * I / pop
        new_infected = sigma * E

        # flux réaliste
        new_hospital = hosp_rate * I
        new_recovered = gamma * I

        # décès dépend des hospitalisés (plus réaliste)
        new_deaths = death_rate * max(H, 1)

        hospital_recovery = 0.05 * H

        S -= new_exposed
        E += new_exposed - new_infected
        I += new_infected - new_recovered - new_hospital
        H += new_hospital - new_deaths - hospital_recovery
        R += new_recovered + hospital_recovery
        D += new_deaths

        S = max(S, 0)
        E = max(E, 0)
        I = max(I, 0)
        H = max(H, 0)
        R = max(R, 0)
        D = max(D, 0)

        results["days"].append(t)
        results["S"].append(S)
        results["E"].append(E)
        results["I"].append(I)
        results["H"].append(H)
        results["R"].append(R)
        results["D"].append(D)

    return results