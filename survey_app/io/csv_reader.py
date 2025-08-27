import pandas as pd
from survey_app.io.id_normalization import normalize_id

# Possible column header keywords for each field, lowercased for easy matching
ID_COLS = ["id", "hole", "hole id", "hole-id", "number", "borehole"]
NORTHING_COLS = ["northing", "north", "y", "ynorth", "y_north", "n"]
EASTING_COLS = ["easting", "east", "x", "xeast", "x_east", "e"]
ELEVATION_COLS = ["elevation", "elev", "z"]

def match_column(headers, candidates):
    """
    Find the best match for a column in headers using candidate keywords.
    Returns the matched header or None.
    """
    for c in candidates:
        for h in headers:
            if c in h.lower().replace("_","").replace(" ",""):
                return h
    return None

def read_survey_csv(filepath):
    """
    Reads a survey CSV file, auto-detects columns for ID, Easting, Northing, Elevation,
    and returns a standardized DataFrame with normalized IDs.

    The resulting DataFrame will have columns: 'ID', 'Easting', 'Northing', 'Elevation' (Elevation optional).
    """
    df = pd.read_csv(filepath)
    headers = list(df.columns)

    # Find relevant columns by matching candidate keywords
    id_col = match_column(headers, ID_COLS)
    north_col = match_column(headers, NORTHING_COLS)
    east_col = match_column(headers, EASTING_COLS)
    elev_col = match_column(headers, ELEVATION_COLS) if match_column(headers, ELEVATION_COLS) else None

    if not (id_col and north_col and east_col):
        raise ValueError(f"Could not automatically identify ID/Northing/Easting columns in {filepath}.\nColumns found: {headers}")

    # Normalize IDs
    df['ID'] = df[id_col].apply(normalize_id)
    df['Northing'] = df[north_col]
    df['Easting'] = df[east_col]
    if elev_col:
        df['Elevation'] = df[elev_col]
    else:
        df['Elevation'] = None

    # Only keep standardized columns
    return df[['ID', 'Easting', 'Northing', 'Elevation']]
