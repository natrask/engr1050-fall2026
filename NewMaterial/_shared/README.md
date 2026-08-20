# Shared assets

This folder holds images, data files, and Thonny scripts referenced by lecture notebooks.

## What lives here

```
_shared/
  Images/        - PNG/JPG figures embedded in notebook markdown cells
  Data/          - CSV, MAT, PKL files loaded by notebooks
  ThonnyScripts/ - .py scripts that run on the Raspberry Pi Pico
  FastfoodData/  - HW5 data aggregation notebooks and CSV
  labcode/       - reference Python code from in-class labs (whack-a-mole, etc.)
```

## Populating from the Fall 2025 archive

The Fall 2025 repository (`PIMILab/ENGR1050`) holds the canonical copies of these files. To populate this folder from a local clone of last year's repo, run:

```bash
SRC=~/path/to/ENGR1050   # Fall 2025 repo
DST=NewMaterial/_shared

cp "$SRC/images/"*.{jpg,jpeg,png}                                "$DST/Images/"        2>/dev/null
cp "$SRC/notebooks/Images/"*.{jpg,jpeg,png}                      "$DST/Images/"        2>/dev/null
cp "$SRC/notebooks/Data/"*.{csv,pkl}                             "$DST/Data/"          2>/dev/null
cp "$SRC/notebooks/Data/example_pickle_usage.py"                 "$DST/Data/"          2>/dev/null
cp "$SRC/notebooks/"*.mat                                        "$DST/Data/"          2>/dev/null
cp "$SRC/notebooks/ThonnyScripts/"*.py                           "$DST/ThonnyScripts/" 2>/dev/null
cp "$SRC/notebooks/FastfoodData/DATA_PROCESSING_GUIDE.md"        "$DST/FastfoodData/"  2>/dev/null
cp "$SRC/notebooks/FastfoodData/aggregate_submissions.ipynb"     "$DST/FastfoodData/"  2>/dev/null
cp "$SRC/notebooks/FastfoodData/aggregated_fast_food_data.csv"   "$DST/FastfoodData/"  2>/dev/null
cp "$SRC/notebooks/FastfoodData/analyze_aggregated_data.ipynb"   "$DST/FastfoodData/"  2>/dev/null
```

## Notes

- `notebooks/Data/SecretSquirrel/` from the Fall 2025 repo is intentionally not migrated.
- `notebooks/FastfoodData/CHAT_TRANSCRIPT.md` from the Fall 2025 repo is intentionally not migrated.
- Many notebooks also fetch data over HTTP via `urllib.request.urlretrieve`, so they continue to function even when the local cache is missing.
