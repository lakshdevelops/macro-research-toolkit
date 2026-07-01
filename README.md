# macro-research-toolkit

A Python-first macro research engineering toolkit built step by step for learning quantitative research workflows.

The first version is deliberately small:

1. Load ETF-style price data from CSV.
2. Validate the basic shape of the data.
3. Calculate simple returns.
4. Plot cumulative returns.

Later versions will add SQLite storage, a monthly momentum backtest, transaction costs, performance/risk metrics, a Streamlit dashboard, tests, and README polish.

## Why This Project Exists

This project is designed to prepare for Quantitative / Software Developer work at King's Quant Society:

- reproducible Python research tooling
- data ingestion and validation
- local storage with SQLite
- backtesting with careful timestamp handling
- portfolio and risk utilities
- reports and dashboarding
- clean GitHub structure and readable code

## Setup

From inside the project folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## First Run

```bash
python scripts/01_first_returns_plot.py
```

This reads `data/raw/sample_prices.csv` and writes:

```text
reports/figures/cumulative_returns.svg
```

## Tests

```bash
pytest
```

The first test checks the basic return and cumulative-return calculations. This matters because the later backtest will depend on the same return logic.

## Git Workflow

When you are ready to track the project:

```bash
git init
git add .
git commit -m "Create first returns research workflow"
```

## Data Shape

For now, price files should be wide CSVs:

```text
date,SPY,TLT,GLD,EEM
2023-01-31,100.0,100.0,100.0,100.0
2023-02-28,102.1,98.7,101.5,99.4
```

Each column after `date` is one asset. Values should be adjusted close prices when using real market data.

## Roadmap

- Step 1: CSV prices, returns, cumulative returns plot
- Step 2: Download real ETF data with `yfinance`
- Step 3: Store clean prices in SQLite
- Step 4: Add monthly momentum ranking
- Step 5: Add portfolio backtest with transaction costs
- Step 6: Add performance metrics such as CAGR, volatility, Sharpe, drawdown
- Step 7: Add Streamlit dashboard
- Step 8: Add tests and GitHub-ready documentation
