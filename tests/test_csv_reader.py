import unittest
import pandas as pd
from io import StringIO
from survey_app.io.csv_reader import read_survey_csv

class TestCSVReader(unittest.TestCase):

    def test_detects_standard_headers(self):
        csv = StringIO("""Hole ID,Northing,Easting,Elevation
A100,1200,1000,12.5
A101,1220,1005,12.0
""")
        df = read_survey_csv(csv)
        self.assertEqual(list(df.columns), ['ID', 'Easting', 'Northing', 'Elevation'])
        self.assertEqual(df.iloc[0]['ID'], 'FP-100')
        self.assertEqual(df.iloc[1]['Easting'], 1005)

    def test_detects_alt_headers(self):
        csv = StringIO("""number,ynorth,xeast,z
104b,1564,1444,37.2
105a,1570,1447,37.0
""")
        df = read_survey_csv(csv)
        self.assertTrue(set(['ID', 'Easting', 'Northing', 'Elevation']).issubset(df.columns))
        self.assertEqual(df.iloc[0]['ID'], 'FP-104-B')
        self.assertEqual(df.iloc[1]['ID'], 'FP-105A')
        self.assertEqual(df.iloc[0]['Northing'], 1564)
        self.assertEqual(df.iloc[1]['Easting'], 1447)

    def test_missing_elevation(self):
        csv = StringIO("""hole,x,y
98,1021,5022
""")
        df = read_survey_csv(csv)
        self.assertEqual(df.iloc[0]['ID'], 'FP-98')
        self.assertEqual(df.iloc[0]['Easting'], 1021)
        self.assertEqual(df.iloc[0]['Northing'], 5022)
        self.assertTrue('Elevation' in df.columns)
        self.assertTrue(pd.isna(df.iloc[0]['Elevation']) or df.iloc[0]['Elevation'] is None)

    def test_no_id_column(self):
        csv = StringIO("""foo,north,xeast
123,500,400
""")
        with self.assertRaises(ValueError):
            read_survey_csv(csv)

    def test_id_column_with_prefix_suffix(self):
        csv = StringIO("""ID: Bore,northing,easting
110a,1400,1340
""")
        df = read_survey_csv(csv)
        self.assertEqual(df.iloc[0]['ID'], 'FP-110A')

if __name__ == "__main__":
    unittest.main()
