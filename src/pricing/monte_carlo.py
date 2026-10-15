import numpy as np
from typing import Tuple

def mc_price(S: float, K: float, T: float, r: float, sigma: float, 
             option_type: str = "call", n_sims: int = 100000, seed: int = 42) -> Tuple[float, float, Tuple[float, float]]:
    """
    Prix Monte-Carlo avec intervalle de confiance à 95%.
    """
    np.random.seed(seed)
    Z = np.random.standard_normal(n_sims)
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    if option_type.lower() == "call":
        payoffs = np.maximum(S_T - K, 0.0)
    else:
        payoffs = np.maximum(K - S_T, 0.0)
        
    discounted_payoffs = np.exp(-r * T) * payoffs
    price = float(np.mean(discounted_payoffs))
    std_err = float(np.std(discounted_payoffs) / np.sqrt(n_sims))
    
    ci_lower = price - 1.96 * std_err
    ci_upper = price + 1.96 * std_err
    
    return price, std_err, (ci_lower, ci_upper)