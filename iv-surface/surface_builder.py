"""
Build a clean strike × expiry implied-vol grid from a raw options chain.

Filters illiquid / deep ITM-OTM junk that produces garbage IVs, then
structures the remaining points for Plotly surface / smile charts.
"""

from __future__ import annotations

import math
from typing import Any, Literal

import numpy as np
import pandas as pd
from scipy.interpolate import griddata

from black_scholes import implied_volatility

OptionType = Literal["call", "put"]


def _moneyness(strike: float, spot: float) -> float:
    return strike / spot if spot > 0 else np.nan


def _yahoo_iv(value: Any) -> float | None:
    try:
        yiv = float(value)
    except (TypeError, ValueError):
        return None
    # yfinance is usually a decimal; occasionally a percent.
    if yiv > 3.0:  # e.g. 25.0 meaning 25%
        yiv /= 100.0
    if 0.03 <= yiv <= 1.50:
        return yiv
    return None


def filter_liquid_contracts(
    chain: pd.DataFrame,
    option_type: OptionType,
    *,
    min_volume: int = 0,
    min_open_interest: int = 0,
    max_spread_pct: float = 0.50,
    min_moneyness: float = 0.70,
    max_moneyness: float = 1.30,
    min_mid: float = 0.05,
    min_days: float = 5.0,
    max_days: float = 180.0,
    require_live_quote: bool = False,
    allow_yahoo_iv_only: bool = True,
) -> pd.DataFrame:
    """
    Keep near-money contracts that either have a usable mark or a Yahoo IV.

    Defaults are cloud-friendly: Yahoo often returns empty bid/ask on Streamlit Cloud.
    """
    df = chain.loc[chain["option_type"] == option_type].copy()
    if df.empty:
        return df

    spot = float(df["spot"].iloc[0])
    df["moneyness"] = df["strike"] / spot
    df["spread"] = df["ask"] - df["bid"]
    df["spread_pct"] = np.where(df["mid"] > 0, df["spread"] / df["mid"], np.inf)
    has_live_quote = (df["bid"] > 0) & (df["ask"] > df["bid"])
    if "impliedVolatility" in df.columns:
        yiv = df["impliedVolatility"].map(_yahoo_iv)
        df["_yiv"] = yiv
        has_yiv = yiv.notna()
    else:
        df["_yiv"] = np.nan
        has_yiv = pd.Series(False, index=df.index)

    has_mark = df["mid"] >= min_mid

    liquid = (
        (df["moneyness"] >= min_moneyness)
        & (df["moneyness"] <= max_moneyness)
        & (df["days_to_expiry"] >= min_days)
        & (df["days_to_expiry"] <= max_days)
        & (has_mark | (allow_yahoo_iv_only & has_yiv))
    )

    if min_volume > 0 or min_open_interest > 0:
        liquid &= (df["volume"] >= min_volume) | (df["openInterest"] >= min_open_interest)

    if require_live_quote:
        liquid &= has_live_quote & (df["spread_pct"] <= max_spread_pct)
    else:
        # If a live quote exists, enforce spread; marks/Yahoo-only rows stay.
        liquid &= (~has_live_quote) | (df["spread_pct"] <= max_spread_pct)

    return df.loc[liquid].reset_index(drop=True)


def compute_implied_vols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Invert BS when the mark has meaningful time value; otherwise use Yahoo IV.

    Deep ITM options priced near intrinsic produce nonsense IVs and wreck the smile.
    """
    if df.empty:
        return df.assign(iv=pd.Series(dtype=float), iv_pct=pd.Series(dtype=float))

    ivs: list[float | None] = []
    for row in df.itertuples(index=False):
        S = float(row.spot)
        K = float(row.strike)
        T = float(row.time_to_expiry)
        r = float(row.risk_free_rate)
        mid = float(row.mid)
        opt = row.option_type
        yiv = _yahoo_iv(getattr(row, "impliedVolatility", None))

        iv: float | None = None
        discounted_k = K * math.exp(-r * T)
        if opt == "call":
            intrinsic = max(S - discounted_k, 0.0)
        else:
            intrinsic = max(discounted_k - S, 0.0)

        # Only invert when there is clear time value above intrinsic.
        time_value = mid - intrinsic
        if mid > 0 and time_value > max(0.05, 0.02 * mid):
            iv = implied_volatility(mid, S, K, T, r, opt)  # type: ignore[arg-type]

        if iv is None:
            iv = yiv

        # Reject deep-ITM inversions that still look like junk vs Yahoo.
        if iv is not None and yiv is not None and abs(iv - yiv) > 0.50:
            # Prefer Yahoo when our solve disagrees wildly (stale ITM marks).
            m = K / S
            deep = (opt == "call" and m < 0.92) or (opt == "put" and m > 1.08)
            if deep:
                iv = yiv

        ivs.append(iv)

    out = df.copy()
    out["iv"] = ivs
    out = out.dropna(subset=["iv"])
    out = out.loc[(out["iv"] >= 0.04) & (out["iv"] <= 1.20)].reset_index(drop=True)
    out["iv_pct"] = out["iv"] * 100.0
    return out


def best_smile_expiry(iv_df: pd.DataFrame, spot: float) -> str:
    """Pick the expiry with the best strike coverage around spot (true smile)."""
    best_exp = str(iv_df["expiry"].iloc[0])
    best_score = -1e18
    for expiry, frame in iv_df.groupby("expiry"):
        if len(frame) < 4:
            continue
        m = frame["strike"] / spot
        n = len(frame)
        span = float(m.max() - m.min()) if n else 0.0
        atm_dist = float((m - 1.0).abs().min())
        has_left = bool((m < 0.98).any())
        has_right = bool((m > 1.02).any())
        wing_bonus = 5.0 * (int(has_left) + int(has_right))
        # Prefer ~2w–3m tenors with wings around ATM.
        days = float(frame["days_to_expiry"].iloc[0])
        tenor_score = -abs(days - 45.0) / 45.0
        score = wing_bonus + span * 10.0 + n * 0.15 - atm_dist * 20.0 + tenor_score
        if score > best_score:
            best_score = score
            best_exp = str(expiry)
    return best_exp


def build_iv_surface(
    chain: pd.DataFrame,
    option_type: OptionType = "call",
    **filter_kwargs: Any,
) -> dict[str, Any]:
    """End-to-end: filter → invert IV → grid → skew diagnostics."""
    attempts = [
        {**filter_kwargs, "require_live_quote": False, "allow_yahoo_iv_only": True},
        {
            **filter_kwargs,
            "require_live_quote": False,
            "allow_yahoo_iv_only": True,
            "min_volume": 0,
            "min_open_interest": 0,
            "max_spread_pct": 0.9,
            "min_mid": 0.01,
            "min_days": 3.0,
            "max_days": 365.0,
        },
        {
            **filter_kwargs,
            "require_live_quote": False,
            "allow_yahoo_iv_only": True,
            "min_volume": 0,
            "min_open_interest": 0,
            "min_mid": 0.0,
            "min_days": 2.0,
            "max_days": 400.0,
            "min_moneyness": min(float(filter_kwargs.get("min_moneyness", 0.7)), 0.75),
            "max_moneyness": max(float(filter_kwargs.get("max_moneyness", 1.3)), 1.25),
        },
    ]

    iv_df = pd.DataFrame()
    last_liquid = 0
    for kwargs in attempts:
        liquid = filter_liquid_contracts(chain, option_type, **kwargs)
        last_liquid = len(liquid)
        iv_df = compute_implied_vols(liquid)
        # Need enough points AND some strike span to look like a surface/smile.
        if len(iv_df) >= 15:
            span = float(iv_df["strike"].max() - iv_df["strike"].min())
            spot = float(iv_df["spot"].iloc[0])
            if span / spot >= 0.08:
                break

    if iv_df.empty or len(iv_df) < 8:
        n_type = int((chain["option_type"] == option_type).sum()) if not chain.empty else 0
        raise ValueError(
            f"No valid {option_type} IVs after filtering / inversion "
            f"({n_type} raw {option_type}s, {last_liquid} after filters). "
            "Yahoo quotes are often empty on cloud hosts — click Update again or widen moneyness."
        )

    spot = float(iv_df["spot"].iloc[0])
    grid = build_surface_grid(iv_df)
    skew = analyze_skew(iv_df, spot)
    expiries = sorted(iv_df["expiry"].unique().tolist())
    smile_expiry = best_smile_expiry(iv_df, spot)

    return {
        "option_type": option_type,
        "spot": spot,
        "iv_df": iv_df,
        "grid": grid,
        "skew": skew,
        "expiries": expiries,
        "smile_expiry": smile_expiry,
    }


def build_surface_grid(
    iv_df: pd.DataFrame,
    *,
    n_strike: int = 80,
    n_expiry: int = 50,
) -> dict[str, Any]:
    """
    Interpolate scattered (strike, days, iv%) points onto a dense mesh
    suitable for go.Surface.
    """
    from scipy.ndimage import gaussian_filter

    if iv_df.empty or len(iv_df) < 8:
        raise ValueError(
            "Not enough liquid IV points to build a surface. "
            "Try another ticker or relax liquidity filters."
        )

    strikes = iv_df["strike"].to_numpy(dtype=float)
    days = iv_df["days_to_expiry"].to_numpy(dtype=float)
    iv_pct = iv_df["iv_pct"].to_numpy(dtype=float)

    # Winsorize extreme IVs so a few junk points don't dominate the mesh.
    lo, hi = np.nanpercentile(iv_pct, [5, 95])
    if hi <= lo:
        lo, hi = float(np.nanmin(iv_pct)), float(np.nanmax(iv_pct))
    iv_pct = np.clip(iv_pct, lo, hi)

    strike_grid = np.linspace(strikes.min(), strikes.max(), n_strike)
    day_grid = np.linspace(days.min(), days.max(), n_expiry)
    strike_mesh, day_mesh = np.meshgrid(strike_grid, day_grid)
    pts = np.column_stack([strikes, days])

    iv_mesh = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="linear")
    if iv_mesh is None or np.isnan(iv_mesh).all():
        iv_mesh = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="nearest")

    nearest = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="nearest")
    iv_mesh = np.where(np.isnan(iv_mesh), nearest, iv_mesh)
    iv_mesh = gaussian_filter(iv_mesh.astype(float), sigma=1.0, mode="nearest")
    iv_mesh = np.clip(iv_mesh, lo, hi)

    return {
        "strike_mesh": strike_mesh,
        "day_mesh": day_mesh,
        "iv_mesh": iv_mesh,
        "points": iv_df,
    }


def smile_for_expiry(iv_df: pd.DataFrame, expiry: str) -> pd.DataFrame:
    """IV vs strike slice for one expiry (classic vol smile)."""
    smile = (
        iv_df.loc[iv_df["expiry"] == expiry, ["strike", "iv", "iv_pct", "moneyness", "mid", "volume"]]
        .sort_values("strike")
        .reset_index(drop=True)
    )
    return smile


def analyze_skew(iv_df: pd.DataFrame, spot: float) -> dict[str, Any]:
    """
    Derive a short desk-style read of skew / smile from the data.

    Compares downside-strike IV (moneyness ~0.85-0.95) vs upside-strike IV
    (~1.05-1.15) on a single expiry that has both wings populated. Works on
    call-only or put-only surfaces because those wings are strike regions,
    not option type.
    """
    if iv_df.empty:
        return {
            "summary": "Insufficient data to assess skew.",
            "put_wing_iv": None,
            "call_wing_iv": None,
            "atm_iv": None,
            "skew_pp": None,
        }

    def _wing_stats(frame: pd.DataFrame) -> tuple[float | None, float | None, float]:
        m = frame["strike"] / spot
        atm = frame.iloc[(m - 1.0).abs().argsort()[:3]]
        atm_iv = float(atm["iv_pct"].mean())
        down = frame.loc[(m >= 0.85) & (m <= 0.95), "iv_pct"]
        up = frame.loc[(m >= 1.05) & (m <= 1.15), "iv_pct"]
        down_iv = float(down.mean()) if len(down) else None
        up_iv = float(up.mean()) if len(up) else None
        return down_iv, up_iv, atm_iv

    # Prefer an expiry with both wings and enough points; favor ~1w-2m tenor.
    candidates: list[tuple[int, float, str]] = []
    for expiry, frame in iv_df.groupby("expiry"):
        if len(frame) < 6:
            continue
        down_iv, up_iv, _ = _wing_stats(frame)
        both = int(down_iv is not None) + int(up_iv is not None)
        days = float(frame["days_to_expiry"].iloc[0])
        # Score: both wings first, then closeness to ~21 days.
        score = both * 10 - abs(days - 21.0) / 21.0
        candidates.append((both, score, str(expiry)))

    if not candidates:
        expiry = str(iv_df.groupby("expiry").size().idxmax())
    else:
        candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
        expiry = candidates[0][2]

    slice_df = iv_df.loc[iv_df["expiry"] == expiry].copy()
    put_iv, call_iv, atm_iv = _wing_stats(slice_df)

    if put_iv is not None and call_iv is not None:
        skew_pp = put_iv - call_iv
        if skew_pp > 3:
            shape = (
                f"Classic equity put skew on {expiry}: downside strikes "
                f"(~{put_iv:.1f}% IV) are priced richer than upside strikes "
                f"(~{call_iv:.1f}% IV) by {skew_pp:.1f} vol points. The market is "
                f"charging more for left-tail / crash protection than for upside "
                f"gap risk - the usual index-equity smirk."
            )
        elif skew_pp < -3:
            shape = (
                f"Reverse / call skew on {expiry}: upside strikes (~{call_iv:.1f}% IV) "
                f"sit above downside strikes (~{put_iv:.1f}% IV) by {abs(skew_pp):.1f} "
                f"vol points. That pattern usually appears when the market is bidding "
                f"upside (squeeze / event chase) harder than downside hedges."
            )
        else:
            shape = (
                f"Nearly symmetric smile on {expiry}: downside IV (~{put_iv:.1f}%) and "
                f"upside IV (~{call_iv:.1f}%) are close (delta={skew_pp:.1f} pp). "
                f"ATM sits near {atm_iv:.1f}% - little evidence of a strong directional "
                f"crash premium in this slice."
            )
    elif put_iv is not None:
        skew_pp = put_iv - atm_iv
        shape = (
            f"Downside wing (~{put_iv:.1f}% IV) vs ATM (~{atm_iv:.1f}% IV) on {expiry}: "
            f"{'elevated downside premium' if skew_pp > 0 else 'muted downside wing'}. "
            f"Upside-wing coverage was too thin for a full skew comparison."
        )
    elif call_iv is not None:
        skew_pp = call_iv - atm_iv
        shape = (
            f"Upside wing (~{call_iv:.1f}% IV) vs ATM (~{atm_iv:.1f}% IV) on {expiry}: "
            f"{'rich upside premium' if skew_pp > 0 else 'soft upside wing'}. "
            f"Downside-wing coverage was too thin for a full skew comparison."
        )
    else:
        skew_pp = None
        shape = (
            f"ATM implied vol near {atm_iv:.1f}% on {expiry}, but wing coverage is too "
            f"thin for a reliable skew read after liquidity filters."
        )

    # Term-structure hint from short vs longer ATM.
    term_note = ""
    by_exp = (
        iv_df.assign(m_dist=(iv_df["strike"] / spot - 1.0).abs())
        .sort_values(["expiry", "m_dist"])
        .groupby("expiry", as_index=False)
        .first()
    )
    if len(by_exp) >= 2:
        short_iv = float(by_exp.iloc[0]["iv_pct"])
        long_iv = float(by_exp.iloc[-1]["iv_pct"])
        if short_iv - long_iv > 2:
            term_note = (
                f" Near-term ATM ({short_iv:.1f}%) is above longer-dated ATM "
                f"({long_iv:.1f}%) - a backwardated term structure, often linked to "
                f"an imminent event or elevated short-horizon uncertainty."
            )
        elif long_iv - short_iv > 2:
            term_note = (
                f" The term structure is upward-sloping: longer-dated ATM "
                f"({long_iv:.1f}%) exceeds front-month ATM ({short_iv:.1f}%), "
                f"the more common 'contango' vol regime when no single event dominates."
            )

    return {
        "summary": shape + term_note,
        "expiry_used": expiry,
        "put_wing_iv": put_iv,
        "call_wing_iv": call_iv,
        "atm_iv": atm_iv,
        "skew_pp": skew_pp,
    }


def main() -> None:
    """Stage-3 smoke test: build a surface grid for SPY calls."""
    from data_fetcher import fetch_options_chain

    print("Fetching SPY chain...")
    data = fetch_options_chain("SPY")
    print(f"Raw contracts: {len(data['chain'])}")

    surface = build_iv_surface(data["chain"], option_type="call")
    iv_df = surface["iv_df"]
    grid = surface["grid"]

    print(f"Liquid IV points: {len(iv_df)}")
    print(f"Expiries used:    {surface['expiries']}")
    print(f"Grid shape:       {grid['iv_mesh'].shape} (expiry x strike)")
    print(f"IV range:         {np.nanmin(grid['iv_mesh']):.2f}% - {np.nanmax(grid['iv_mesh']):.2f}%")
    print(f"\nSkew read:\n{surface['skew']['summary']}")


if __name__ == "__main__":
    main()
