import re

def normalize_id(raw: str) -> str:
    """
    Normalize hole IDs to:
      - FP-XXX      (number)
      - FP-XXXa     (gap pipe suffix letter, e.g., 'a')
      - FP-XXX-b    (battered pipe marker '-b')
    Rules:
      - Accept many incoming forms (ID, Hole-ID, number, etc.).
      - If incoming format not 'FP-*', extract the numeric part and optional 'a' letter.
      - Preserve '-b' when present after the number.
    Examples:
      '12' -> 'FP-12'
      '12a' -> 'FP-12a'
      'FP-12-b' -> 'FP-12-b'
    """
    s = (raw or "").strip()
    m = re.search(r"(?i)fp[- ]*(\d+)([a-z])?(-b)?$", s)
    if m:
        num, letter, battered = m.groups()
        return f"FP-{int(num)}{letter or ''}{battered or ''}"
    m = re.search(r"(\d+)([a-z])?(-b)?$", s, flags=re.I)
    if m:
        num, letter, battered = m.groups()
        return f"FP-{int(num)}{(letter or '').lower()}{(battered or '').lower()}"
    return s  # last resort: keep as-is to flag upstream

