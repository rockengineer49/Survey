def test_package_imports():
    import survey_app
    assert hasattr(survey_app, "__version__")
