import numpy as np
from scipy.stats import norm

def bs_price(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
    """
    Calcule le prix analytique d'une option européenne via Black-Scholes.
    """
    if T <= 0:
        return max(S - K, 0.0) if option_type.lower() == "call" else max(K - S, 0.0)
        
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type.lower() == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type doit être 'call' ou 'put'")