import pandas as pd
from survey_app.io.id_normalization import normalize_id

def load_downhole_csv_for_merge(filepath):
    """
    Reads a Downhole (Boretrak) CSV file (exported from the program), returns a DataFrame
    suitable for merging with baseline/top-of-pipe.
    Only includes rows with valid geometry and IDs, and normalizes IDs.
    Output columns: ['ID', 'Easting', 'Northing', 'Elevation']
    """
    df = pd.read_csv(filepath)

    # Drop rows with no Hole or no position data
    df = df[df['Hole'].notnull() & df['Easting'].notnull() & df['Northing'].notnull() & df['Elevation'].notnull()]

    # Normalize IDs
    df['ID'] = df['Hole'].apply(normalize_id)

    # Convert numerical columns in case they're strings
    for col in ('Easting', 'Northing', 'Elevation'):
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows missing key data after conversion
    out = df[['ID', 'Easting', 'Northing', 'Elevation']].dropna(subset=['ID', 'Easting', 'Northing', 'Elevation'])

    return out.reset_index(drop=True)
