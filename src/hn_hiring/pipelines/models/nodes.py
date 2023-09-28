"""
This is a boilerplate pipeline 'models'
generated using Kedro 0.18.12
"""

from typing import Dict, Tuple

import matplotlib.pyplot as plt


def plot_companies_karma(data: Dict[str, Tuple[str, str, int]], n: int = 10):
    # drop any companies with null karma company, or user
    # Remove keys with None values
    data = {k: v for k, v in data.items() if None not in v}

    # Sort data by values and select top n
    sorted_data = dict(
        sorted(data.items(), key=lambda item: item[1][2], reverse=True)[:n]
    )

    # Transform data
    labels = [v[0][:20] for v in sorted_data.values()]
    values = [v[2] for v in sorted_data.values()]
    overlays = [v[1] for v in sorted_data.values()]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(labels, values, color="skyblue")

    # Add overlays
    for bar, overlay in zip(bars, overlays):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            overlay,
            va="center",
            ha="right",
            color="black",
            fontsize=10,
        )

    ax.set_xlabel("Company Karma")
    ax.set_title("Companies' karma rank barh plot")
    ax.invert_yaxis()  # Flip the y-axis
    return plt
