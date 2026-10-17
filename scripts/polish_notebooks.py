import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

beta_path = ROOT / "notebooks" / "market-betas" / "BetaCalculations.ipynb"
nb = json.loads(beta_path.read_text(encoding="utf-8"))
for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    if "read_excel" in src:
        cell["source"] = [
            "import pandas as pd\n",
            "\n",
            "dataframe = pd.read_excel('crsp2025.xlsx')\n",
        ]
        break
intro = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Equity Beta Estimation\n",
        "\n",
        "Estimate equity betas for major tech names against the CRSP value-weighted market return:\n",
        "\n",
        r"$$\beta_i = \frac{\mathrm{Cov}(R_i, R_m)}{\mathrm{Var}(R_m)}$$" + "\n",
    ],
}
if not (nb["cells"] and nb["cells"][0].get("cell_type") == "markdown"):
    nb["cells"] = [intro] + nb["cells"]
beta_path.write_text(json.dumps(nb, indent=1), encoding="utf-8")

loan_path = ROOT / "notebooks" / "loan-book" / "LoanBook.ipynb"
nb2 = json.loads(loan_path.read_text(encoding="utf-8"))
intro2 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Loan Book Diversification\n",
        "\n",
        "Monte Carlo simulation of independent loan defaults (2% PD, 40% LGD) "
        "to show how portfolio loss risk falls as the book gets larger.\n",
    ],
}
for cell in nb2["cells"]:
    src = "".join(cell.get("source", []))
    if "risk profile of a loan book" in src or cell.get("source") == []:
        if "risk profile" in src:
            cell["cell_type"] = "markdown"
            cell["source"] = [
                "Larger books have similar *average* losses, but much thinner "
                "left-tail (bad-year) losses — diversification of idiosyncratic "
                "credit risk.\n"
            ]
            cell.pop("outputs", None)
            cell.pop("execution_count", None)
if not (nb2["cells"] and nb2["cells"][0].get("cell_type") == "markdown"):
    nb2["cells"] = [intro2] + nb2["cells"]
loan_path.write_text(json.dumps(nb2, indent=1), encoding="utf-8")
print("polished")
