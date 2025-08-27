def test_package_imports():
    import survey_app.init as init
    assert hasattr(init, "__version__")
