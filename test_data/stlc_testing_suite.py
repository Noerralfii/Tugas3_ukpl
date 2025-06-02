# STLC Extended Testing Suite for utils.py
import sys
import os
sys.path.append(os.path.abspath(".."))  # Tambahkan folder di atas ke path Python

from utils import buat_data_riwayat, simpan_ke_csv

import unittest
import os
import time
from utils import buat_data_riwayat, simpan_ke_csv

class TestUtilsUnit(unittest.TestCase):
    # ---------- UNIT TESTING ----------
    def test_buat_data_riwayat_valid(self):
        data = buat_data_riwayat("Ayu", "Dewasa", ["demam"], ["DBD"])
        self.assertEqual(data["nama"], "Ayu")
        self.assertEqual(data["jenis"], "Dewasa")
        self.assertIn("demam", data["gejala"])
        self.assertIn("DBD", data["hasil"])

    def test_buat_data_riwayat_kosong(self):
        data = buat_data_riwayat("Ayu", "Dewasa", [], [])
        self.assertEqual(data["gejala"], "")
        self.assertEqual(data["hasil"], "")

    def test_simpan_ke_csv_filebaru(self):
        filename = "test_unit.csv"
        if os.path.exists(filename):
            os.remove(filename)
        data = buat_data_riwayat("Test", "Anak", ["flu"], ["Pilek"])
        simpan_ke_csv(data, filename)
        self.assertTrue(os.path.exists(filename))

    def tearDown(self):
        if os.path.exists("test_unit.csv"):
            os.remove("test_unit.csv")


# ---------- LOAD TESTING ----------
def test_load_simpan_ke_csv():
    print("\n[LOAD TEST] Menyimpan 1000 data...")
    start = time.time()
    for i in range(1000):
        data = buat_data_riwayat(f"User{i}", "Dewasa", ["demam"], ["flu"])
        simpan_ke_csv(data, "load_test_output.csv")
    end = time.time()
    print(f"Waktu eksekusi: {end - start:.2f} detik")
    os.remove("load_test_output.csv")


# ---------- STRESS TESTING ----------
def test_stress_input():
    print("\n[STRESS TEST] Input data berukuran sangat besar...")
    try:
        long_string = "X" * 10**6
        data = buat_data_riwayat(long_string, "Dewasa", ["flu"], ["pilek"])
        simpan_ke_csv(data, "stress_test.csv")
        print("Stress test berhasil tanpa error.")
        os.remove("stress_test.csv")
    except Exception as e:
        print(f"Stress test gagal: {e}")


# ---------- INTEGRATION TESTING ----------
def test_integration_create_and_save():
    print("\n[INTEGRATION TEST] Buat data → Simpan ke file")
    data = buat_data_riwayat("IntegrationTest", "Dewasa", ["batuk"], ["asma"])
    simpan_ke_csv(data, "integration_test.csv")
    with open("integration_test.csv", "r") as file:
        lines = file.readlines()
        assert any("IntegrationTest" in line for line in lines), "Data tidak ditemukan dalam file."
    print("Integration test berhasil.")
    os.remove("integration_test.csv")


if __name__ == '__main__':
    unittest.main(exit=False)
    test_load_simpan_ke_csv()
    test_stress_input()
    test_integration_create_and_save()
