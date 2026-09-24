"""Statistics and aggregations over the crater dataset.

NumPy handles the descriptive statistics, pandas handles the grouping.
Every function returns data rather than printing it, so the CLI stays in
charge of presentation.
"""

import numpy as np
import pandas as pd


def describe_column(df, column):
    """Return the standard descriptive statistics for one numeric column."""
    values = df[column].dropna().to_numpy()

    return {
        "count": int(values.size),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std_dev": float(np.std(values)),
        "variance": float(np.var(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "p25": float(np.percentile(values, 25)),
        "p75": float(np.percentile(values, 75)),
    }


def normalise(df, column):
    """Return the column rescaled to mean 0, standard deviation 1.

    This is the z-score every ML pipeline applies before training, done
    here with plain NumPy so the arithmetic stays visible.
    """
    values = df[column].dropna().to_numpy()
    return (values - np.mean(values)) / np.std(values)


def missing_value_report(df):
    """Return a per-column count and percentage of missing values."""
    missing = df.isnull().sum()
    report = pd.DataFrame({
        "missing": missing,
        "percent": (missing / len(df) * 100).round(2),
    })
    return report[report["missing"] > 0].sort_values("missing", ascending=False)


def size_class_summary(df):
    """Aggregate diameter and depth by the derived size class."""
    return df.groupby("SIZE_CLASS", observed=True).agg(
        craters=("DIAM_CIRCLE_IMAGE", "count"),
        mean_diameter=("DIAM_CIRCLE_IMAGE", "mean"),
        mean_depth=("DEPTH_RIMFLOOR_TOPOG", "mean"),
        mean_layers=("NUMBER_LAYERS", "mean"),
    ).round(3)


def hemisphere_summary(df):
    """Compare the northern and southern hemispheres."""
    return df.groupby("HEMISPHERE").agg(
        craters=("DIAM_CIRCLE_IMAGE", "count"),
        mean_diameter=("DIAM_CIRCLE_IMAGE", "mean"),
        largest=("DIAM_CIRCLE_IMAGE", "max"),
    ).round(3)


def ejecta_summary(df, top_n=10):
    """Return the most common ejecta morphologies and their mean diameter."""
    summary = df.groupby("MORPHOLOGY_EJECTA_1").agg(
        craters=("DIAM_CIRCLE_IMAGE", "count"),
        mean_diameter=("DIAM_CIRCLE_IMAGE", "mean"),
    ).round(3)
    return summary.sort_values("craters", ascending=False).head(top_n)


def largest_craters(df, top_n=10):
    """Return the largest named craters."""
    named = df[df["IS_NAMED"]]
    columns = ["CRATER_NAME", "DIAM_CIRCLE_IMAGE", "DEPTH_RIMFLOOR_TOPOG",
               "LATITUDE_CIRCLE_IMAGE", "HEMISPHERE"]
    return named.nlargest(top_n, "DIAM_CIRCLE_IMAGE")[columns]


def correlation_matrix(df):
    """Return the correlation matrix for the numeric measurements."""
    columns = ["DIAM_CIRCLE_IMAGE", "DEPTH_RIMFLOOR_TOPOG",
               "NUMBER_LAYERS", "LATITUDE_CIRCLE_IMAGE"]
    return df[columns].corr().round(3)


def depth_to_diameter_ratio(df):
    """Return the depth/diameter ratio for craters that report both.

    A near-constant ratio is the signature of simple bowl-shaped craters;
    the ratio collapsing at large diameters marks the transition to
    complex craters with central peaks.
    """
    subset = df[(df["DEPTH_RIMFLOOR_TOPOG"] > 0) & (df["DIAM_CIRCLE_IMAGE"] > 0)].copy()
    subset["RATIO"] = subset["DEPTH_RIMFLOOR_TOPOG"] / subset["DIAM_CIRCLE_IMAGE"]

    return subset.groupby("SIZE_CLASS", observed=True)["RATIO"].agg(
        ["count", "mean", "std"]
    ).round(4)
