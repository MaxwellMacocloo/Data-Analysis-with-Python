# Notebooks

The learning notebooks behind the analysis in the repo root. Teaching
notebooks first, then the assignments and their solutions.

```bash
pip install -r ../requirements.txt
jupyter notebook
```

All outputs are committed, so every notebook renders on GitHub without
running anything.

## Teaching notebooks

| Notebook | Cells | Covers |
|---|---|---|
| [numpy.ipynb](numpy.ipynb) | 19 | Array creation, `reshape`, `arange`, `ones`, `eye`; `ndim`/`size`/`shape`/`dtype`; vectorised arithmetic; ufuncs (`sqrt`, `exp`, `log`, `sin`); slicing and indexing; element assignment; mean/median/std/variance/percentiles; z-score normalisation; boolean logic with `&`, `|`, `~` |
| [Pandas.ipynb](Pandas.ipynb) | 56 | Series from lists and dicts with custom indexes; DataFrames from dicts and records; `head`/`tail`/`describe`/`dtypes`; adding and dropping columns and rows; `loc`; missing values with `isnull` and `fillna`; `rename`; `astype`; `apply` with a lambda; `groupby` with single and multiple keys; `agg` with several functions; all four join types; reading CSV, JSON, HTML, Excel and pickle |
| [Visualization.ipynb](Visualization.ipynb) | 30 | Matplotlib line plots with markers and styling, `subplot` grids, bar and horizontal bar, histograms, scatter, pie with `explode`; then Seaborn `scatterplot`, `lineplot`, `catplot`, `boxplot`, `barplot`, `violinplot`, `histplot` with KDE, `kdeplot`, `pairplot` with `hue`, and an annotated correlation `heatmap` |

## Assignments

| Notebook | Cells | Notes |
|---|---|---|
| [numpyassignments.ipynb](numpyassignments.ipynb) | 17 | Questions |
| [numpysolutions.ipynb](numpysolutions.ipynb) | 40 | Worked solutions |
| [pandasasssignments.ipynb](pandasasssignments.ipynb) | 2 | Questions |
| [pandassolution.ipynb](pandassolution.ipynb) | 40 | Worked solutions |

## Datasets

All data lives in [`../data/`](../data/), shared with the analysis
package in the repo root rather than duplicated here.

| File | Rows | Used by |
|---|---|---|
| `marscrater_pds.csv` | 384,343 | Pandas.ipynb, and the package in `../src/` |
| `mtcars.csv` | 32 | Visualization.ipynb |
| `EP.health.csv` | 168 | Visualization.ipynb |
| `data.xlsx` | 3 | Pandas.ipynb, for the `read_excel` lesson |

Paths in the notebooks are relative (`../data/...`), so they work from a
fresh clone on any machine. Run the notebooks from this directory.

## Cells that are expected to fail

A few cells in `Pandas.ipynb` demonstrate syntax against columns that do
not exist in the crater dataset, and will raise if you run the notebook
straight through. They are left as written, because the syntax is the
point of the lesson:

| Cell | What happens |
|---|---|
| `data.fillna(data.mean(), ...)` | `TypeError: Cannot perform reduction 'mean' with string dtype` — the crater data has text columns. Use `data.select_dtypes('number').mean()`. |
| `data['column_name'].fillna(...)` | `KeyError` — `'column_name'` is a placeholder, not a real column. |
| `data.rename(columns={'old_column_name': ...})` | No error, but renames nothing, for the same reason. |
| `dff2.astype({'ID': 'int64'})` | `KeyError` — the rename above it targets `'CRATER_ID '` with a trailing space, which matches no column, so `ID` never gets created. Drop the space and it becomes a `ValueError` instead, because crater ids look like `01-000000`. |

`data.pkl` is not committed: the `read_excel` cell just above creates it,
so it appears the first time you run the notebook.
