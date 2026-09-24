"""Chart generation. Every function saves a PNG and returns its path.

Matplotlib runs on the non-interactive Agg backend so the CLI works over
SSH and in CI, where no display is attached.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

sns.set_theme(style="whitegrid")


def _save(fig, name):
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_diameter_distribution(df):
    """Histogram of crater diameters on a log x-axis.

    Diameters span four orders of magnitude, so a linear axis would crush
    every crater into the first bin.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["DIAM_CIRCLE_IMAGE"], bins=60, log_scale=True,
                 color="#c1440e", edgecolor="white", ax=ax)
    ax.set_title("Distribution of Mars crater diameters")
    ax.set_xlabel("Diameter (km, log scale)")
    ax.set_ylabel("Number of craters")
    return _save(fig, "01_diameter_distribution.png")


def plot_size_class_counts(summary):
    """Bar chart of crater counts per size class."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(summary.index.astype(str), summary["craters"], color="#c1440e")
    ax.set_title("Crater count by size class")
    ax.set_xlabel("Size class")
    ax.set_ylabel("Number of craters")
    ax.tick_params(axis="x", rotation=20)

    for i, value in enumerate(summary["craters"]):
        ax.text(i, value, f"{value:,}", ha="center", va="bottom", fontsize=9)

    return _save(fig, "02_size_class_counts.png")


def plot_hemisphere_comparison(df):
    """Box plot comparing diameters north and south of the equator."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=df, x="HEMISPHERE", y="DIAM_CIRCLE_IMAGE",
                hue="HEMISPHERE", legend=False, palette="rocket", ax=ax)
    ax.set_yscale("log")
    ax.set_title("Crater diameter by hemisphere")
    ax.set_xlabel("Hemisphere")
    ax.set_ylabel("Diameter (km, log scale)")
    return _save(fig, "03_hemisphere_comparison.png")


def plot_spatial_scatter(df, sample_size=20000):
    """Scatter of crater positions, coloured by diameter.

    The full 380k points overplot into a solid block, so this samples a
    readable subset with a fixed seed for reproducibility.
    """
    sample = df.sample(min(sample_size, len(df)), random_state=42)

    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = ax.scatter(
        sample["LONGITUDE_CIRCLE_IMAGE"],
        sample["LATITUDE_CIRCLE_IMAGE"],
        c=sample["DIAM_CIRCLE_IMAGE"],
        s=4, alpha=0.5, cmap="inferno",
        norm=matplotlib.colors.LogNorm(),
    )
    ax.set_title(f"Crater positions on Mars (sample of {len(sample):,})")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.axhline(0, color="#3b82f6", linewidth=1, linestyle="--")
    fig.colorbar(scatter, ax=ax, label="Diameter (km)")
    return _save(fig, "04_spatial_scatter.png")


def plot_correlation_heatmap(corr):
    """Annotated heatmap of the correlation matrix."""
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0,
                fmt=".3f", linewidths=0.5, ax=ax)
    ax.set_title("Correlation between crater measurements")
    return _save(fig, "05_correlation_heatmap.png")


def plot_depth_vs_diameter(df, sample_size=15000):
    """Scatter of depth against diameter, both on log axes."""
    subset = df[(df["DEPTH_RIMFLOOR_TOPOG"] > 0) & (df["DIAM_CIRCLE_IMAGE"] > 0)]
    sample = subset.sample(min(sample_size, len(subset)), random_state=42)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(sample["DIAM_CIRCLE_IMAGE"], sample["DEPTH_RIMFLOOR_TOPOG"],
               s=5, alpha=0.3, color="#c1440e")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Crater depth against diameter")
    ax.set_xlabel("Diameter (km, log scale)")
    ax.set_ylabel("Depth (km, log scale)")
    return _save(fig, "06_depth_vs_diameter.png")


def plot_mtcars_mpg(mtcars):
    """Grouped bar chart of fuel economy by cylinder count."""
    summary = mtcars.groupby("cyl")["mpg"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary["cyl"].astype(str), summary["mpg"], color="#2563eb")
    ax.set_title("Mean fuel economy by cylinder count (mtcars)")
    ax.set_xlabel("Cylinders")
    ax.set_ylabel("Mean MPG")

    for i, value in enumerate(summary["mpg"]):
        ax.text(i, value, f"{value:.1f}", ha="center", va="bottom")

    return _save(fig, "07_mtcars_mpg_by_cylinder.png")
