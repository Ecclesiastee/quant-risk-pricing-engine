import numpy as np
from scipy.stats import norm

class OptionGreeks:
    """Calcul analytique des Greeks Black-Scholes."""
    
    @staticmethod
    def delta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return norm.cdf(d1) if option_type.lower() == "call" else norm.cdf(d1) - 1.0

    @staticmethod
    def gamma(S: float, K: float, T: float, r: float, sigma: float) -> float:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return norm.pdf(d1) / (S * sigma * np.sqrt(T))

    @staticmethod
    def vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return S * norm.pdf(d1) * np.sqrt(T)

    @staticmethod
    def theta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        if option_type.lower() == "call":
            return term1 - r * K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return term1 + r * K * np.exp(-r * T) * norm.cdf(-d2)

    @staticmethod
    def rho(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type.lower() == "call":
            return K * T * np.exp(-r * T) * norm.cdf(d2)
        else:
            return -K * T * np.exp(-r * T) * norm.cdf(-d2)