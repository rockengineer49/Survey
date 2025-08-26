import re

def normalize_id(raw_id: str) -> str:
    """
    Normalize a raw hole ID string into the standard 'FP-XXX', 'FP-XXXa', 'FP-XXX-b', etc. format.
    
    Rules:
    - Extract the number (XXX) and any suffixes (like 'a', '-b').
    - Clean input by stripping spaces and converting to uppercase where applicable.
    - If input is already in FP-xxx form (like FP-103a or FP-103-B), return as uppercase.
    - IDs can come as: 'FP103', 'fp-104', '104', '104a', '104-b', etc.
    - Result: 'FP-104', 'FP-104A', 'FP-104-B', etc.

    Args:
        raw_id (str): The raw ID from the CSV/Excel file.

    Returns:
        str: The normalized ID string.
    """
    # Remove spaces and make upper
    clean = raw_id.replace(' ', '').upper()
    
    # Pattern: look for FP prefix (or not), digit sequence, possible suffixes
    match = re.match(r'(FP-?|)?(\d+)([A-Z]?|-B)?', clean)
    if not match:
        raise ValueError(f"Unrecognized hole ID format: {raw_id}")

    prefix, num, suffix = match.groups()
    norm_id = f"FP-{num}"
    if suffix:
        norm_id += suffix

    return norm_id

# ===== Optional: Batch normalization for a list/Series =====
def normalize_id_list(id_list):
    """
    Normalize a list or pandas.Series of IDs.
    """
    return [normalize_id(str(x)) for x in id_list]
