import pandas as pd


def calculate_simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate period-on-period simple returns from price data."""
    return prices.pct_change(fill_method=None).dropna(how="all")


def calculate_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Convert simple returns into cumulative growth of 1 unit of capital."""
    return (1 + returns.fillna(0)).cumprod()
