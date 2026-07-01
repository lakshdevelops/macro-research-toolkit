import pandas as pd
from pandas.testing import assert_frame_equal

from macro_research_toolkit.analysis.returns import (
    calculate_cumulative_returns,
    calculate_simple_returns,
)


def test_calculate_returns_and_cumulative_returns() -> None:
    prices = pd.DataFrame(
        {
            "SPY": [100.0, 110.0, 121.0],
            "TLT": [100.0, 90.0, 99.0],
        },
        index=pd.to_datetime(["2024-01-31", "2024-02-29", "2024-03-31"]),
    )

    returns = calculate_simple_returns(prices)
    expected_returns = pd.DataFrame(
        {
            "SPY": [0.10, 0.10],
            "TLT": [-0.10, 0.10],
        },
        index=pd.to_datetime(["2024-02-29", "2024-03-31"]),
    )

    cumulative_returns = calculate_cumulative_returns(returns)
    expected_cumulative_returns = pd.DataFrame(
        {
            "SPY": [1.10, 1.21],
            "TLT": [0.90, 0.99],
        },
        index=pd.to_datetime(["2024-02-29", "2024-03-31"]),
    )

    assert_frame_equal(returns, expected_returns)
    assert_frame_equal(cumulative_returns, expected_cumulative_returns)
