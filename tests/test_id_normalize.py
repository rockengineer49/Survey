import unittest
from survey_app.io.id_normalization import normalize_id

class TestNormalizeID(unittest.TestCase):
    def test_simple_numeric(self):
        self.assertEqual(normalize_id("103"), "FP-103")
        self.assertEqual(normalize_id("104"), "FP-104")
    
    def test_letters_and_case(self):
        self.assertEqual(normalize_id("fp-104"), "FP-104")
        self.assertEqual(normalize_id("FP104"), "FP-104")
        self.assertEqual(normalize_id("Fp-120a"), "FP-120A")
    
    def test_gap_and_battered(self):
        self.assertEqual(normalize_id("104a"), "FP-104A")
        self.assertEqual(normalize_id("104-b"), "FP-104-B")
        self.assertEqual(normalize_id("FP-107-b"), "FP-107-B")
        self.assertEqual(normalize_id("fp108-B"), "FP-108-B")
    
    def test_weird_format(self):
        self.assertEqual(normalize_id("ID: 131"), "FP-131")
        self.assertEqual(normalize_id("hole110a"), "FP-110A")
        self.assertEqual(normalize_id("Number: 112"), "FP-112")
        
    def test_spaces(self):
        self.assertEqual(normalize_id(" fp-113 "), "FP-113")
        self.assertEqual(normalize_id(" 115a "), "FP-115A")
    
    def test_invalid(self):
        with self.assertRaises(ValueError):
            normalize_id("abcdef")
        with self.assertRaises(ValueError):
            normalize_id("")

if __name__ == "__main__":
    unittest.main()
