# Survey: borehole survey processing app

## What this does
- Combines Baseline, Top‑of‑Pipe, and Downhole surveys into a versioned Survey CSV and a detailed changelog. [attached_file:1]
- Computes downhole coordinates using inclination, azimuth, and length; produces Point‑Elevation CSVs and standard graphs. [attached_file:1]
- Provides a simple GUI with four flows: Initialize Project, Update Survey, Elevation Data, and Graphs. [attached_file:1]

## Quick start
1. Create a virtual environment and install:
   - python -m venv .venv && . .venv/bin/activate  (Windows: .venv\Scripts\activate) [13]
   - pip install -e . [13]
2. Show CLI help:
   - survey --help [13]
3. Launch GUI (when implemented):
   - python -m survey_app.gui.app [1]

## Inputs and outputs
- Inputs:
  - Baseline Survey (ID, Northing, Easting, Elevation optional). [1]
  - Top‑of‑Pipe Survey (ID, Northing, Easting, Elevation). [1]
  - Downhole Survey (ID, azimuth, inclination, length; Northing/Easting may be arbitrary like 1000/1000/1000). [1]
- Outputs:
  - Survey: YYYY.MM.DD_PROJECT_Survey.csv (vX if multiple updates/day). [1]
  - Changelog: YYYY.MM.DD_PROJECT_Changelog.txt. [1]
  - Point‑Elevation CSV for a specified elevation. [1]
  - Graphs: Northing vs Depth, Easting vs Depth, Northing vs Easting. [1]
## Key rules and rules
- Normalize Hole IDs to FP‑XXX, FP‑XXXa (gap pipes), FP‑XXX-b (battered). [1]
- Replace Baseline with Surveyed when Top‑of‑Pipe is provided; attach downhole to the correct hole. [1]
- Report discrepancies: Baseline ±5.0 threshold; replace with newest data and log full details. [1]
   
## Project layout total
- src/survey_app/: io/, processing/, trajectory/, plotting/, gui/, cli.py, config.py. [13]
- tests/: unit tests; docs/: formulas and data dictionaries. [13]
