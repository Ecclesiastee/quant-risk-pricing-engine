import numpy as np
import pandas as pd
from arch import arch_model
from typing import Dict, Any

class GARCHVolatility:
    """
    Modélisation et prévision de la volatilité historique via GARCH(1,1).
    """
    def __init__(self, returns: pd.Series):
        """
        Paramètres:
            returns : Série temporelle des rendements logarithemiques (log returns).
        """
        self.returns = returns.dropna() * 100  # Conversion en pourcentage pour le package arch
        self.model = arch_model(self.returns, vol='Garch', p=1, q=1, dist='normal')
        self.fit_result = None

    def fit(self) -> Dict[str, Any]:
        """Ajuste le modèle GARCH(1,1) aux données de rendement."""
        self.fit_result = self.model.fit(disp='off')
        
        omega = self.fit_result.params['omega']
        alpha = self.fit_result.params['alpha[1]']
        beta = self.fit_result.params['beta[1]']
        
        # Volatilité de long terme (Unconditional Volatility)
        long_run_vol = np.sqrt(omega / (1 - alpha - beta)) * np.sqrt(252) / 100
        
        return {
            "omega": omega,
            "alpha": alpha,
            "beta": beta,
            "persistence": alpha + beta,
            "annualized_long_run_vol": long_run_vol
        }

    def forecast_volatility(self, horizon_days: int = 1) -> float:
        """
        Prévoit la volatilité annualisée à un horizon donné.
        """
        if self.fit_result is None:
            self.fit()
            
        forecast = self.fit_result.forecast(horizon=horizon_days)
        daily_variance_forecast = forecast.variance.iloc[-1, -1]
        
        # Volatilité quotidienne convertie en volatilité annualisée
        annualized_vol = np.sqrt(daily_variance_forecast) * np.sqrt(252) / 100
        return float(annualized_vol)