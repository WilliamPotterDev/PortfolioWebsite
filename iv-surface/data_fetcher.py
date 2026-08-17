"""
Fetch equity options chain data via yfinance.

Pulls every available expiry for a ticker, joins calls/puts into one frame,
and attaches spot price plus a risk-free rate proxy (3-month Treasury yield).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd
import numpy as np
import yfinance as yf

# Fallback if ^IRX is unavailable (approx. recent 3M T-bill level).
DEFAULT_RISK_FREE_RATE = 0.05


def get_risk_free_rate() -> float:
    """
    Proxy for the continuous risk-free rate using the 13-week T-bill (^IRX).

    yfinance reports ^IRX as an annualized percentage yield (e.g. 5.2 means 5.2%).
    """
    try:
        tbil = yf.Ticker("^IRX")
        hist = tbil.history(period="5d")
        if hist.empty:
            return DEFAULT_RISK_FREE_RATE
        # Last close is in percent; convert to decimal.
        rate = float(hist["Close"].iloc[-1]) / 100.0
        if rate <= 0 or rate > 0.25:
            return DEFAULT_RISK_FREE_RATE
        return rate
    except Exception:
        return DEFAULT_RISK_FREE_RATE


def get_spot_price(ticker: yf.Ticker) -> float:
    """Best-effort last/mark price for the underlying."""
    info: dict[str, Any] = {}
    try:
        info = ticker.info or {}
    except Exception:
        info = {}

    for key in ("regularMarketPrice", "currentPrice", "previousClose"):
        value = info.get(key)
        if value is not None and float(value) > 0:
            return float(value)

    hist = ticker.history(period="5d")
    if hist.empty:
        raise ValueError("Could not determine spot price for ticker.")
    return float(hist["Close"].iloc[-1])


def _normalize_chain(df: pd.DataFrame, option_type: str, expiry: str) -> pd.DataFrame:
    """Standardize a single calls/puts frame and tag expiry metadata."""
    if df is None or df.empty:
        return pd.DataFrame()

    out = df.copy()
    out["option_type"] = option_type
    out["expiry"] = expiry

    expiry_dt = datetime.strptime(expiry, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days_to_expiry = max((expiry_dt - now).total_seconds() / 86400.0, 1 / 24.0)
    out["days_to_expiry"] = days_to_expiry
    out["time_to_expiry"] = days_to_expiry / 365.0  # years for BS math

    # Mid price is more stable for IV inversion than last trade alone.
    bid = pd.to_numeric(out.get("bid"), errors="coerce").fillna(0.0)
    ask = pd.to_numeric(out.get("ask"), errors="coerce").fillna(0.0)
    last = pd.to_numeric(out.get("lastPrice"), errors="coerce").fillna(0.0)
    mid = (bid + ask) / 2.0
    # Prefer mid when both sides exist; otherwise fall back to last.
    use_mid = (bid > 0) & (ask > 0)
    out["mid"] = mid.where(use_mid, last)
    out["bid"] = bid
    out["ask"] = ask
    out["lastPrice"] = last
    out["volume"] = pd.to_numeric(out.get("volume"), errors="coerce").fillna(0).astype(int)
    out["openInterest"] = pd.to_numeric(out.get("openInterest"), errors="coerce").fillna(0).astype(int)
    out["strike"] = pd.to_numeric(out.get("strike"), errors="coerce")
    if "impliedVolatility" in out.columns:
        out["impliedVolatility"] = pd.to_numeric(out["impliedVolatility"], errors="coerce")
    else:
        out["impliedVolatility"] = np.nan

    keep = [
        "contractSymbol",
        "option_type",
        "expiry",
        "strike",
        "bid",
        "ask",
        "lastPrice",
        "mid",
        "volume",
        "openInterest",
        "days_to_expiry",
        "time_to_expiry",
        "impliedVolatility",  # yfinance's own IV — kept for optional comparison only
    ]
    existing = [c for c in keep if c in out.columns]
    return out[existing].dropna(subset=["strike"])


def fetch_options_chain(ticker_symbol: str) -> dict[str, Any]:
    """
    Pull the full options chain across all listed expiries.

    Returns
    -------
    dict with keys:
        ticker, spot, risk_free_rate, chain (DataFrame), expiries (list[str])
    """
    symbol = ticker_symbol.strip().upper()
    if not symbol:
        raise ValueError("Ticker symbol is required.")

    ticker = yf.Ticker(symbol)
    expiries = list(ticker.options or [])
    if not expiries:
        raise ValueError(f"No options expiries found for {symbol}.")

    spot = get_spot_price(ticker)
    r = get_risk_free_rate()

    frames: list[pd.DataFrame] = []
    for expiry in expiries:
        try:
            chain = ticker.option_chain(expiry)
        except Exception:
            continue
        calls = _normalize_chain(chain.calls, "call", expiry)
        puts = _normalize_chain(chain.puts, "put", expiry)
        if not calls.empty:
            frames.append(calls)
        if not puts.empty:
            frames.append(puts)

    if not frames:
        raise ValueError(f"Failed to download any option contracts for {symbol}.")

    full_chain = pd.concat(frames, ignore_index=True)
    full_chain["spot"] = spot
    full_chain["risk_free_rate"] = r
    full_chain["ticker"] = symbol

    return {
        "ticker": symbol,
        "spot": spot,
        "risk_free_rate": r,
        "expiries": expiries,
        "chain": full_chain,
    }


def main() -> None:
    """Stage-1 smoke test: print a raw options chain sample."""
    symbol = "SPY"
    print(f"Fetching options chain for {symbol}...")
    data = fetch_options_chain(symbol)
    chain: pd.DataFrame = data["chain"]

    print(f"Ticker:          {data['ticker']}")
    print(f"Spot:            {data['spot']:.2f}")
    print(f"Risk-free rate:  {data['risk_free_rate']:.4%}")
    print(f"Expiries:        {len(data['expiries'])}")
    print(f"Contracts:       {len(chain)}")
    print(f"Calls / Puts:    {(chain['option_type'] == 'call').sum()} / {(chain['option_type'] == 'put').sum()}")
    print("\nSample rows:")
    cols = [
        "option_type",
        "expiry",
        "strike",
        "bid",
        "ask",
        "mid",
        "volume",
        "days_to_expiry",
        "time_to_expiry",
    ]
    print(chain[cols].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
