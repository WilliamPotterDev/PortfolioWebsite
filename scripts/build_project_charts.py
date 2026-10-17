"""Generate portfolio visuals for market-betas and loan-book projects."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_BETA = ROOT / "public" / "projects" / "market-betas"
OUT_LOAN = ROOT / "public" / "projects" / "loan-book"
CRSP = ROOT / "notebooks" / "market-betas" / "crsp2025.xlsx"


def main() -> None:
    OUT_BETA.mkdir(parents=True, exist_ok=True)
    OUT_LOAN.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(CRSP)
    tickers = ["AAPL", "NVDA", "AVGO", "MSFT", "ORCL"]
    names = ["Apple", "Nvidia", "Broadcom", "Microsoft", "Oracle"]
    betas: list[float] = []
    for ticker in tickers:
        series = df[df["Ticker"] == ticker]
        beta = (
            series["Daily Total Return"].cov(
                series["Value-weighted return including dividends"]
            )
            / series["Value-weighted return including dividends"].var()
        )
        betas.append(float(beta))

    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor="#0b0b0b")
    ax.set_facecolor("#0b0b0b")
    colors = ["#6ee7b7" if b < 1 else "#f87171" for b in betas]
    bars = ax.bar(names, betas, color=colors, width=0.62)
    ax.axhline(1.0, color="#ffffff55", linestyle="--", linewidth=1)
    ax.set_ylabel("Equity beta vs market", color="#dddddd")
    ax.set_title("Systematic Risk — Equity Betas (CRSP 2025)", color="#ffffff", pad=14)
    ax.tick_params(colors="#cccccc")
    for spine in ax.spines.values():
        spine.set_color("#333333")
    for bar, beta in zip(bars, betas):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.04,
            f"{beta:.2f}",
            ha="center",
            va="bottom",
            color="#eeeeee",
            fontsize=10,
        )
    ax.set_ylim(0, max(betas) * 1.18)
    fig.tight_layout()
    fig.savefig(OUT_BETA / "betas-chart.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor="#0b1524")
    ax.set_facecolor("#0b1524")
    ax.axis("off")
    ax.text(0.06, 0.72, "SYSTEMATIC RISK", color="#a89068", fontsize=12, fontfamily="monospace")
    ax.text(0.06, 0.52, "Equity Beta Estimation", color="#ffffff", fontsize=34, fontweight="bold")
    ax.text(
        0.06,
        0.38,
        "CRSP daily returns  ·  Big Tech vs the market",
        color="#c8d0dc",
        fontsize=14,
    )
    ax.text(
        0.06,
        0.18,
        "Python  ·  Pandas  ·  Covariance / Variance",
        color="#8fa3bc",
        fontsize=11,
    )
    fig.savefig(OUT_BETA / "cover.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    rng = np.random.default_rng(42)
    sizes = np.array([100, 1000, 20000])
    typical = np.empty(3)
    bad = np.empty(3)
    for i, n in enumerate(sizes):
        defaults = rng.random((5000, int(n))) < 0.02
        loss = defaults * 0.4
        year_loss = loss.mean(axis=1)
        typical[i] = year_loss.mean()
        bad[i] = np.quantile(year_loss, 0.95)

    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor="#0b0b0b")
    ax.set_facecolor("#0b0b0b")
    x = np.arange(len(sizes))
    width = 0.35
    ax.bar(x - width / 2, typical * 100, width=width, label="Typical year", color="#94a3b8")
    ax.bar(
        x + width / 2,
        bad * 100,
        width=width,
        label="Bad year (95th %ile)",
        color="#f87171",
    )
    ax.set_xticks(x)
    ax.set_xticklabels([f"{n:,} loans" for n in sizes], color="#cccccc")
    ax.set_ylabel("Portfolio loss rate", color="#dddddd")
    ax.set_title(
        "Loan Book Diversification — Typical vs Stress Loss",
        color="#ffffff",
        pad=14,
    )
    ax.tick_params(colors="#cccccc")
    ax.legend(facecolor="#151515", edgecolor="#333333", labelcolor="#eeeeee")
    for spine in ax.spines.values():
        spine.set_color("#333333")
    fig.tight_layout()
    fig.savefig(OUT_LOAN / "loss-chart.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor="#101d35")
    ax.set_facecolor("#101d35")
    ax.axis("off")
    ax.text(0.06, 0.72, "CREDIT RISK", color="#a89068", fontsize=12, fontfamily="monospace")
    ax.text(
        0.06,
        0.52,
        "Loan Book Diversification",
        color="#ffffff",
        fontsize=32,
        fontweight="bold",
    )
    ax.text(
        0.06,
        0.38,
        "Monte Carlo simulation of default losses across book sizes",
        color="#c8d0dc",
        fontsize=14,
    )
    ax.text(
        0.06,
        0.18,
        "Python  ·  NumPy  ·  5,000 simulated years",
        color="#8fa3bc",
        fontsize=11,
    )
    fig.savefig(OUT_LOAN / "cover.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close()

    print("ok")
    print("betas", list(zip(names, [round(b, 3) for b in betas])))
    print(
        "loan",
        list(zip(sizes.tolist(), (typical * 100).round(2), (bad * 100).round(2))),
    )


if __name__ == "__main__":
    main()
