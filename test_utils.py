import unittest
import os
import csv
from utils import buat_data_riwayat, simpan_ke_csv

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_riwayat.csv"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_buat_data_riwayat_output(self):
        data = buat_data_riwayat("Ayu", "Dewasa", ["demam"], ["DBD"])
        self.assertEqual(data["nama"], "Ayu")
        self.assertEqual(data["jenis"], "Dewasa")
        self.assertIn("demam", data["gejala"])
        self.assertIn("DBD", data["hasil"])
        self.assertIn("waktu", data)
        self.assertRegex(data["waktu"], r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")  # Format waktu valid

    def test_buat_data_riwayat_kosong(self):
        data = buat_data_riwayat("Ayu", "Dewasa", [], [])
        self.assertEqual(data["gejala"], "")
        self.assertEqual(data["hasil"], "")

    def test_simpan_ke_csv_filebaru(self):
        data = buat_data_riwayat("TestUser", "Anak", ["flu"], ["Pilek"])
        simpan_ke_csv(data, self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))

        with open(self.test_filename, "r") as f:
            content = f.read()
        self.assertIn("waktu", content)
        self.assertIn("TestUser", content)
        self.assertIn("Anak", content)

    def test_simpan_ke_csv_tambah_data(self):
        data1 = buat_data_riwayat("User1", "Dewasa", ["batuk"], ["Flu"])
        data2 = buat_data_riwayat("User2", "Anak", ["demam"], ["DBD"])
        simpan_ke_csv(data1, self.test_filename)
        simpan_ke_csv(data2, self.test_filename)

        with open(self.test_filename, newline="") as f:
            reader = list(csv.reader(f))
        self.assertEqual(len(reader), 3)  # Header + 2 data
        self.assertIn("User1", reader[1][1])  # kolom "nama"
        self.assertIn("User2", reader[2][1])

    def test_file_header_tertulis_satu_kali(self):
        """Header hanya ditulis sekali meski file disimpan dua kali"""
        data = buat_data_riwayat("UjiHeader", "Kucing", ["gatal"], ["Kulit Jamuran"])
        simpan_ke_csv(data, self.test_filename)
        simpan_ke_csv(data, self.test_filename)

        with open(self.test_filename, "r") as f:
            lines = f.readlines()
        header_count = sum(1 for line in lines if "waktu,nama,jenis,gejala,hasil" in line)
        self.assertEqual(header_count, 1)

if __name__ == '__main__':
    unittest.main()
