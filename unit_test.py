
import unittest
from ukpl import diagnosa  

class TestDiagnosa(unittest.TestCase):
    def test_gastritis(self):
        gejala = ["muntah", "tidak mau makan", "lemas"]
        hasil = diagnosa(gejala)
        self.assertIn("Gastritis", hasil)

    def test_flu_kemungkinan(self):
        gejala = ["batuk"]
        hasil = diagnosa(gejala)
        self.assertTrue(any("Flu" in h for h in hasil))

    def test_tidak_diketahui(self):
        gejala = ["luka", "pincang"]
        hasil = diagnosa(gejala)
        self.assertEqual(hasil, ["Tidak diketahui, konsultasikan ke dokter hewan"])

if __name__ == '__main__':
    unittest.main()
