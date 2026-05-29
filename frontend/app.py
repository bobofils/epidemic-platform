import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from sir import run_sir
from seir import run_seir
from seihrd import run_seihrd

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Plateforme Epidémique",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Plateforme de Simulation Epidémique")

# =====================================================
# PARAMETRES
# =====================================================

st.sidebar.header("Paramètres")

model = st.sidebar.selectbox("Modèle", ["SIR", "SEIR", "SEIHRD"])

population = st.sidebar.slider("Population", 100, 1000000, 10000)
infected = st.sidebar.slider("Infectés", 1, 1000, 10)
exposed = st.sidebar.slider("Exposés", 0, 1000, 20)

beta = st.sidebar.slider("β", 0.1, 1.0, 0.3)
gamma = st.sidebar.slider("γ", 0.01, 1.0, 0.1)
sigma = st.sidebar.slider("σ", 0.01, 1.0, 0.2)

hosp_rate = st.sidebar.slider("Hospitalisation", 0.0, 1.0, 0.1)
death_rate = st.sidebar.slider("Décès", 0.0, 0.5, 0.02)

vaccination_rate = st.sidebar.slider("Vaccination", 0.0, 0.1, 0.01)
barrier_effect = st.sidebar.slider("Barrières", 0.0, 1.0, 0.3)

lockdown_start = st.sidebar.slider("Début confinement", 0, 300, 30)
lockdown_end = st.sidebar.slider("Fin confinement", 0, 300, 90)
lockdown_strength = st.sidebar.slider("Intensité confinement", 0.0, 1.0, 0.5)

days = st.sidebar.slider("Jours", 30, 365, 180)

# =====================================================
# SIMULATION
# =====================================================

if st.button("Lancer Simulation"):

    try:
        # =========================
        # β effectif
        # =========================
        effective_beta = beta * (1 - barrier_effect)

        if lockdown_start < lockdown_end:
            effective_beta *= (1 - lockdown_strength)

        vaccinated_population = int(population * vaccination_rate)
        adjusted_population = max(population - vaccinated_population, 1)

        # =========================
        # MODELES (SAFE CALLS)
        # =========================

        if model == "SIR":
            data = run_sir(adjusted_population, infected, 0, effective_beta, gamma, days)

        elif model == "SEIR":
            data = run_seir(adjusted_population, exposed, infected, 0, effective_beta, sigma, gamma, days)

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

        df = pd.DataFrame(data)

        # =========================
        # GRAPH
        # =========================

        fig = go.Figure()

        for col in df.columns:
            if col != "days":
                fig.add_trace(go.Scatter(x=df["days"], y=df[col], name=col))

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # INDICATEURS SAFE
        # =========================

        peak_I = int(np.nanmax(df["I"])) if "I" in df else 0
        peak_H = int(np.nanmax(df["H"])) if "H" in df else 0
        deaths = int(df["D"].iloc[-1]) if "D" in df else 0

        Rt = round(effective_beta / max(gamma, 1e-6), 2)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Pic Infectieux", peak_I)
        col2.metric("Pic Hospitalier", peak_H)
        col3.metric("Décès", deaths)
        col4.metric("R0", Rt)

        # =========================
        # CSV
        # =========================

        st.download_button("CSV", df.to_csv(index=False), "data.csv")

        # =========================
        # EXCEL SAFE
        # =========================

        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="data")

        excel_buffer.seek(0)

        st.download_button(
            "Excel",
            data=excel_buffer,
            file_name="simulation.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # =========================
        # PDF SAFE
        # =========================

        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer)

        styles = getSampleStyleSheet()

        content = [
            Paragraph("Rapport Simulation Epidémique", styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"Pic Infectieux: {peak_I}", styles["Normal"]),
            Paragraph(f"Pic Hospitalier: {peak_H}", styles["Normal"]),
            Paragraph(f"Décès: {deaths}", styles["Normal"]),
            Paragraph(f"R0: {Rt}", styles["Normal"]),
        ]

        doc.build(content)
        pdf_buffer.seek(0)

        st.download_button(
            "PDF",
            pdf_buffer,
            "report.pdf",
            "application/pdf"
        )

        st.success("Simulation terminée avec succès")

    except Exception as e:
        st.error(f"Erreur simulation: {e}")