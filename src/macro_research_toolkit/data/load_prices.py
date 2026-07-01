from pathlib import Path

import pandas as pd


def load_price_csv(path: str | Path) -> pd.DataFrame:
    """Load a wide price CSV indexed by date.

    Expected shape:
        date,SPY,TLT,GLD
        2024-01-31,100.0,101.0,99.5
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Price file not found: {csv_path}")

    prices = pd.read_csv(csv_path, parse_dates=["date"])
    if "date" not in prices.columns:
        raise ValueError("Price CSV must contain a 'date' column.")

    prices = prices.set_index("date").sort_index()
    validate_prices(prices)
    return prices


def validate_prices(prices: pd.DataFrame) -> None:
    """Run basic validation checks before analysis."""
    if prices.empty:
        raise ValueError("Price data is empty.")

    if not prices.index.is_monotonic_increasing:
        raise ValueError("Price index must be sorted in increasing date order.")

    if prices.index.has_duplicates:
        raise ValueError("Price index contains duplicate dates.")

    if prices.columns.empty:
        raise ValueError("Price data must contain at least one asset column.")

    non_numeric = prices.select_dtypes(exclude=["number"]).columns.tolist()
    if non_numeric:
        raise ValueError(f"Price columns must be numeric. Non-numeric columns: {non_numeric}")

    if (prices <= 0).any().any():
        raise ValueError("Prices must be positive.")
