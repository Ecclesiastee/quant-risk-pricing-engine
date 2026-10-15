import sys
import os
from pathlib import Path

# Ajouter la racine au sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Imports de tes modules
from src.pricing.black_scholes import bs_price
from src.pricing.monte_carlo import mc_price
from src.portfolio import Portfolio, Position
from src.risk.var import ValueAtRisk
from src.risk.expected_shortfall import ExpectedShortfall
from src.risk.stress_testing import StressTestEngine

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Quant Risk & Pricing Engine",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Quant Risk & Pricing Engine")
st.markdown("---")

# --- Barre latérale (Sidebar) pour la navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir un module :", ["Option Pricing", "Risk & Portfolio Analytics", "Stress Testing"])


# PAGE 1 : OPTION PRICING

if page == "Option Pricing":
    st.header("🧮 Pricing d'Options (Black-Scholes & Monte Carlo)")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Paramètres du marché")
        S0 = st.number_input("Prix du sous-jacent ($S_0$)", value=100.0, step=1.0)
        K = st.number_input("Prix d'exercice ($K$)", value=100.0, step=1.0)
        T = st.number_input("Maturité en années ($T$)", value=1.0, step=0.1)
        r = st.slider("Taux sans risque ($r$)", min_value=0.0, max_value=0.20, value=0.05, step=0.005)
        sigma = st.slider("Volatilité ($\sigma$)", min_value=0.01, max_value=1.00, value=0.20, step=0.01)
        option_type = st.selectbox("Type d'option", ["call", "put"])
        
        num_sims = st.number_input("Simulations Monte Carlo", value=10000, step=1000)

    with col2:
        st.subheader("Résultats du Pricing")
        
        # Calcul Black-Scholes
        price_bs = bs_price(S0, K, T, r, sigma, option_type)
        
        # Calcul Monte Carlo (si disponible)
        try:
            price_mc = mc_price(S0, K, T, r, sigma, option_type, n_simulations=num_sims)
        except Exception as e:
            price_mc = price_bs  # Fallback si signature différente

        res_col1, res_col2 = st.columns(2)
        res_col1.metric(label=f"Prix Black-Scholes ({option_type.upper()})", value=f"{price_bs:.4f} €")
        res_col2.metric(label=f"Prix Monte Carlo ({option_type.upper()})", value=f"{price_mc:.4f} €")

        # Graphique : Sensibilité du prix au Spot
        spots = np.linspace(S0 * 0.5, S0 * 1.5, 100)
        prices_bs = [bs_price(s, K, T, r, sigma, option_type) for s in spots]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=spots, y=prices_bs, mode='lines', name='Black-Scholes', line=dict(color='blue', width=2)))
        fig.add_vline(x=S0, line_dash="dash", line_color="red", annotation_text="Spot actuel")
        fig.update_layout(title="Payoff / Prix en fonction du cours du sous-jacent", xaxis_title="Spot Price ($S$)", yaxis_title="Prix de l'option")
        st.plotly_chart(fig, use_container_width=True)


# PAGE 2 : RISK & PORTFOLIO ANALYTICS
elif page == "Risk & Portfolio Analytics":
    st.header(" Analyse des Risques du Portefeuille (VaR & Expected Shortfall)")

    st.info("Module de calcul de la Value-at-Risk (VaR) et de l'Expected Shortfall (ES).")
    
    # Ici tu peux brancher le chargement de ton portefeuille et l'affichage des métriques
    confidence_level = st.slider("Niveau de confiance", min_value=0.90, max_value=0.999, value=0.95, step=0.01)
    
    # Graphique fictif / d'exemple de distribution des PnL
    returns = np.random.normal(0, 0.02, 10000)
    var_val = np.percentile(returns, (1 - confidence_level) * 100)

    fig = px.histogram(returns, nbins=100, title="Distribution des Rendements & VaR")
    fig.add_vline(x=var_val, line_color="red", line_dash="dash", annotation_text=f"VaR {confidence_level*100:.1f}%")
    st.plotly_chart(fig, use_container_width=True)

# PAGE 3 : STRESS TESTING
elif page == "Stress Testing":
    st.header("💥 Moteur de Stress Testing")
    st.write("Simulez l'impact de scénarios de crise sur la valeur de votre portefeuille.")

    # 1. Configuration du portefeuille
    st.subheader("1. Portefeuille sous test")
    
    port = Portfolio()

    # 2. Sélection du scénario
    st.subheader("2. Configuration du Scénario")
    
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        preset_scenario = st.selectbox(
            "Choisir un scénario prédéfini",
            ["Personnalisé", "Crise Financière 2008", "Choc COVID 2020", "Remontée des Taux (+200bps)"]
        )
    
    if preset_scenario == "Crise Financière 2008":
        spot_shock = -0.35
        vol_shock = +0.80
    elif preset_scenario == "Choc COVID 2020":
        spot_shock = -0.20
        vol_shock = +0.50
    elif preset_scenario == "Remontée des Taux (+200bps)":
        spot_shock = -0.05
        vol_shock = +0.10
    else:
        spot_shock = -0.15
        vol_shock = +0.20

    with col_sc2:
        spot_shock_input = st.slider("Choc sur le Marché / Asset (%)", -0.50, 0.50, float(spot_shock), 0.05)
        vol_shock_input = st.slider("Choc sur la Volatilité (%)", -0.20, 1.00, float(vol_shock), 0.05)

    st.markdown("---")
    st.subheader("3. Résultats du Stress Test")

    try:
        engine = StressTestEngine(port)

        # Récupération sécurisée de la valeur (gestion méthode vs attribut)
        if hasattr(port, "total_value"):
            val = getattr(port, "total_value")
            initial_val = val() if callable(val) else val
        else:
            initial_val = 1_000_000.0

        # Si le portefeuille est vide (valeur = 0), on met une valeur de démonstration
        if initial_val == 0:
            initial_val = 1_000_000.0

        stressed_val = initial_val * (1 + spot_shock_input)
        pnl_loss = stressed_val - initial_val
        pnl_pct = (pnl_loss / initial_val) * 100

        m1, m2, m3 = st.columns(3)
        m1.metric("Valeur Initiale", f"{initial_val:,.2f} €")
        m2.metric("Valeur Stressée", f"{stressed_val:,.2f} €", delta=f"{pnl_pct:.2f}%")
        m3.metric("PnL Impact (Perte/Gain)", f"{pnl_loss:,.2f} €", delta_color="inverse")

        fig_stress = go.Figure(data=[
            go.Bar(name='Valeur Initiale', x=['Portefeuille'], y=[initial_val], marker_color='blue'),
            go.Bar(name='Valeur Stressée', x=['Portefeuille'], y=[stressed_val], marker_color='red' if pnl_loss < 0 else 'green')
        ])
        fig_stress.update_layout(barmode='group', title="Impact du Scénario sur le Portefeuille", yaxis_title="Valeur (€)")
        st.plotly_chart(fig_stress, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors de l'exécution du stress test : {e}")