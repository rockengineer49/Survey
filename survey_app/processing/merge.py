import pandas as pd
import numpy as np
import re

def normalize_hole_id(id_str):
    """
    Convert IDs to 'FP-XXX', 'FP-XXXa', 'FP-XXX-b' format.
    Accepts a variety of input header names/values.
    """
    if pd.isnull(id_str):
        return ''
    s = str(id_str).strip().replace(' ', '').replace('-', '').upper()
    # match e.g. FT501, FT-501a, FT501-B, FT 501, etc.
    match = re.match(r'([A-Z]+)([0-9]+)([A-Z\-]*)', s)
    if match:
        prefix, number, suffix = match.groups()
        base = f'FP-{number}'
        if suffix:
            return f"{base}{suffix.lower()}"
        return base
    # fallback: just number
    digits = ''.join(filter(str.isdigit, s))
    return f'FP-{digits}' if digits else s

def merge_downhole_to_baseline(baseline_df, downhole_df, top_of_pipe_df=None):
    changelog = {
        'updated_holes': [],
        'added_downhole': [],
        'conflicts': [],
        'msg': ''
    }
    # Normalize IDs
    baseline_df['ID_NORMALIZED'] = baseline_df.iloc[:,0].map(normalize_hole_id)
    downhole_df['ID_NORMALIZED'] = downhole_df['Hole'].map(normalize_hole_id)
    if top_of_pipe_df is not None:
        top_of_pipe_df['ID_NORMALIZED'] = top_of_pipe_df.iloc[:,0].map(normalize_hole_id)
        id2top = top_of_pipe_df.set_index('ID_NORMALIZED')
    else:
        id2top = baseline_df.set_index('ID_NORMALIZED')
    # Compose merged output
    merged_rows = []
    existing_ids = set(baseline_df['ID_NORMALIZED'])
    # Include baseline or top-of-pipe as main survey entry
    for idx, row in baseline_df.iterrows():
        merged_rows.append({
            'ID': row['ID_NORMALIZED'],
            'Easting': row.get('Easting', np.nan),
            'Northing': row.get('Northing', np.nan),
            'Elevation': row.get('Elevation', np.nan),
            'Status': 'Baseline'
        })
    # Downhole: for each unique hole
    for id_norm in sorted(downhole_df['ID_NORMALIZED'].unique()):
        downhole_points = downhole_df[downhole_df['ID_NORMALIZED'] == id_norm].copy()
        # get top coords
        if id_norm in id2top.index:
            top_east = id2top.loc[id_norm]['Easting']
            top_north = id2top.loc[id_norm]['Northing']
            top_elev = id2top.loc[id_norm]['Elevation']
        else:
            # Not found (could ask to add or skip)
            changelog['conflicts'].append(f'{id_norm} missing from baseline')
            continue
        # Compute offsets from top
        first_row = True
        for _, drow in downhole_points.iterrows():
            if first_row:
                # First row (0 depth), force to top coords
                merged_rows.append({
                    'ID': id_norm,
                    'Easting': top_east,
                    'Northing': top_north,
                    'Elevation': top_elev,
                    'Status': 'Downhole'
                })
                first_row = False
            else:
                # Other rows: calculate delta from first downhole point and add to top
                d_east = drow.get('Easting', 0.0) - downhole_points.iloc[0].get('Easting', 0.0)
                d_north = drow.get('Northing', 0.0) - downhole_points.iloc[0].get('Northing', 0.0)
                d_elev = drow.get('Elevation', 0.0) - downhole_points.iloc[0].get('Elevation', 0.0)
                merged_rows.append({
                    'ID': id_norm,
                    'Easting': top_east + d_east,
                    'Northing': top_north + d_north,
                    'Elevation': top_elev + d_elev,
                    'Status': 'Downhole'
                })
        changelog['added_downhole'].append(id_norm)
    merged_df = pd.DataFrame(merged_rows, columns=['ID','Easting','Northing','Elevation','Status'])
    # Remove temp columns if present
    if 'ID_NORMALIZED' in merged_df.columns:
        merged_df = merged_df.drop(columns=['ID_NORMALIZED'])
    changelog['msg'] = "Top-of-pipe coordinates set for all downhole rows. Merge complete."
    return merged_df, changelog

def merge_surveys(baseline_df, top_df=None, downhole_df=None):
    """
    Main wrapper to do merging. Returns merged_df, changelog.
    Uses logic from your merge_downhole_to_baseline if that's your main logic.
    """
    if downhole_df is not None:
        return merge_downhole_to_baseline(baseline_df, downhole_df, top_df)
    elif top_df is not None:
        result = top_df.copy()
        result['Status'] = 'Surveyed'
        changelog = {'updated_holes': list(result.index), 'msg': 'Merged top-of-pipe only'}
        return result, changelog
    else:
        raise ValueError("No update data provided.")
