import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from sir import run_sir
from seir import run_seir
from seihrd import run_seihrd

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Plateforme Epidémique",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# STYLE
# =====================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TITRE
# =====================================================

st.title("Plateforme de Simulation Epidémique")

st.markdown(
    "Simulation avancée SIR / SEIR / SEIHRD"
)

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
# COMPARAISON
# =====================================================

st.sidebar.subheader("Comparaison")

multi_scenario = st.sidebar.checkbox(
    "Activer comparaison"
)

# =====================================================
# PDF
# =====================================================

def generate_pdf(
    peak_I,
    peak_H,
    deaths,
    Rt
):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Rapport Simulation Epidémique",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Pic Infectieux : {peak_I}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Pic Hospitalier : {peak_H}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Décès Totaux : {deaths}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"R0 Effectif : {Rt:.2f}",
            styles["Normal"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer

# =====================================================
# SIMULATION
# =====================================================

if st.button("Lancer Simulation"):

    effective_beta = beta

    effective_beta *= (
        1 - barrier_effect
    )

    if lockdown_start < lockdown_end:

        effective_beta *= (
            1 - lockdown_strength
        )

    vaccinated_population = int(
        population * vaccination_rate
    )

    adjusted_population = (
        population - vaccinated_population
    )

    # =================================================
    # COMPARAISON
    # =================================================

    if multi_scenario:

        scenarios = [

            {
                "name": "Normal",
                "beta": beta
            },

            {
                "name": "Réduction 30%",
                "beta": beta * 0.7
            },

            {
                "name": "Réduction 50%",
                "beta": beta * 0.5
            }

        ]

        fig_compare = go.Figure()

        for scenario in scenarios:

            data_compare = run_sir(
                adjusted_population,
                infected,
                0,
                scenario["beta"],
                gamma,
                days
            )

            df_compare = pd.DataFrame(
                data_compare
            )

            fig_compare.add_trace(

                go.Scatter(
                    x=df_compare["days"],
                    y=df_compare["I"],
                    mode="lines",
                    name=scenario["name"]
                )

            )

        fig_compare.update_layout(
            title="Comparaison Multi-Scénarios",
            template="plotly_dark",
            height=650
        )

        st.plotly_chart(
            fig_compare,
            use_container_width=True
        )

    # =================================================
    # MODELES
    # =================================================

    if model == "SIR":

        data = run_sir(
            adjusted_population,
            infected,
            0,
            effective_beta,
            gamma,
            days
        )

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

    # =================================================
    # DATAFRAME
    # =================================================

    df = pd.DataFrame(data)

    # =================================================
    # GRAPHIQUE
    # =================================================

    fig = go.Figure()

    for column in df.columns:

        if column != "days":

            fig.add_trace(

                go.Scatter(
                    x=df["days"],
                    y=df[column],
                    mode="lines",
                    name=column,
                    line=dict(width=3)
                )

            )

    fig.update_layout(
        title="Simulation Epidémique",
        template="plotly_dark",
        xaxis_title="Temps (jours)",
        yaxis_title="Population",
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =================================================
    # INDICATEURS
    # =================================================

    st.subheader("Indicateurs")

    col1, col2, col3, col4 = st.columns(4)

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

    col4.metric(
        "R0 Effectif",
        round(Rt, 2)
    )

    # =================================================
    # TABLEAU
    # =================================================

    st.subheader("Données")

    st.dataframe(df)

    # =================================================
    # EXPORT CSV
    # =================================================

    csv = df.to_csv(index=False)

    st.download_button(
        label="Télécharger CSV",
        data=csv,
        file_name="simulation.csv",
        mime="text/csv"
    )

    # =================================================
    # EXPORT EXCEL
    # =================================================

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Simulation"
        )

    excel_buffer.seek(0)

    st.download_button(
        "Télécharger Excel",
        data=excel_buffer,
        file_name="simulation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =================================================
    # EXPORT PDF
    # =================================================

    pdf = generate_pdf(
        peak_infected,
        peak_hospital,
        total_deaths,
        Rt
    )

    st.download_button(
        "Télécharger PDF",
        data=pdf,
        file_name="rapport.pdf",
        mime="application/pdf"
    )

    # =================================================
    # MESSAGE
    # =================================================

    st.success(
        "Simulation terminée avec succès."
    )