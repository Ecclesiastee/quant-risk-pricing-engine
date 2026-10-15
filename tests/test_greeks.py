import pytest
from src.greeks.greeks import OptionGreeks

def test_greeks_values():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.20
    
    delta_call = OptionGreeks.delta(S, K, T, r, sigma, "call")
    delta_put = OptionGreeks.delta(S, K, T, r, sigma, "put")
    
    # Propriété : Delta(Call) - Delta(Put) = 1
    assert pytest.approx(delta_call - delta_put, rel=1e-5) == 1.0
    assert OptionGreeks.gamma(S, K, T, r, sigma) > 0
    assert OptionGreeks.vega(S, K, T, r, sigma) > 0