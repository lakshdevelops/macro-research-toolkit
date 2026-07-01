from pathlib import Path

from macro_research_toolkit.analysis.returns import (
    calculate_cumulative_returns,
    calculate_simple_returns,
)
from macro_research_toolkit.data.load_prices import load_price_csv
from macro_research_toolkit.viz.plots import plot_cumulative_returns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRICE_FILE = PROJECT_ROOT / "data" / "raw" / "sample_prices.csv"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / "reports" / "figures" / "cumulative_returns.svg"


def main() -> None:
    prices = load_price_csv(DEFAULT_PRICE_FILE)
    returns = calculate_simple_returns(prices)
    cumulative_returns = calculate_cumulative_returns(returns)

    output_path = plot_cumulative_returns(cumulative_returns, DEFAULT_OUTPUT_FILE)

    print(f"Loaded prices: {prices.shape[0]} rows x {prices.shape[1]} assets")
    print(f"Calculated returns: {returns.shape[0]} rows x {returns.shape[1]} assets")
    print(f"Saved chart: {output_path}")


if __name__ == "__main__":
    main()
