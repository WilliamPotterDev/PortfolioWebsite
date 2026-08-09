"""
Black-Scholes pricing and implied volatility inversion.

IV is solved by root-finding on price(σ) − market_price = 0 using
scipy.optimize.brentq (bracketed, more stable than Newton for this problem).
"""

from __future__ import annotations

import math
from typing import Literal

from scipy.optimize import brentq
from scipy.stats import norm

OptionType = Literal["call", "put"]

# Practical IV search bracket (annualized vol).
_IV_LOW = 1e-4
_IV_HIGH = 5.0


def _d1_d2(S: float, K: float, T: float, r: float, sigma: float) -> tuple[float, float]:
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        raise ValueError("S, K, T, sigma must all be positive.")
    sqrt_t = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt_t)
    d2 = d1 - sigma * sqrt_t
    return d1, d2


def black_scholes_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: OptionType = "call",
) -> float:
    """
    European Black-Scholes price (no dividends).

    Parameters
    ----------
    S : spot
    K : strike
    T : time to expiry in years
    r : continuous risk-free rate
    sigma : annualized volatility
    option_type : 'call' or 'put'
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    if option_type == "put":
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")


def implied_volatility(
    market_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    option_type: OptionType = "call",
) -> float | None:
    """
    Invert Black-Scholes for implied volatility via brentq.

    Returns None when the market price is outside the no-arbitrage bounds
    or when the root finder fails to converge.
    """
    if market_price is None or not math.isfinite(market_price) or market_price <= 0:
        return None
    if S <= 0 or K <= 0 or T <= 0:
        return None

    # Intrinsic (discounted) lower bounds for European options.
    discounted_k = K * math.exp(-r * T)
    if option_type == "call":
        lower = max(S - discounted_k, 0.0)
        upper = S
    else:
        lower = max(discounted_k - S, 0.0)
        upper = discounted_k

    # Prices at/below intrinsic or above the trivial upper bound have no IV.
    if market_price < lower - 1e-8 or market_price > upper + 1e-6:
        return None

    def objective(sigma: float) -> float:
        return black_scholes_price(S, K, T, r, sigma, option_type) - market_price

    try:
        f_low = objective(_IV_LOW)
        f_high = objective(_IV_HIGH)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None

    # Need a sign change for brentq.
    if f_low * f_high > 0:
        return None

    try:
        iv = brentq(objective, _IV_LOW, _IV_HIGH, xtol=1e-8, rtol=1e-8, maxiter=200)
    except (ValueError, RuntimeError):
        return None

    if not math.isfinite(iv) or iv <= 0:
        return None
    return float(iv)


def main() -> None:
    """
    Stage-2 validation: price a few known contracts, invert for IV,
    and check that recovered σ matches the input within tolerance.
    """
    cases = [
        # S, K, T, r, sigma, type, label
        (100.0, 100.0, 1.0, 0.05, 0.20, "call", "ATM 1Y call @ 20% vol"),
        (100.0, 100.0, 1.0, 0.05, 0.20, "put", "ATM 1Y put @ 20% vol"),
        (100.0, 110.0, 0.5, 0.03, 0.35, "call", "OTM 6M call @ 35% vol"),
        (450.0, 440.0, 30 / 365, 0.05, 0.18, "put", "Near-dated put @ 18% vol"),
    ]

    print("Black-Scholes round-trip IV validation\n" + "-" * 56)
    for S, K, T, r, sigma, opt, label in cases:
        price = black_scholes_price(S, K, T, r, sigma, opt)  # type: ignore[arg-type]
        recovered = implied_volatility(price, S, K, T, r, opt)  # type: ignore[arg-type]
        err = abs((recovered or float("nan")) - sigma)
        status = "OK" if recovered is not None and err < 1e-6 else "FAIL"
        print(
            f"[{status}] {label}\n"
            f"       price={price:.6f}  true_iv={sigma:.6f}  "
            f"recovered_iv={recovered}  abs_err={err:.2e}\n"
        )

    # Intentionally unsolvable: price below intrinsic.
    bad = implied_volatility(0.01, 100.0, 90.0, 1.0, 0.05, "call")
    print(f"[OK] deep ITM call priced below intrinsic -> IV={bad} (expected None)")


if __name__ == "__main__":
    main()
