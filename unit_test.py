import unittest
from diagnosa import diagnosa, get_all_gejala

class TestDiagnosa(unittest.TestCase):

    def test_diagnosa_pasti(self):
        """Semua gejala cocok 100%"""
        gejala = ["muntah", "tidak mau makan", "lemas"]
        hasil = diagnosa(gejala)
        self.assertIn("Gastritis (100%)", hasil)

    def test_diagnosa_kemungkinan_skor(self):
        """Sebagian gejala cocok, tampilkan skor persentase"""
        gejala = ["muntah", "lemas"]  # 2/3 cocok = 67%
        hasil = diagnosa(gejala)
        self.assertTrue(any("Gastritis (67%" in h for h in hasil))

    def test_diagnosa_multiple_match(self):
        """Gejala yang cocok dengan lebih dari satu penyakit"""
        gejala = ["lemas", "batuk"]
        hasil = diagnosa(gejala)
        self.assertTrue(any("Gastritis" in h for h in hasil))
        self.assertTrue(any("Flu" in h for h in hasil))

    def test_diagnosa_tidak_dikenal(self):
        """Gejala tidak cocok dengan penyakit manapun"""
        gejala = ["gejala tidak valid"]
        hasil = diagnosa(gejala)
        self.assertEqual(hasil, ["Tidak diketahui, konsultasikan ke dokter hewan"])

    def test_diagnosa_kosong(self):
        """Jika input gejala kosong, harus muncul pesan tidak diketahui"""
        hasil = diagnosa([])
        self.assertEqual(hasil, ["Tidak diketahui, konsultasikan ke dokter hewan"])

    def test_tidak_ada_duplikat_diagnosa(self):
        """Hasil diagnosa tidak boleh duplikat meskipun input gejala tumpang tindih"""
        gejala = ["batuk", "pilek", "demam", "batuk"]  # 'batuk' dua kali
        hasil = diagnosa(gejala)
        self.assertEqual(len(hasil), len(set(hasil)))  # semua hasil harus unik

    def test_gejala_validasi_manual(self):
        """Gejala manual semuanya valid"""
        gejala_manual = ["mata merah", "keluar air mata"]
        semua_gejala = get_all_gejala()
        for g in gejala_manual:
            self.assertIn(g, semua_gejala)

    def test_gejala_manual_tidak_valid(self):
        """Gejala manual yang tidak ada harus dianggap tidak valid secara manual"""
        semua_gejala = get_all_gejala()
        gejala_manual = ["gatal", "warna bulu berubah"]
        tidak_valid = [g for g in gejala_manual if g not in semua_gejala]
        self.assertIn("warna bulu berubah", tidak_valid)

if __name__ == '__main__':
    unittest.main()
