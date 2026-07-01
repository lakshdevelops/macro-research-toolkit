from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd


def plot_cumulative_returns(
    cumulative_returns: pd.DataFrame,
    output_path: str | Path,
    title: str = "Cumulative Returns",
) -> Path:
    """Save a cumulative returns line chart."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        _plot_cumulative_returns_svg(cumulative_returns, path, title)
        return path

    ax = cumulative_returns.plot(figsize=(11, 6), linewidth=1.8)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth of 1.0")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Asset", loc="best")

    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

    return path


def _plot_cumulative_returns_svg(
    cumulative_returns: pd.DataFrame,
    output_path: Path,
    title: str,
) -> None:
    """Dependency-free SVG fallback for restricted environments."""
    data = cumulative_returns.dropna(how="all")
    if data.empty:
        raise ValueError("No cumulative return data to plot.")

    width, height = 960, 540
    margin_left, margin_right, margin_top, margin_bottom = 72, 170, 56, 64
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    min_y = float(data.min().min())
    max_y = float(data.max().max())
    if min_y == max_y:
        min_y *= 0.95
        max_y *= 1.05

    colors = [
        "#2563eb",
        "#dc2626",
        "#16a34a",
        "#9333ea",
        "#ea580c",
        "#0891b2",
    ]

    def x_pos(i: int) -> float:
        if len(data.index) == 1:
            return margin_left + plot_width / 2
        return margin_left + (i / (len(data.index) - 1)) * plot_width

    def y_pos(value: float) -> float:
        return margin_top + (max_y - value) / (max_y - min_y) * plot_height

    chart_lines = []
    legend_items = []
    for column_index, column in enumerate(data.columns):
        series = data[column].dropna()
        if series.empty:
            continue

        points = []
        for date, value in series.items():
            row_index = data.index.get_loc(date)
            points.append(f"{x_pos(row_index):.2f},{y_pos(float(value)):.2f}")

        color = colors[column_index % len(colors)]
        chart_lines.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2.5" '
            f'points="{" ".join(points)}" />'
        )

        legend_y = margin_top + 24 * column_index
        legend_items.append(
            f'<line x1="{width - margin_right + 28}" y1="{legend_y}" '
            f'x2="{width - margin_right + 52}" y2="{legend_y}" '
            f'stroke="{color}" stroke-width="3" />'
            f'<text x="{width - margin_right + 60}" y="{legend_y + 5}" '
            f'font-size="14">{escape(str(column))}</text>'
        )

    start_label = escape(data.index[0].date().isoformat())
    end_label = escape(data.index[-1].date().isoformat())

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white" />
  <text x="{width / 2}" y="30" text-anchor="middle" font-size="22" font-family="Arial, sans-serif">{escape(title)}</text>
  <line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{margin_left + plot_width}" y2="{margin_top + plot_height}" stroke="#111827" />
  <line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_height}" stroke="#111827" />
  <line x1="{margin_left}" y1="{y_pos(1.0):.2f}" x2="{margin_left + plot_width}" y2="{y_pos(1.0):.2f}" stroke="#9ca3af" stroke-dasharray="5,5" />
  <text x="{margin_left}" y="{height - 24}" text-anchor="middle" font-size="13" font-family="Arial, sans-serif">{start_label}</text>
  <text x="{margin_left + plot_width}" y="{height - 24}" text-anchor="middle" font-size="13" font-family="Arial, sans-serif">{end_label}</text>
  <text x="22" y="{margin_top + plot_height / 2}" transform="rotate(-90 22 {margin_top + plot_height / 2})" text-anchor="middle" font-size="14" font-family="Arial, sans-serif">Growth of 1.0</text>
  <text x="{margin_left - 10}" y="{y_pos(max_y):.2f}" text-anchor="end" dominant-baseline="middle" font-size="12" font-family="Arial, sans-serif">{max_y:.2f}</text>
  <text x="{margin_left - 10}" y="{y_pos(min_y):.2f}" text-anchor="end" dominant-baseline="middle" font-size="12" font-family="Arial, sans-serif">{min_y:.2f}</text>
  {"".join(chart_lines)}
  {"".join(legend_items)}
</svg>
'''
    output_path.write_text(svg, encoding="utf-8")
