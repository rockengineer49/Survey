from pathlib import Path
import json
import pandas as pd
from ..config import ProjectPaths
from ..io.id_normalize import normalize_id

def initialize_project(baseline_csv: str, out_dir: str, project_name: str, base_elevation: float | None = None) -> Path:
    """
    Initialize project:
      - Read baseline survey.
      - Normalize IDs; set Status='Baseline'.
      - Compute project center (mean Easting/Northing) and store in project_meta.json.
      - Ensure Elevation present (use base_elevation if missing).
      - Write YYYY.MM.DD_PROJECT_Survey.csv.
    Returns path to created Survey CSV.
    """
    # TODO: implement flexible column detection and writing logic per spec.
    raise NotImplementedError("initialize_project to be implemented")

