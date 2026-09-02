# NIST uniaxial tension data

The three CSVs here are extracts from the NIST Public Data Repository record
**mds2-2202**, "Data for Numisheet 2020 uniaxial tensile and tension/compression
tests" (DOI [10.18434/M32202](https://doi.org/10.18434/M32202)), used by
`Lecture03/lec03.ipynb`.

Cite as: Rust, E., Luecke, W. E., & Iadicola, M. A. (2020). *2020 Numisheet
benchmark study uniaxial tensile tests summary.* DOI: 10.18434/M32202.
NIST data is in the public domain.

## Why local copies

NIST's file distribution service (`https://data.nist.gov/od/ds/...`) is
unreliable -- it currently times out even for a 64-byte checksum sidecar, while
the metadata API on the same host responds normally. An in-class demo should not
depend on it, so the data ships with the course.

## What was extracted

Each original is a ~14 MB digital image correlation file with **1217 columns**
(X/Y/Z position and Hencky strain components across the specimen surface, plus
load-frame channels). The lecture reads exactly two of them, so only those two
are kept:

| column | note |
|---|---|
| `Displacement_(mm)` | crosshead displacement |
| `Force_(kN)` | load cell force |

All **1093 data rows** are preserved, so `len(curve1) == 1093` as Exercise 1
states. Column names are unchanged, so `csv.DictReader` code works against
either the extract or an original file.

## Provenance of the originals

Verified byte-for-byte against the SHA-256 hashes NIST publishes in its record
metadata before extraction:

| file | original size | SHA-256 (NIST published, verified) |
|---|---|---|
| `U15Al6XXX-T81_BatchB13R01T2.6921W12.71.csv` | 14,005,999 B | `38787897a2920fd8305daaab066275714300b6e28cd74f0c5e07cf6b360cc072` |
| `U30Al6XXX-T81_BatchB8R01T2.693W12.66.csv` | 14,346,901 B | `a6d419d57bd113765582390a6a6893283bd27d243d18d7528da034cf348cfb9c` |
| `U90Al6XXX-T81_BatchB5R03T2.684W12.68.csv` | 15,221,915 B | `e57d964265e0cbfbee95aa4d07bc2914760aa4f6fc8f8624cd48dac12fdde544` |

To regenerate from originals, keep the two named columns and drop the rest.
