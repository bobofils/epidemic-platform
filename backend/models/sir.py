import numpy as np
from scipy.integrate import odeint


def equations(y, t, beta, gamma):

    S, I, R = y

    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I

    return [dSdt, dIdt, dRdt]


def run_sir(
    population,
    infected,
    recovered,
    beta,
    gamma,
    days
):

    susceptible = (
        population
        - infected
        - recovered
    )

    y0 = [
        susceptible,
        infected,
        recovered
    ]

    t = np.linspace(
        0,
        days,
        days
    )

    result = odeint(
        equations,
        y0,
        t,
        args=(beta, gamma)
    )

    return {
        "days": t.tolist(),
        "S": result[:, 0].tolist(),
        "I": result[:, 1].tolist(),
        "R": result[:, 2].tolist()
    }