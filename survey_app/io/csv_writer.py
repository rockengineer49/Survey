import pandas as pd
import os
from datetime import datetime

def make_survey_filename(project, outdir, version=None, date=None):
    if date is None:
        date = datetime.today()
    datestr = date.strftime("%Y.%m.%d")
    filename = f"{datestr}_{project}_Survey"
    if version:
        filename += f"_v{version}"
    return os.path.join(outdir, filename + ".csv")

def write_survey_csv(df, project, outdir, status='Baseline', version=None, date=None):
    """
    Write standardized survey file with columns in correct order + status.
    Returns the full path written.
    """
    save_df = df.copy()
    save_df['Status'] = status
    columns = ['ID', 'Status', 'Easting', 'Northing', 'Elevation']
    for col in columns:
        if col not in save_df.columns:
            save_df[col] = None
    save_df = save_df[columns]
    out_path = make_survey_filename(project, outdir, version, date)
    save_df.to_csv(out_path, index=False)
    return out_path
