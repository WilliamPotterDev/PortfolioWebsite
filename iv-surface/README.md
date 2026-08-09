# Implied Volatility Surface Desk

Interactive **strike × time-to-expiry × implied volatility** surface built from live options chains. The stack is intentional desk tooling, not a toy chart: real market marks → Black-Scholes inversion you can explain → Plotly surface you can rotate/hover → a classic smile slice and a skew read driven by the actual shape of the data.

## What is an implied vol surface?

An option’s **implied volatility (IV)** is the volatility you must plug into Black-Scholes so the model price equals the market price. It is *not* a forecast pulled from a crystal ball; it is the market’s price of uncertainty, expressed in vol units.

If you solve IV for many strikes and expiries and plot:

| Axis | Meaning |
|------|---------|
| X | Strike |
| Y | Days to expiry |
| Z / color | Implied vol (%) |

…you get the **volatility surface**. Equity index surfaces are rarely flat. They usually show:

- a **smile / smirk** across strikes (wings richer than ATM), and
- a **term structure** across expiries (front-month vs longer-dated vol).

Those shapes are where the economics live.

## Why skew / smile shape matters

Black-Scholes assumes a single constant σ. Markets do not. After 1987, equity indices developed a persistent **put skew**: downside strikes carry higher IV than upside strikes. Intuition:

- **Steeper put skew** (OTM puts richer than OTM calls) → dealers/investors are paying up for crash protection; the market embeds more left-tail risk.
- **Call skew / reverse skew** → upside is being bid (squeeze, melt-up, event chase).
- **Symmetric smile** → wings are rich on both sides (jump risk / demand for convexity) without a strong directional crash premium.
- **Term structure** → backwardation (near-term ATM > long-dated) often flags an imminent event; mild contango is the calmer default.

The app’s text panel recomputes this from the filtered surface (OTM put wing vs OTM call wing vs ATM, plus a short term-structure note). It is a desk-style sanity check, not a trading signal.

## Project layout

```
iv-surface/
├── data_fetcher.py      # yfinance chain + spot + 3M Treasury proxy (^IRX)
├── black_scholes.py     # BS price + brentq IV inversion (no QuantLib)
├── surface_builder.py   # liquidity filters, IV grid, smile + skew analytics
├── app.py               # Streamlit UI + Plotly 3D / 2D charts
├── requirements.txt
└── README.md
```

## Setup

Requires **Python 3.11+**.

```bash
cd iv-surface
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Staged validation (recommended)

Build confidence in the stack the same way the code was written:

```bash
# 1) Raw options chain
python data_fetcher.py

# 2) Round-trip BS → price → IV (known σ cases)
python black_scholes.py

# 3) Filtered IV grid + skew text
python surface_builder.py
```

## Run the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).

**Demo tip:** `SPY` or `AAPL` have deep, liquid chains and produce a clean surface. Thin single-name names may fail the liquidity filters — widen the moneyness / spread sliders in the sidebar if needed.

## Implementation notes

- IV is solved with **`scipy.optimize.brentq`** on \(BS(σ) − market\). Failures (no bracket, below intrinsic, etc.) skip that strike instead of crashing.
- **\(T\)** is in **years** inside Black-Scholes; the UI shows **days**.
- Illiquid contracts (wide spreads, no volume/OI, deep ITM/OTM) are filtered — they are the usual source of surface spikes.
- Risk-free rate is a **3-month T-bill proxy** (`^IRX`), with a fixed fallback if Yahoo is unavailable.
- No QuantLib / pre-built IV solvers — the formula and inversion live in `black_scholes.py` so you can walk through them in an interview.

## Disclaimer

For education and visualization. Quotes from Yahoo via yfinance can be delayed or incomplete; this is not production risk-system quality and not investment advice.
