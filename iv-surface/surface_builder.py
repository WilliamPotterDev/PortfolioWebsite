"""
Build a clean strike × expiry implied-vol grid from a raw options chain.

Filters illiquid / deep ITM-OTM junk that produces garbage IVs, then
structures the remaining points for Plotly surface / smile charts.
"""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import pandas as pd
from scipy.interpolate import griddata

from black_scholes import implied_volatility

OptionType = Literal["call", "put"]


def _moneyness(strike: float, spot: float) -> float:
    return strike / spot if spot > 0 else np.nan


def filter_liquid_contracts(
    chain: pd.DataFrame,
    option_type: OptionType,
    *,
    min_volume: int = 1,
    min_open_interest: int = 1,
    max_spread_pct: float = 0.35,
    min_moneyness: float = 0.70,
    max_moneyness: float = 1.30,
    min_mid: float = 0.05,
    min_days: float = 2.0,
    max_days: float = 365.0,
) -> pd.DataFrame:
    """
    Drop contracts that typically break IV inversion or spike the surface.

    Rules of thumb used by desks for a quick visual surface:
    - require some volume OR open interest
    - reject wide bid-ask relative to mid
    - keep strikes near the money (avoid deep ITM/OTM with stale marks)
    - skip ultra-short dated (noise) and >1Y if sparse
    """
    df = chain.loc[chain["option_type"] == option_type].copy()
    if df.empty:
        return df

    spot = float(df["spot"].iloc[0])
    df["moneyness"] = df["strike"] / spot
    df["spread"] = df["ask"] - df["bid"]
    df["spread_pct"] = np.where(df["mid"] > 0, df["spread"] / df["mid"], np.inf)

    liquid = (
        ((df["volume"] >= min_volume) | (df["openInterest"] >= min_open_interest))
        & (df["mid"] >= min_mid)
        & (df["bid"] > 0)
        & (df["ask"] > df["bid"])
        & (df["spread_pct"] <= max_spread_pct)
        & (df["moneyness"] >= min_moneyness)
        & (df["moneyness"] <= max_moneyness)
        & (df["days_to_expiry"] >= min_days)
        & (df["days_to_expiry"] <= max_days)
    )
    return df.loc[liquid].reset_index(drop=True)


def compute_implied_vols(df: pd.DataFrame) -> pd.DataFrame:
    """Solve IV for each row; skip strikes where brentq fails."""
    if df.empty:
        return df.assign(iv=pd.Series(dtype=float))

    ivs: list[float | None] = []
    for row in df.itertuples(index=False):
        iv = implied_volatility(
            market_price=float(row.mid),
            S=float(row.spot),
            K=float(row.strike),
            T=float(row.time_to_expiry),
            r=float(row.risk_free_rate),
            option_type=row.option_type,  # type: ignore[arg-type]
        )
        ivs.append(iv)

    out = df.copy()
    out["iv"] = ivs
    out = out.dropna(subset=["iv"])
    # Sanity band: discard absurd inversions that slipped past filters.
    out = out.loc[(out["iv"] >= 0.01) & (out["iv"] <= 2.5)].reset_index(drop=True)
    out["iv_pct"] = out["iv"] * 100.0
    return out


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

    strike_grid = np.linspace(strikes.min(), strikes.max(), n_strike)
    day_grid = np.linspace(days.min(), days.max(), n_expiry)
    strike_mesh, day_mesh = np.meshgrid(strike_grid, day_grid)
    pts = np.column_stack([strikes, days])

    # Keep the full liquid IV range on the colorbar / z-axis (no percentile cap).
    iv_mesh = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="cubic")
    if iv_mesh is None or np.isnan(iv_mesh).all():
        iv_mesh = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="linear")

    linear = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="linear")
    nearest = griddata(pts, iv_pct, xi=(strike_mesh, day_mesh), method="nearest")
    iv_mesh = np.where(np.isnan(iv_mesh), linear, iv_mesh)
    iv_mesh = np.where(np.isnan(iv_mesh), nearest, iv_mesh)

    # Mild smooth for detail without faceting — matte sheet, not polished metal.
    iv_mesh = gaussian_filter(iv_mesh.astype(float), sigma=0.7, mode="nearest")

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


def build_iv_surface(
    chain: pd.DataFrame,
    option_type: OptionType = "call",
    **filter_kwargs: Any,
) -> dict[str, Any]:
    """End-to-end: filter → invert IV → grid → skew diagnostics."""
    liquid = filter_liquid_contracts(chain, option_type, **filter_kwargs)
    iv_df = compute_implied_vols(liquid)
    if iv_df.empty:
        raise ValueError(f"No valid {option_type} IVs after filtering / inversion.")

    spot = float(iv_df["spot"].iloc[0])
    grid = build_surface_grid(iv_df)
    skew = analyze_skew(iv_df, spot)
    expiries = sorted(iv_df["expiry"].unique().tolist())

    return {
        "option_type": option_type,
        "spot": spot,
        "iv_df": iv_df,
        "grid": grid,
        "skew": skew,
        "expiries": expiries,
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
