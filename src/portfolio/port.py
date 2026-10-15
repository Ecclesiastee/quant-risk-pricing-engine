import sys
from pathlib import Path

# Dire à Python d'aller chercher à la racine du projet
sys.path.append(str(Path(__file__).resolve().parents[2]))

# les imports habituels viennent ensuite :
from typing import List, Dict, Any
from src.pricing.black_scholes import bs_price
from src.greeks.greeks import OptionGreeks

class Position:
    """Représente une position unique (Option ou Action)."""
    def __init__(self, asset_type: str, quantity: float, S: float, K: float = None, T: float = None, r: float = None, sigma: float = None, option_type: str = None):
        self.asset_type = asset_type.lower()  # "stock" ou "option"
        self.quantity = quantity              # Positif pour Long, négatif pour Short
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower() if option_type else None

class Portfolio:
    """Gestionnaire de portefeuille multi-actifs et agrégation des risques."""
    def __init__(self):
        self.positions: List[Position] = []

    def add_position(self, position: Position):
        """Ajoute une position au portefeuille."""
        self.positions.append(position)

    def total_value(self) -> float:
        """Calcule la valeur totale actuelle du portefeuille."""
        total = 0.0
        for pos in self.positions:
            if pos.asset_type == "stock":
                total += pos.quantity * pos.S
            elif pos.asset_type == "option":
                price = bs_price(pos.S, pos.K, pos.T, pos.r, pos.sigma, pos.option_type)
                total += pos.quantity * price
        return total

    def aggregate_greeks(self) -> Dict[str, float]:
        """Agrège les Greeks de l'ensemble des positions du portefeuille."""
        greeks = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        
        for pos in self.positions:
            if pos.asset_type == "stock":
                greeks["delta"] += pos.quantity * 1.0  # Le delta d'une action vaut 1
            elif pos.asset_type == "option":
                greeks["delta"] += pos.quantity * OptionGreeks.delta(pos.S, pos.K, pos.T, pos.r, pos.sigma, pos.option_type)
                greeks["gamma"] += pos.quantity * OptionGreeks.gamma(pos.S, pos.K, pos.T, pos.r, pos.sigma)
                greeks["vega"]  += pos.quantity * OptionGreeks.vega(pos.S, pos.K, pos.T, pos.r, pos.sigma)
                greeks["theta"] += pos.quantity * OptionGreeks.theta(pos.S, pos.K, pos.T, pos.r, pos.sigma, pos.option_type)
                greeks["rho"]   += pos.quantity * OptionGreeks.rho(pos.S, pos.K, pos.T, pos.r, pos.sigma, pos.option_type)
                
        return greeks