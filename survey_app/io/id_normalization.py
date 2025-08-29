import re

def normalize_id(raw_id):
    """
    Convert various forms of Hole ID into 'FP-XXX' format, with rules from your documentation.
    """
    if not isinstance(raw_id, str):
        return ""
    raw = raw_id.strip().upper().replace(" ", "")
    # Extract main number or identifier
    match = re.search(r'(?:FP-|FT-?|FT|FP)?\s*([0-9X]+)([A-Z-]*)', raw)
    if not match:
        return raw  # Fallback to raw if parse fails
    main, suffix = match.groups()
    main = main.lstrip("0")  # remove any leading zeros (optional)
    norm = f"FP-{main}"
    # Attach suffix (gap-pipe, battered, etc)
    if suffix:
        norm += suffix
    return norm
