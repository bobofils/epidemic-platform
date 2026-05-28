import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="COVID Dashboard",
    layout="wide"
)

st.title(
    "Plateforme de Simulation Epidémique"
)

model = st.sidebar.selectbox(
    "Modèle",
    ["SIR", "SEIR", "SEIHRD"]
)

population = st.sidebar.slider(
    "Population",
    100,
    1000000,
    10000
)

infected = st.sidebar.slider(
    "Infectés",
    1,
    1000,
    10
)

exposed = st.sidebar.slider(
    "Exposés",
    0,
    1000,
    20
)

beta = st.sidebar.slider(
    "Transmission β",
    0.1,
    1.0,
    0.3
)

gamma = st.sidebar.slider(
    "Guérison γ",
    0.01,
    1.0,
    0.1
)

sigma = st.sidebar.slider(
    "Incubation σ",
    0.01,
    1.0,
    0.2
)

hosp_rate = st.sidebar.slider(
    "Hospitalisation",
    0.01,
    1.0,
    0.1
)

death_rate = st.sidebar.slider(
    "Décès",
    0.001,
    0.5,
    0.02
)

recovery_h = st.sidebar.slider(
    "Guérison H",
    0.01,
    1.0,
    0.1
)

vaccination_rate = st.sidebar.slider(
    "Vaccination",
    0.0,
    0.1,
    0.01
)

barrier_effect = st.sidebar.slider(
    "Mesures barrières",
    0.0,
    1.0,
    0.3
)

lockdown_start = st.sidebar.slider(
    "Début confinement",
    0,
    300,
    30
)

lockdown_end = st.sidebar.slider(
    "Fin confinement",
    0,
    300,
    90
)

lockdown_strength = st.sidebar.slider(
    "Intensité confinement",
    0.0,
    1.0,
    0.5
)

days = st.sidebar.slider(
    "Jours",
    30,
    365,
    180
)

if st.button("Lancer Simulation"):

    payload = {

        "model": model,

        "population": population,

        "infected": infected,

        "exposed": exposed,

        "beta": beta,

        "gamma": gamma,

        "sigma": sigma,

        "hosp_rate": hosp_rate,

        "death_rate": death_rate,

        "recovery_h": recovery_h,

        "vaccination_rate": vaccination_rate,

        "barrier_effect": barrier_effect,

        "lockdown_start": lockdown_start,

        "lockdown_end": lockdown_end,

        "lockdown_strength": lockdown_strength,

        "days": days
    }

    response = requests.post(
        "http://127.0.0.1:8000/simulate",
        json=payload
    )

    data = response.json()

    fig = go.Figure()

    for key in data:

        if key != "days":

            fig.add_trace(
                go.Scatter(
                    x=data["days"],
                    y=data[key],
                    name=key
                )
            )

    st.plotly_chart(fig)

    if "H" in data:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Pic Hospitalier",
            int(max(data["H"]))
        )

        col2.metric(
            "Décès Totaux",
            int(data["D"][-1])
        )

        Rt = beta / gamma

        col3.metric(
            "R0 Effectif",
            round(Rt, 2)
        )

    df = pd.DataFrame(data)

    csv = df.to_csv(index=False)

    st.download_button(
        "Télécharger CSV",
        csv,
        "simulation.csv",
        "text/csv"
    )