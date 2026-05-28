import numpy as np
from scipy.integrate import odeint


def equations(
    y,
    t,
    beta,
    sigma,
    gamma,
    hosp_rate,
    death_rate,
    recovery_h,
    vaccination_rate,
    barrier_effect,
    lockdown_start,
    lockdown_end,
    lockdown_strength
):

    S, E, I, H, R, D = y

    beta = beta * (
        1 - barrier_effect
    )

    if (
        t >= lockdown_start
        and t <= lockdown_end
    ):

        beta = beta * (
            1 - lockdown_strength
        )

    dSdt = (
        -beta * S * I
        - vaccination_rate * S
    )

    dEdt = (
        beta * S * I
        - sigma * E
    )

    dIdt = (
        sigma * E
        - gamma * I
        - hosp_rate * I
    )

    dHdt = (
        hosp_rate * I
        - death_rate * H
        - recovery_h * H
    )

    dRdt = (
        gamma * I
        + recovery_h * H
        + vaccination_rate * S
    )

    dDdt = death_rate * H

    return [
        dSdt,
        dEdt,
        dIdt,
        dHdt,
        dRdt,
        dDdt
    ]


def run_seihrd(
    population,
    exposed,
    infected,
    beta,
    sigma,
    gamma,
    hosp_rate,
    death_rate,
    recovery_h,
    vaccination_rate,
    barrier_effect,
    lockdown_start,
    lockdown_end,
    lockdown_strength,
    days
):

    S0 = (
        population
        - exposed
        - infected
    )

    y0 = [
        S0,
        exposed,
        infected,
        0,
        0,
        0
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
            gamma,
            hosp_rate,
            death_rate,
            recovery_h,
            vaccination_rate,
            barrier_effect,
            lockdown_start,
            lockdown_end,
            lockdown_strength
        )
    )

    return {

        "days": t.tolist(),

        "S": result[:, 0].tolist(),

        "E": result[:, 1].tolist(),

        "I": result[:, 2].tolist(),

        "H": result[:, 3].tolist(),

        "R": result[:, 4].tolist(),

        "D": result[:, 5].tolist()
    }