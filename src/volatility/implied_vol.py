import numpy as np
from scipy.optimize import brentq
from src.pricing.black_scholes import bs_price
from src.greeks.greeks import OptionGreeks

def implied_volatility(market_price: float, S: float, K: float, T: float, r: float, option_type: str = "call") -> float:
    """
    Calcule la volatilité implicite d'une option via la méthode hybride Newton-Raphson / Brent.
    
    Paramètres:
        market_price : Prix observé sur le marché
        S : Prix du sous-jacent (Spot)
        K : Prix d'exercice (Strike)
        T : Maturité (en années)
        r : Taux sans risque (annuel)
        option_type : "call" ou "put"
        
    Retourne:
        Volatilité implicite (ex: 0.20 pour 20%)
    """
    # Valeur intrinsèque minimale
    intrinsic_value = max(S - K, 0.0) if option_type.lower() == "call" else max(K - S, 0.0)
    if market_price < intrinsic_value:
        raise ValueError("Le prix de marché est inférieur à la valeur intrinsèque de l'option.")

    # Fonction objectif : f(sigma) = Prix_BS(sigma) - Prix_Marché = 0
    def objective_function(sigma: float) -> float:
        return bs_price(S, K, T, r, sigma, option_type) - market_price

    # Tentative 1 : Algorithme de Newton-Raphson rapide basé sur le Vega
    sigma_est = 0.20  # Point de départ initial (20%)
    for _ in range(50):
        price_diff = objective_function(sigma_est)
        vega = OptionGreeks.vega(S, K, T, r, sigma_est)
        
        if abs(price_diff) < 1e-6:
            return sigma_est
        if abs(vega) < 1e-8:
            break  # Passage à Brent en cas de Vega trop faible
            
        sigma_est -= price_diff / vega

    # Tentative 2 : Méthode robuste de Brent en cas de non-convergence de Newton-Raphson
    try:
        return brentq(objective_function, a=1e-4, b=5.0, xtol=1e-6)
    except Exception:
        return np.nan