"""A small, consistent look for the charts of the workshop."""

import matplotlib.pyplot as plt

# Three colors that stay distinguishable with the common color-vision deficiencies.
# A chart that needs more than three series is better split into several charts.
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]
MUTED_COLOR = "#8a8880"


def apply_style() -> None:
    """Set the matplotlib defaults used in the analysis files. Call it once per session."""
    plt.rcParams.update(
        {
            "axes.prop_cycle": plt.cycler(color=SERIES_COLORS),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.titlelocation": "left",
            "axes.titleweight": "bold",
            "grid.color": "#e4e2dc",
            "grid.linewidth": 0.8,
            "lines.linewidth": 1.6,
            "legend.frameon": False,
            "figure.figsize": (8.0, 4.0),
            "figure.dpi": 110,
            "figure.constrained_layout.use": True,
        }
    )
