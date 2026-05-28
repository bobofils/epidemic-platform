import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from sir import run_sir
from seir import run_seir
from seihrd import run_seihrd

# =====================================================
# CONFIGURATION PAGE
# =====================================================

st.set_page_config(
    page_title="Plateforme Epidémique",
    layout="wide"
)

# =====================================================
# TITRE
# =====================================================

st.title("Plateforme de Simulation Epidémique")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Paramètres")

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
    0.10,
    1.00,
    0.30
)

gamma = st.sidebar.slider(
    "Guérison γ",
    0.01,
    1.00,
    0.10
)

sigma = st.sidebar.slider(
    "Incubation σ",
    0.01,
    1.00,
    0.20
)

hosp_rate = st.sidebar.slider(
    "Hospitalisation",
    0.01,
    1.00,
    0.10
)

death_rate = st.sidebar.slider(
    "Décès",
    0.00,
    0.50,
    0.02
)

vaccination_rate = st.sidebar.slider(
    "Vaccination",
    0.00,
    0.10,
    0.01
)

barrier_effect = st.sidebar.slider(
    "Mesures barrières",
    0.00,
    1.00,
    0.30
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
    0.00,
    1.00,
    0.50
)

days = st.sidebar.slider(
    "Jours",
    30,
    365,
    180
)

# =====================================================
# BOUTON
# =====================================================

if st.button("Lancer Simulation"):

    # -------------------------------------------------
    # PARAMETRES MODIFIES
    # -------------------------------------------------

    effective_beta = beta

    # Mesures barrières
    effective_beta = effective_beta * (
        1 - barrier_effect
    )

    # Confinement
    if lockdown_start < lockdown_end:

        effective_beta = effective_beta * (
            1 - lockdown_strength
        )

    # Vaccination
    vaccinated_population = int(
        population * vaccination_rate
    )

    adjusted_population = (
        population - vaccinated_population
    )

    # -------------------------------------------------
    # MODELE SIR
    # -------------------------------------------------

    if model == "SIR":

        data = run_sir(
            adjusted_population,
            infected,
            0,
            effective_beta,
            gamma,
            days
        )

    # -------------------------------------------------
    # MODELE SEIR
    # -------------------------------------------------

    elif model == "SEIR":

        data = run_seir(
            adjusted_population,
            exposed,
            infected,
            0,
            effective_beta,
            sigma,
            gamma,
            days
        )

    # -------------------------------------------------
    # MODELE SEIHRD
    # -------------------------------------------------

    elif model == "SEIHRD":

        data = run_seihrd(
            adjusted_population,
            exposed,
            infected,
            effective_beta,
            sigma,
            gamma,
            hosp_rate,
            death_rate,
            days
        )

    # -------------------------------------------------
    # DATAFRAME
    # -------------------------------------------------

    df = pd.DataFrame(data)

    # -------------------------------------------------
    # GRAPHIQUES
    # -------------------------------------------------

    fig = go.Figure()

    for column in df.columns:

        if column != "days":

            fig.add_trace(

                go.Scatter(
                    x=df["days"],
                    y=df[column],
                    mode="lines",
                    name=column
                )

            )

    fig.update_layout(
        title="Simulation Epidémique",
        template="plotly_dark",
        xaxis_title="Temps (jours)",
        yaxis_title="Population",
        height=650
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------------------------------
    # INDICATEURS
    # -------------------------------------------------

    st.subheader("Indicateurs")

    col1, col2, col3 = st.columns(3)

    peak_infected = int(
        max(df["I"])
    )

    col1.metric(
        "Pic Infectieux",
        peak_infected
    )

    if "H" in df.columns:

        peak_hospital = int(
            max(df["H"])
        )

    else:

        peak_hospital = 0

    col2.metric(
        "Pic Hospitalier",
        peak_hospital
    )

    if "D" in df.columns:

        total_deaths = int(
            df["D"].iloc[-1]
        )

    else:

        total_deaths = 0

    col3.metric(
        "Décès Totaux",
        total_deaths
    )

    Rt = effective_beta / gamma

    st.metric(
        "R0 Effectif",
        round(Rt, 2)
    )

    # -------------------------------------------------
    # TABLEAU
    # -------------------------------------------------

    st.subheader("Données")

    st.dataframe(df)

    # -------------------------------------------------
    # EXPORT CSV
    # -------------------------------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="Télécharger CSV",
        data=csv,
        file_name="simulation.csv",
        mime="text/csv"
    )

    # -------------------------------------------------
    # MESSAGE
    # -------------------------------------------------

    st.success(
        "Simulation terminée avec succès."
    )
