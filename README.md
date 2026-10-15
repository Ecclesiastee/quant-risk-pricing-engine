# Quant Risk & Pricing Engine 📈

Une solution complète et modulaire développée sous Python pour le **pricing d'options**, l'**analyse des risques de marché** (Value at Risk, Expected Shortfall, Stress Testing) et la **simulation de scénarios de crise**.

Le projet propose une architecture orientée objet propre ainsi qu'un dashboard web interactif réalisé avec **Streamlit** et **Plotly**.

---

## 📌 Fonctionnalités Principales

### 1. Moteur de Pricing d'Options (`src/pricing`)
- **Modèle Black-Scholes :** Pricing analytique d'options européennes (Call / Put) et calcul complet des Grecques ($\Delta, \Gamma, \Vega, \Theta, \Rho$).
- **Simulations de Monte-Carlo :** Modélisation par Mouvement Brunien Géométrique (GBM) avec convergence des intervalles de confiance.
- **Surface de Volatilité :** Visualisation et analyse du smile de volatilité.

### 2. Gestion & Mesure des Risques (`src/risk`)
- **Value at Risk (VaR) & Expected Shortfall (ES) :**
  - Approche Paramétrique (distribution normale / Student).
  - Approche Historique.
  - Simulation Monte-Carlo.
- **Stress Testing & Scénarios de Crise :** Simulation d'impacts sur portefeuille selon divers chocs de marché (chocs de taux, pics de volatilité, krachs historiques).
- **Backtesting :** Évaluation de la précision des modèles de risque (tests de couverture de Kupiec et Christoffersen).

### 3. Application Web & Visualisation (`src/app.py`)
- Dashboard interactif **Streamlit** permettant de :
  - Configurer les paramètres des options et du portefeuille en temps réel.
  - Visualiser la décomposition des payoffs et des risques via des graphiques dynamiques **Plotly**.
  - Générer des rapports synthétiques sur les métriques de risque.

---

## 🛠️ Stack Technique

- **Langage :** Python 3.10+
- **Calcul Numérique & Données :** `NumPy`, `SciPy`, `Pandas`
- **Visualisation :** `Plotly`, `Matplotlib`, `Seaborn`
- **Interface Web :** `Streamlit`
- **Environnement & Outils :** `Git`, `Jupyter Notebook`

---

## 🏗️ Structure du Projet

```text
quant-risk-pricing-engine/
├── src/
│   ├── pricing/          # Modèles analytiques et Monte-Carlo
│   ├── risk/             # Calculs de VaR, ES et stress testing
│   ├── portfolio/        # Gestion et agrégation des positions
│   └── app.py            # Application Streamlit
├── data/                 # Données de marché et séries temporelles
├── notebooks/            # Explorations et analyses d'exemples
├── requirements.txt      # Dépendances Python
└── README.md             # Documentation du projet
