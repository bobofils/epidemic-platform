# Plateforme de Simulation Épidémique

## Description

Cette application web permet de simuler l’évolution d’une épidémie avec différents modèles mathématiques :

- SIR
- SEIR
- SEIHRD

L’utilisateur peut modifier plusieurs paramètres :

- transmission
- incubation
- hospitalisation
- vaccination
- confinement
- mesures barrières

---

# Fonctionnalités

## Modèles

- SIR
- SEIR
- SEIHRD

## Interventions

- Confinement
- Vaccination
- Mesures barrières

## Visualisations

- Courbes S, E, I, H, R, D
- Pic hospitalier
- Décès totaux
- R0 effectif

## Export

- CSV
- PDF

---

# Technologies

## Backend

- FastAPI
- SciPy
- NumPy

## Frontend

- Streamlit
- Plotly

---

# Installation

## Cloner le projet

git clone https://github.com/bobofils/epidemic-platform.git

---

# Installer les dépendances

pip install -r requirements.txt

---

# Lancer le backend

uvicorn backend.main:app --reload

---

# Lancer le frontend

streamlit run frontend/app.py

---

# Auteur

Projet universitaire de simulation épidémique.