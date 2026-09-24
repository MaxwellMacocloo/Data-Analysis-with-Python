"""Command-line entry point for the Mars crater analysis.

Usage:
    python main.py              # full report + all charts
    python main.py --no-charts  # statistics only, skips plotting
    python main.py --stats-only # same as --no-charts
"""

import argparse

from src import analysis, loader, plots


def banner(title):
    print()
    print("=" * 68)
    print(f"  {title}")
    print("=" * 68)


def run(make_charts=True):
    banner("LOADING DATA")
    df = loader.load_craters()
    df = loader.add_derived_columns(df)
    print(f"Loaded {len(df):,} craters across {len(df.columns)} columns.")

    banner("MISSING VALUES")
    missing = analysis.missing_value_report(df)
    print(missing.to_string() if not missing.empty else "No missing values.")

    banner("DIAMETER STATISTICS (km)")
    for key, value in analysis.describe_column(df, "DIAM_CIRCLE_IMAGE").items():
        print(f"  {key:<10} {value:>14,.3f}")

    banner("NORMALISATION CHECK")
    normalised = analysis.normalise(df, "DIAM_CIRCLE_IMAGE")
    print(f"  mean after z-score : {normalised.mean():.10f}")
    print(f"  std  after z-score : {normalised.std():.10f}")

    banner("SUMMARY BY SIZE CLASS")
    size_summary = analysis.size_class_summary(df)
    print(size_summary.to_string())

    banner("SUMMARY BY HEMISPHERE")
    print(analysis.hemisphere_summary(df).to_string())

    banner("TOP 10 EJECTA MORPHOLOGIES")
    print(analysis.ejecta_summary(df).to_string())

    banner("10 LARGEST NAMED CRATERS")
    print(analysis.largest_craters(df).to_string(index=False))

    banner("DEPTH / DIAMETER RATIO BY SIZE CLASS")
    print(analysis.depth_to_diameter_ratio(df).to_string())

    banner("CORRELATION MATRIX")
    corr = analysis.correlation_matrix(df)
    print(corr.to_string())

    if not make_charts:
        print("\nCharts skipped (--no-charts).")
        return

    banner("GENERATING CHARTS")
    written = [
        plots.plot_diameter_distribution(df),
        plots.plot_size_class_counts(size_summary),
        plots.plot_hemisphere_comparison(df),
        plots.plot_spatial_scatter(df),
        plots.plot_correlation_heatmap(corr),
        plots.plot_depth_vs_diameter(df),
        plots.plot_mtcars_mpg(loader.load_mtcars()),
    ]
    for path in written:
        print(f"  saved {path.name}")
    print(f"\n{len(written)} charts written to outputs/")


def main():
    parser = argparse.ArgumentParser(description="Mars crater exploratory analysis")
    parser.add_argument("--no-charts", "--stats-only", dest="no_charts",
                        action="store_true", help="print statistics without plotting")
    args = parser.parse_args()
    run(make_charts=not args.no_charts)


if __name__ == "__main__":
    main()
