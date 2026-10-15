import pytest
from src.pricing.black_scholes import bs_price
from src.pricing.monte_carlo import mc_price

def test_call_put_parity():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    call = bs_price(S, K, T, r, sigma, "call")
    put = bs_price(S, K, T, r, sigma, "put")
    
    # Parité Call-Put: C - P = S - K * exp(-r*T)
    lhs = call - put
    rhs = S - K * np.exp(-r * T)
    assert pytest.approx(lhs, rel=1e-4) == rhs

def test_mc_convergence():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    bs = bs_price(S, K, T, r, sigma, "call")
    mc, std_err, _ = mc_price(S, K, T, r, sigma, "call", n_sims=200000, seed=42)
    
    # L'écart MC vs BS doit être inférieur à 3 fois l'erreur standard
    assert abs(mc - bs) < 3 * std_err