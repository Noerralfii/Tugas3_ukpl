penyakit_db = {
    "Gastritis": ["muntah", "tidak mau makan", "lemas"],
    "Konjungtivitis": ["mata merah", "keluar air mata"],
    "Flu": ["batuk", "pilek", "demam"],
    "Cacingan": ["perut buncit", "berat badan turun", "lemas"],
    "Kulit Jamuran": ["bulu rontok", "kulit bersisik", "gatal"]
}

def diagnosa(gejala_terpilih):
    hasil = []
    for penyakit, gejala in penyakit_db.items():
        total = len(gejala)
        cocok = sum(1 for g in gejala if g in gejala_terpilih)
        if cocok == total:
            hasil.append(f"{penyakit} (100%)")
        elif cocok > 0:
            persentase = round((cocok / total) * 100)
            hasil.append(f"{penyakit} ({persentase}%)")
    return list(dict.fromkeys(hasil)) if hasil else ["Tidak diketahui, konsultasikan ke dokter hewan"]

def get_all_gejala():
    return sorted(set(g for gejala in penyakit_db.values() for g in gejala))
