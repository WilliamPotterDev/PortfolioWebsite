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
    page_title="Implied Volatility Surface",
    page_icon="IV",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _apply_chrome() -> None:
    bg = "#ffffff"
    panel = "#ffffff"
    sidebar = "#ffffff"
    border = "#d0d0d0"
    text = "#111111"
    muted = "#555555"
    button = "#d9d9d9"
    button_hover = "#c4c4c4"
    input_bg = "#ffffff"

    st.markdown(
        f"""
        <style>
        html, body, [class*="css"], .stApp, button, input, label, p, h1, h2, h3, h4, h5, h6 {{
            font-family: Arial, Helvetica, sans-serif !important;
        }}
        .stApp {{
            background: {bg};
            color: {text};
        }}
        .block-container {{
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }}
        h1, h2, h3, h4, h5, h6, p, label, span, div {{
            color: inherit;
        }}
        h1 {{
            font-weight: 600 !important;
            letter-spacing: 0;
            font-size: 1.55rem !important;
            margin-bottom: 0.25rem !important;
            color: {text} !important;
        }}
        div[data-testid="stMetricValue"] {{
            font-size: 1.15rem;
            font-weight: 600;
            color: {text} !important;
        }}
        div[data-testid="stMetricLabel"] {{
            font-size: 0.8rem;
            color: {muted} !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {panel};
            border: 1px solid {border} !important;
            border-radius: 2px;
            padding: 0.4rem 0.5rem 0.15rem 0.5rem;
            box-shadow: none;
        }}
        section[data-testid="stSidebar"] {{
            background: {sidebar} !important;
            border-right: 1px solid {border};
        }}
        section[data-testid="stSidebar"] * {{
            color: {text};
        }}
        [data-testid="stHeader"] {{
            background: {bg} !important;
        }}
        .stSelectbox label, .stSlider label, .stRadio label,
        .stNumberInput label, .stTextInput label {{
            color: {text} !important;
        }}
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stNumberInput"] [data-testid="stNumberInputField"],
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stSelectbox"] > div > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"],
        div[data-baseweb="base-input"],
        div[data-baseweb="input"] input {{
            background-color: {input_bg} !important;
            background: {input_bg} !important;
            color: {text} !important;
            border-color: {border} !important;
            caret-color: {text} !important;
            -webkit-text-fill-color: {text} !important;
        }}
        [data-testid="stNumberInput"] button {{
            background-color: {button} !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stNumberInput"] button svg,
        [data-testid="stNumberInput"] button span,
        [data-testid="stNumberInput"] button i {{
            color: {text} !important;
            fill: {text} !important;
        }}
        [data-testid="stNumberInput"] button:hover {{
            background-color: {button_hover} !important;
            color: {text} !important;
        }}
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] ul,
        ul[role="listbox"],
        li[role="option"] {{
            background-color: {bg} !important;
            background: {bg} !important;
            color: {text} !important;
        }}
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {{
            background-color: #ececec !important;
        }}
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stNumberInput"] input::placeholder {{
            color: {muted} !important;
            -webkit-text-fill-color: {muted} !important;
        }}
        .stApp [data-testid="stTextInput"] *,
        .stApp [data-testid="stNumberInput"] input,
        .stApp [data-testid="stSelectbox"] [data-baseweb="select"] * {{
            color: {text};
        }}
        div[data-testid="stStatusWidget"] {{
            display: none !important;
        }}
        div[data-testid="stMarkdownContainer"] p {{
            color: {text};
        }}
        .stButton > button,
        .stButton > button[kind="primary"],
        button[data-testid="baseButton-primary"],
        button[kind="primary"] {{
            background-color: {button} !important;
            background-image: none !important;
            color: {text} !important;
            border: 1px solid #b5b5b5 !important;
            border-radius: 2px !important;
            font-weight: 600 !important;
            box-shadow: none !important;
        }}
        .stButton > button:hover,
        .stButton > button[kind="primary"]:hover,
        button[data-testid="baseButton-primary"]:hover,
        button[kind="primary"]:hover {{
            background-color: {button_hover} !important;
            color: {text} !important;
            border-color: #999999 !important;
        }}
        div[role="radiogroup"] label {{
            color: {text} !important;
        }}
        [data-testid="stSlider"] [data-baseweb="slider"] div {{
            background-color: #cfcfcf !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _chart_palette() -> dict:
    return {
        "font": "#111111",
        "title": "#111111",
        "muted": "#555555",
        "paper": "#ffffff",
        "plot": "#ffffff",
        "scene": "#ffffff",
        "axis_bg": "#f7f7f7",
        "grid": "#dddddd",
        "line": "#888888",
        "marker": "#ff4b4b",
        "vline": "#777777",
        "axis_line": "#999999",
    }


def _vivid_iv_colorscale(z: np.ndarray) -> tuple[list | str, float, float]:
    """
    Full IV% colorbar range, with the vivid Turbo band packed into the
    bulk of the data so the surface stays colourful.
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

    turbo = [
        [0.0, "#30123b"],
        [0.08, "#4145ab"],
        [0.16, "#4662d7"],
        [0.24, "#3e8ef4"],
        [0.32, "#2cb4e4"],
        [0.40, "#1ae4b6"],
        [0.48, "#6dff75"],
        [0.56, "#c8ef34"],
        [0.64, "#f5db19"],
        [0.72, "#fba238"],
        [0.80, "#f66b19"],
        [0.88, "#e03b0d"],
        [0.96, "#a51107"],
        [1.0, "#7a0403"],
    ]
    scale: list[list] = [[0.0, turbo[0][1]]]
    for t, color in turbo:
        scale.append([t_lo + t * (t_hi - t_lo), color])
    scale.append([1.0, turbo[-1][1]])

    cleaned: list[list] = []
    for pos, color in scale:
        pos = float(min(max(pos, 0.0), 1.0))
        if cleaned and pos <= cleaned[-1][0]:
            pos = min(cleaned[-1][0] + 1e-6, 1.0)
        cleaned.append([pos, color])
    return cleaned, zmin, zmax


@st.cache_data(ttl=300, show_spinner=False)
def _load_chain(ticker: str) -> dict:
    return fetch_options_chain(ticker)


def _surface_figure(grid: dict, option_type: str, ticker: str) -> go.Figure:
    z = np.asarray(grid["iv_mesh"], dtype=float)
    colorscale, zmin, zmax = _vivid_iv_colorscale(z)
    p = _chart_palette()
    font_family = "Arial, Helvetica, sans-serif"

    fig = go.Figure(
        data=[
            go.Surface(
                x=grid["strike_mesh"],
                y=grid["day_mesh"],
                z=z,
                colorscale=colorscale,
                cmin=zmin,
                cmax=zmax,
                lighting=dict(
                    ambient=0.95,
                    diffuse=0.25,
                    specular=0.0,
                    roughness=1.0,
                    fresnel=0.0,
                ),
                lightposition=dict(x=100, y=100, z=2000),
                colorbar=dict(
                    title=dict(text="IV %", side="right", font=dict(size=11, color=p["font"])),
                    len=0.7,
                    thickness=14,
                    tickfont=dict(size=10, color=p["muted"]),
                    outlinewidth=0,
                    bgcolor="rgba(0,0,0,0)",
                ),
                hovertemplate=(
                    "Strike %{x:.2f}<br>"
                    "Days %{y:.1f}<br>"
                    "IV %{z:.2f}%<extra></extra>"
                ),
                contours=dict(
                    z=dict(
                        show=True,
                        usecolormap=True,
                        highlightcolor="#ffffff",
                        width=1,
                        project=dict(z=False),
                    )
                ),
            )
        ]
    )

    def _axis(label: str) -> dict:
        return dict(
            title=dict(text=label, font=dict(size=12, color=p["muted"])),
            backgroundcolor=p["axis_bg"],
            gridcolor=p["grid"],
            showbackground=True,
            zeroline=False,
            tickfont=dict(size=10, color=p["muted"]),
            color=p["font"],
        )

    fig.update_layout(
        title=dict(
            text=f"{ticker} {option_type.upper()} Surface",
            x=0.0,
            xanchor="left",
            font=dict(size=14, color=p["title"], family=font_family),
        ),
        scene=dict(
            xaxis=_axis("Strike"),
            yaxis=_axis("Days to expiry"),
            zaxis=_axis("IV %"),
            aspectmode="manual",
            aspectratio=dict(x=1.25, y=1.05, z=0.65),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
            bgcolor=p["scene"],
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=640,
        paper_bgcolor=p["paper"],
        font=dict(color=p["font"], family=font_family),
    )
    return fig


def _smile_figure(smile, expiry: str, spot: float, option_type: str) -> go.Figure:
    p = _chart_palette()
    font_family = "Arial, Helvetica, sans-serif"
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=smile["strike"],
            y=smile["iv_pct"],
            mode="lines+markers",
            name="IV",
            line=dict(color=p["line"], width=2),
            marker=dict(size=5, color=p["marker"]),
            hovertemplate="Strike %{x:.2f}<br>IV %{y:.2f}%<extra></extra>",
        )
    )
    fig.add_vline(
        x=spot,
        line_width=1,
        line_dash="dot",
        line_color=p["vline"],
        annotation_text=f"spot {spot:.2f}",
        annotation_position="top",
        annotation_font=dict(size=11, color=p["muted"]),
    )
    fig.update_layout(
        title=dict(
            text=f"{option_type.upper()} smile — {expiry}",
            font=dict(size=14, color=p["title"], family=font_family),
        ),
        xaxis_title="Strike",
        yaxis_title="IV %",
        height=360,
        margin=dict(l=40, r=20, t=44, b=40),
        paper_bgcolor=p["paper"],
        plot_bgcolor=p["plot"],
        font=dict(color=p["font"], size=12, family=font_family),
        xaxis=dict(
            gridcolor=p["grid"],
            zeroline=False,
            showline=True,
            linecolor=p["axis_line"],
            color=p["font"],
        ),
        yaxis=dict(
            gridcolor=p["grid"],
            zeroline=False,
            showline=True,
            linecolor=p["axis_line"],
            color=p["font"],
        ),
    )
    return fig


def main() -> None:
    _apply_chrome()
    st.markdown(
        """
        <div style="margin: 0 0 1.1rem 0;">
          <h1 style="
            margin: 0 0 0.35rem 0;
            font-family: Arial, Helvetica, sans-serif;
            font-weight: 600;
            letter-spacing: 0;
            font-size: 1.55rem;
            color: #111111;
          ">Implied Volatility Surface</h1>
          <p style="
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 0.85rem;
            font-weight: 400;
            color: #555555;
          ">William Potter</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.subheader("Inputs")
        ticker = st.text_input("Ticker", value="SPY").strip().upper()
        option_type = st.radio("Type", options=["call", "put"], horizontal=True)
        st.subheader("Filters")
        min_volume = st.number_input("Min volume or OI", min_value=0, value=1, step=1)
        max_spread = st.slider("Max bid-ask / mid", 0.05, 0.80, 0.35, 0.05)
        moneyness = st.slider("Moneyness band", 0.50, 1.50, (0.70, 1.30), 0.05)
        run = st.button("Update", use_container_width=True)

    if not ticker:
        st.warning("Enter a ticker.")
        return

    if "bootstrapped" not in st.session_state:
        st.session_state.bootstrapped = True
        run = True

    if not run and "surface_payload" not in st.session_state:
        st.info("Choose a ticker and click Update.")
        return

    if run:
        with st.spinner(f"Loading {ticker} options..."):
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
                st.error(f"Could not build surface: {exc}")
                return

    payload = st.session_state.surface_payload
    if payload["option_type"] != option_type or payload["ticker"] != ticker:
        with st.spinner("Updating surface..."):
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
                st.error(f"Could not rebuild surface: {exc}")
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
    c4.metric("ATM IV", f"{atm:.1f}%" if atm is not None else "n/a")

    with st.container(border=True):
        st.plotly_chart(
            _surface_figure(surface["grid"], option_type, ticker),
            use_container_width=True,
        )

    st.markdown("##### Smile by expiry")
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


if __name__ == "__main__":
    main()
