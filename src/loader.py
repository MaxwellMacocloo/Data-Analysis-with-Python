"""Loading and cleaning the Mars crater dataset.

The raw PDS export has one quirk that quietly breaks naive analysis:
missing values are encoded as a single space rather than an empty field,
so pandas reads them as the string ``' '``. ``isnull()`` then reports
zero missing values for a column that is 99.7% empty.

The file also carries a UTF-8 BOM, which pandas strips on its own; it is
read with ``utf-8-sig`` here to make that explicit rather than accidental.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

NUMERIC_COLUMNS = [
    "LATITUDE_CIRCLE_IMAGE",
    "LONGITUDE_CIRCLE_IMAGE",
    "DIAM_CIRCLE_IMAGE",
    "DEPTH_RIMFLOOR_TOPOG",
    "NUMBER_LAYERS",
]


def load_craters(path=None):
    """Return the crater dataset as a cleaned DataFrame."""
    path = Path(path) if path else DATA_DIR / "marscrater_pds.csv"
    df = pd.read_csv(path, encoding="utf-8-sig")

    # Defensive: this export's headers are clean, but PDS files are not
    # consistent about it and a stray space makes df['CRATER_ID'] a KeyError.
    df.columns = [c.strip() for c in df.columns]

    # Blank-looking strings become real NaN so .isnull() reports the truth.
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # A crater with no diameter tells us nothing; drop those rows.
    df = df.dropna(subset=["DIAM_CIRCLE_IMAGE"])

    return df


def add_derived_columns(df):
    """Add the two features the rest of the analysis groups by."""
    df = df.copy()

    # Named craters are the scientifically notable ones.
    df["IS_NAMED"] = df["CRATER_NAME"].notna()

    # Size classes make a 380k-row table summarisable in one glance.
    df["SIZE_CLASS"] = pd.cut(
        df["DIAM_CIRCLE_IMAGE"],
        bins=[0, 2, 5, 20, 100, float("inf")],
        labels=["tiny (<2km)", "small (2-5km)", "medium (5-20km)",
                "large (20-100km)", "huge (100km+)"],
    )

    # Mars' hemispheres have famously different crater densities.
    df["HEMISPHERE"] = df["LATITUDE_CIRCLE_IMAGE"].apply(
        lambda lat: "Northern" if lat >= 0 else "Southern"
    )

    return df


def load_mtcars(path=None):
    """Return the mtcars dataset, used for the grouped-bar example."""
    path = Path(path) if path else DATA_DIR / "mtcars.csv"
    return pd.read_csv(path)
