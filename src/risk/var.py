import numpy as np
from scipy.stats import norm

class ValueAtRisk:
    """Calculateur de Value-at-Risk (VaR) pour portefeuilles d'actifs."""
    
    @staticmethod
    def parametric_var(portfolio_value: float, vol_daily: float, confidence_level: float = 0.95, days: int = 1) -> float:
        """VaR Paramétrique sous hypothèse de normalité des rendements."""
        z_score = norm.ppf(confidence_level)
        return portfolio_value * z_score * vol_daily * np.sqrt(days)

    @staticmethod
    def historical_var(returns: np.ndarray, portfolio_value: float, confidence_level: float = 0.95) -> float:
        """VaR Historique non-paramétrique basée sur les centiles historiques."""
        percentile = (1 - confidence_level) * 100
        loss_percentile = np.percentile(returns, percentile)
        return -loss_percentile * portfolio_value

    @staticmethod
    def monte_carlo_var(portfolio_value: float, mu_daily: float, vol_daily: float, confidence_level: float = 0.95, n_sims: int = 50000) -> float:
        """VaR estimée par simulation Monte-Carlo des rendements futuribles."""
        np.random.seed(42)
        simulated_returns = np.random.normal(mu_daily, vol_daily, n_sims)
        percentile = (1 - confidence_level) * 100
        loss_percentile = np.percentile(simulated_returns, percentile)
        return -loss_percentile * portfolio_value