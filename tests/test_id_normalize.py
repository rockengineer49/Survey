from survey_app.io.id_normalize import normalize_id

def test_normalize_id_basic():
    assert normalize_id("12") == "FP-12"
    assert normalize_id("12a") == "FP-12a"
    assert normalize_id("FP-12-b") == "FP-12-b"
