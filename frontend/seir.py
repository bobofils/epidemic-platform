import numpy as np
from scipy.integrate import odeint


def equations(
    y,
    t,
    beta,
    sigma,
    gamma
):

    S, E, I, R = y

    dSdt = -beta * S * I

    dEdt = (
        beta * S * I
        - sigma * E
    )

    dIdt = (
        sigma * E
        - gamma * I
    )

    dRdt = gamma * I

    return [
        dSdt,
        dEdt,
        dIdt,
        dRdt
    ]


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

    susceptible = (
        population
        - exposed
        - infected
        - recovered
    )

    y0 = [
        susceptible,
        exposed,
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
        args=(
            beta,
            sigma,
            gamma
        )
    )

    return {
        "days": t.tolist(),
        "S": result[:, 0].tolist(),
        "E": result[:, 1].tolist(),
        "I": result[:, 2].tolist(),
        "R": result[:, 3].tolist()
    }