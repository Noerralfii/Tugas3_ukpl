import csv
import os
import datetime

def simpan_ke_csv(data, filename="riwayat_diagnosa.csv"):
    try:
        file_exists = os.path.exists(filename)
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["waktu", "nama", "jenis", "gejala", "hasil"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"Gagal menyimpan: {e}")


def buat_data_riwayat(nama, jenis, gejala, hasil):
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "waktu": waktu,
        "nama": nama,
        "jenis": jenis,
        "gejala": ", ".join(gejala),
        "hasil": ", ".join(hasil)
    }

