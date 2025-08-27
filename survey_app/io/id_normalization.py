import re

def normalize_id(raw_id):
    raw_id = str(raw_id)  # <-- Add this line!
    clean = raw_id.strip().upper()

    # Try to extract the first (letter(s))? number group and an optional -letter or letter suffix, skipping extra tokens
    # Accepts things like "ID: 131", "hole110a", etc.
    # It will find the first number in the string
    m = re.search(r'([A-Z]*)[-: ]*?(\d+)([A-Z]|-B)?', clean)
    if not m:
        raise ValueError(f"Unrecognized hole ID format: {raw_id}")

    _, num, suffix = m.groups()

    norm_id = f"FP-{num}"
    if suffix:
        # unify -B and B and A as suffixes (always "-B" and "A")
        if suffix in ["-B", "B"]:
            norm_id += "-B"
        else:
            norm_id += suffix
    return norm_id
