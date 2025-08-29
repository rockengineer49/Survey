import unittest
import pandas as pd
from io import StringIO
from survey_app.io.downhole_loader import load_downhole_csv_for_merge

class TestDownholeLoader(unittest.TestCase):
    def setUp(self):
        # Example CSV with enough rows for strong tests
        self.csv = StringIO(
            "Quality,Pattern,Row,Hole,Deployment,Record Index,Azimuth,Inclination,Length,Deviation,Percent Deviation,Time,Easting,Northing,Elevation\n"
            ",,,ft 501,Deployment-1,0,,,0,,,,1000.00000,1031.11270,1000.00000\n"
            "Good,,,ft 501,Deployment-1,1,331.11508,0.68649,3.28,,,08:52:56,968.86831,968.92172,996.71940\n"
            "Good,,,ftX202,Deployment-1,1,0.0,0.0,1.0,,,08:52:56,1002.0,1001.0,999.0\n"
            ",,,,,,,,,,,,,,\n"  # empty row
            ",,, ,Deployment-1,0,,,0,,,,,,"  # blank hole
        )

    def test_loads_and_normalizes(self):
        df = load_downhole_csv_for_merge(self.csv)
        # Check columns and shape
        self.assertEqual(list(df.columns), ["ID", "Easting", "Northing", "Elevation"])
        # Only valid rows should remain (should drop the blank and empty ones)
        self.assertEqual(len(df), 3)
        # ID normalization e.g. FP-501, FP-X202
        self.assertEqual(df.iloc[0]["ID"], "FP-501")
        self.assertEqual(df.iloc[1]["ID"], "FP-501")
        self.assertEqual(df.iloc[2]["ID"], "FP-X202")
        # Data types should be numeric
        self.assertTrue(df["Easting"].apply(lambda x: isinstance(x, float)).all())

    def test_no_bad_rows(self):
        df = load_downhole_csv_for_merge(self.csv)
        # No rows where essential columns are missing or nan
        self.assertFalse(df["ID"].isnull().any())
        self.assertFalse(df["Easting"].isnull().any())
        self.assertFalse(df["Northing"].isnull().any())
        self.assertFalse(df["Elevation"].isnull().any())

if __name__ == "__main__":
    unittest.main()

