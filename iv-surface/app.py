"""
Streamlit front-end: interactive 3D implied volatility surface + smile slice.
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from data_fetcher import fetch_options_chain
from surface_builder import build_iv_surface, smile_for_expiry

st.set_page_config(
    page_title="IV Surface Desk",
    page_icon="IV",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.35rem; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(14, 18, 26, 0.92);
        border: 1px solid rgba(90, 110, 130, 0.45) !important;
        border-radius: 10px;
        padding: 0.6rem 0.75rem 0.35rem 0.75rem;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.28);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def _load_chain(ticker: str) -> dict:
    return fetch_options_chain(ticker)


def _turbo_colorscale_for_range(z: np.ndarray) -> tuple[list, float, float]:
    """
    Keep the full IV% colorbar range, but pack Turbo's color span into the
    bulk of the data (2nd–98th percentile) so the surface looks like it did
    before the scale was widened.
    """
    zmin = float(np.nanmin(z))
    zmax = float(np.nanmax(z))
    if not np.isfinite(zmin) or not np.isfinite(zmax) or zmax <= zmin:
        return "Turbo", zmin, zmax

    lo = float(np.nanpercentile(z, 2))
    hi = float(np.nanpercentile(z, 98))
    lo = max(lo, zmin)
    hi = min(hi, zmax)
    if hi <= lo:
        return "Turbo", zmin, zmax

    span = zmax - zmin
    t_lo = (lo - zmin) / span
    t_hi = (hi - zmin) / span

    # Sample Turbo across the bulk band; clamp outside to end colors.
    turbo = [
        [0.0, "#30123b"],
        [0.1, "#4662d7"],
        [0.2, "#36aae5"],
        [0.3, "#1ae4b6"],
        [0.4, "#72fe5e"],
        [0.5, "#c8ef34"],
        [0.6, "#faba39"],
        [0.7, "#f66b19"],
        [0.8, "#ca2a04"],
        [0.9, "#7a0403"],
        [1.0, "#7a0403"],
    ]
    scale: list[list] = [[0.0, turbo[0][1]]]
    for t, color in turbo:
        scale.append([t_lo + t * (t_hi - t_lo), color])
    scale.append([1.0, turbo[-1][1]])
    # Plotly requires strictly increasing positions.
    cleaned: list[list] = []
    for pos, color in scale:
        pos = float(min(max(pos, 0.0), 1.0))
        if cleaned and pos <= cleaned[-1][0]:
            pos = min(cleaned[-1][0] + 1e-6, 1.0)
        cleaned.append([pos, color])
    return cleaned, zmin, zmax


def _surface_figure(grid: dict, option_type: str, ticker: str) -> go.Figure:
    z = np.asarray(grid["iv_mesh"], dtype=float)
    colorscale, zmin, zmax = _turbo_colorscale_for_range(z)

    fig = go.Figure(
        data=[
            go.Surface(
                x=grid["strike_mesh"],
                y=grid["day_mesh"],
                z=z,
                colorscale=colorscale,
                cmin=zmin,
                cmax=zmax,
                # Matte finish — no specular / metal look.
                lighting=dict(
                    ambient=0.92,
                    diffuse=0.35,
                    specular=0.0,
                    roughness=1.0,
                    fresnel=0.0,
                ),
                lightposition=dict(x=100, y=100, z=2000),
                colorbar=dict(title=dict(text="IV %", side="right"), len=0.72),
                hovertemplate=(
                    "Strike: %{x:.2f}<br>"
                    "Days to expiry: %{y:.1f}<br>"
                    "Implied vol: %{z:.2f}%<extra></extra>"
                ),
                contours={
                    "x": {"show": True, "color": "rgba(255,255,255,0.10)", "width": 1},
                    "y": {"show": True, "color": "rgba(255,255,255,0.10)", "width": 1},
                    "z": {
                        "show": True,
                        "usecolormap": True,
                        "highlightcolor": "#ffffff",
                        "project": {"z": False},
                        "width": 2,
                    },
                },
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text=f"{ticker} {option_type.upper()} Surface",
            x=0.02,
            xanchor="left",
        ),
        scene=dict(
            xaxis_title="Strike Price",
            yaxis_title="Days to Expiry",
            zaxis_title="Implied Volatility %",
            aspectmode="manual",
            aspectratio=dict(x=1.3, y=1.1, z=0.7),
            camera=dict(eye=dict(x=1.55, y=1.55, z=0.85)),
            xaxis=dict(backgroundcolor="rgb(18,22,28)", gridcolor="rgb(50,58,70)"),
            yaxis=dict(backgroundcolor="rgb(18,22,28)", gridcolor="rgb(50,58,70)"),
            zaxis=dict(backgroundcolor="rgb(18,22,28)", gridcolor="rgb(50,58,70)"),
            bgcolor="rgb(14,18,26)",
        ),
        margin=dict(l=0, r=0, t=48, b=0),
        height=680,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8eef7"),
    )
    return fig


def _smile_figure(smile, expiry: str, spot: float, option_type: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=smile["strike"],
            y=smile["iv_pct"],
            mode="lines+markers",
            name="IV",
            line=dict(color="#3dd6c6", width=2.5),
            marker=dict(size=7, color="#f0b429"),
            hovertemplate="Strike %{x:.2f}<br>IV %{y:.2f}%<extra></extra>",
        )
    )
    fig.add_vline(
        x=spot,
        line_width=1.5,
        line_dash="dash",
        line_color="#9aa7b8",
        annotation_text=f"Spot {spot:.2f}",
        annotation_position="top",
    )
    fig.update_layout(
        title=f"{option_type.upper()} vol smile — expiry {expiry}",
        xaxis_title="Strike Price",
        yaxis_title="Implied Volatility %",
        height=380,
        margin=dict(l=40, r=20, t=48, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,16,22,0.85)",
        font=dict(color="#e8eef7"),
        xaxis=dict(gridcolor="rgba(80,90,105,0.35)"),
        yaxis=dict(gridcolor="rgba(80,90,105,0.35)"),
    )
    return fig


def main() -> None:
    st.title("Implied Volatility Surface")

    with st.sidebar:
        st.header("Controls")
        ticker = st.text_input("Ticker", value="SPY").strip().upper()
        option_type = st.radio("Option type", options=["call", "put"], horizontal=True)
        st.markdown("---")
        st.subheader("Liquidity filters")
        min_volume = st.number_input("Min volume (or OI)", min_value=0, value=1, step=1)
        max_spread = st.slider("Max bid-ask / mid", 0.05, 0.80, 0.35, 0.05)
        moneyness = st.slider("Moneyness band", 0.50, 1.50, (0.70, 1.30), 0.05)
        run = st.button("Build surface", type="primary", use_container_width=True)

    if not ticker:
        st.warning("Enter a ticker symbol.")
        return

    # Auto-run on first load; button refreshes after filter tweaks.
    if "bootstrapped" not in st.session_state:
        st.session_state.bootstrapped = True
        run = True

    if not run and "surface_payload" not in st.session_state:
        st.info("Set a ticker and click **Build surface**.")
        return

    if run:
        with st.spinner(f"Pulling {ticker} options chain and solving IVs..."):
            try:
                raw = _load_chain(ticker)
                surface = build_iv_surface(
                    raw["chain"],
                    option_type=option_type,  # type: ignore[arg-type]
                    min_volume=int(min_volume),
                    min_open_interest=int(min_volume),
                    max_spread_pct=float(max_spread),
                    min_moneyness=float(moneyness[0]),
                    max_moneyness=float(moneyness[1]),
                )
                st.session_state.surface_payload = {
                    "raw": raw,
                    "surface": surface,
                    "ticker": ticker,
                    "option_type": option_type,
                }
            except Exception as exc:
                st.error(f"Failed to build surface: {exc}")
                return

    payload = st.session_state.surface_payload
    # Rebuild if user toggled call/put without re-fetching the chain.
    if payload["option_type"] != option_type or payload["ticker"] != ticker:
        with st.spinner("Recomputing surface for new settings..."):
            try:
                if payload["ticker"] != ticker:
                    raw = _load_chain(ticker)
                else:
                    raw = payload["raw"]
                surface = build_iv_surface(
                    raw["chain"],
                    option_type=option_type,  # type: ignore[arg-type]
                    min_volume=int(min_volume),
                    min_open_interest=int(min_volume),
                    max_spread_pct=float(max_spread),
                    min_moneyness=float(moneyness[0]),
                    max_moneyness=float(moneyness[1]),
                )
                st.session_state.surface_payload = {
                    "raw": raw,
                    "surface": surface,
                    "ticker": ticker,
                    "option_type": option_type,
                }
                payload = st.session_state.surface_payload
            except Exception as exc:
                st.error(f"Failed to rebuild surface: {exc}")
                return

    raw = payload["raw"]
    surface = payload["surface"]
    iv_df = surface["iv_df"]
    skew = surface["skew"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Spot", f"{raw['spot']:.2f}")
    c2.metric("Risk-free (3M)", f"{raw['risk_free_rate']:.2%}")
    c3.metric("IV points", f"{len(iv_df):,}")
    atm = skew.get("atm_iv")
    c4.metric("ATM IV (near expiry)", f"{atm:.1f}%" if atm is not None else "n/a")

    with st.container(border=True):
        st.plotly_chart(
            _surface_figure(surface["grid"], option_type, ticker),
            use_container_width=True,
        )

    st.subheader("Volatility smile (single expiry)")
    expiries = surface["expiries"]
    default_idx = 0
    if skew.get("expiry_used") in expiries:
        default_idx = expiries.index(skew["expiry_used"])
    expiry = st.selectbox("Expiry", options=expiries, index=default_idx)
    smile = smile_for_expiry(iv_df, expiry)
    if smile.empty:
        st.warning("No smile points for that expiry after filters.")
    else:
        st.plotly_chart(
            _smile_figure(smile, expiry, surface["spot"], option_type),
            use_container_width=True,
        )

    st.subheader("Market sentiment from skew / smile")
    st.write(skew["summary"])

    with st.expander("Methodology"):
        st.markdown(
            """
            - **Market price** for inversion: bid-ask mid when both sides are live, else last.
            - **IV solver**: Black-Scholes (no dividend) inverted with `scipy.optimize.brentq`.
            - **Time**: T in years for pricing math; plot axes show **days** to expiry.
            - **Filters**: volume/OI, bid-ask width, moneyness band — illiquid deep ITM/OTM
              marks are dropped because they produce unstable or impossible IVs.
            - **Surface**: scattered IV points linearly interpolated onto a regular mesh.
            """
        )


if __name__ == "__main__":
    main()
