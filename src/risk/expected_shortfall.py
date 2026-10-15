import numpy as np

class ExpectedShortfall:
    """Calculateur d'Expected Shortfall (ES / CVaR)."""
    
    @staticmethod
    def historical_es(returns: np.ndarray, portfolio_value: float, confidence_level: float = 0.95) -> float:
        """ES Historique : moyenne des pertes pires que la VaR historique."""
        percentile = (1 - confidence_level) * 100
        var_cutoff = np.percentile(returns, percentile)
        tail_losses = returns[returns <= var_cutoff]
        return -np.mean(tail_losses) * portfolio_value