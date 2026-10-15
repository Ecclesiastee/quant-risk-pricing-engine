from typing import Dict
from src.portfolio.port import Portfolio, Position

class StressTestEngine:
    """Moteur de Stress Testing sur scénarios de crise."""
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def run_scenario(self, spot_shock_pct: float, vol_shock_pct: float) -> Dict[str, float]:
        """
        Applique un choc simultané sur le Spot (ex: -0.20 pour -20%) et sur la Volatilité (ex: +0.30 pour +30%).
        """
        initial_value = self.portfolio.total_value()
        stressed_portfolio = Portfolio()

        for pos in self.portfolio.positions:
            new_S = pos.S * (1 + spot_shock_pct)
            new_sigma = pos.sigma * (1 + vol_shock_pct) if pos.sigma else None
            
            stressed_pos = Position(
                asset_type=pos.asset_type,
                quantity=pos.quantity,
                S=new_S,
                K=pos.K,
                T=pos.T,
                r=pos.r,
                sigma=new_sigma,
                option_type=pos.option_type
            )
            stressed_portfolio.add_position(stressed_pos)

        stressed_value = stressed_portfolio.total_value()
        pnl = stressed_value - initial_value

        return {
            "initial_value": initial_value,
            "stressed_value": stressed_value,
            "pnl_impact": pnl,
            "pnl_percentage": (pnl / initial_value) * 100
        }