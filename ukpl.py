import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import csv
import os

# Basis pengetahuan sederhana 
penyakit_db = {
    "Gastritis": ["muntah", "tidak mau makan", "lemas"],
    "Konjungtivitis": ["mata merah", "keluar air mata"],
    "Flu": ["batuk", "pilek", "demam"],
    "Cacingan": ["perut buncit", "berat badan turun", "lemas"],
    "Kulit Jamuran": ["bulu rontok", "kulit bersisik", "gatal"]
}

riwayat_diagnosa = []

def diagnosa(gejala_terpilih):
    hasil = []
    for penyakit, gejala in penyakit_db.items():
        if all(g in gejala_terpilih for g in gejala):
            hasil.append(penyakit)
        elif any(g in gejala_terpilih for g in gejala):
            hasil.append(penyakit + " (kemungkinan)")
    return hasil if hasil else ["Tidak diketahui, konsultasikan ke dokter hewan"]

def proses_diagnosa():
    nama_hewan = entry_nama.get().strip()
    jenis_hewan = combo_jenis.get().strip()
    gejala_terpilih = [g for g, var in gejala_vars.items() if var.get() == 1]

    if not nama_hewan or not jenis_hewan:
        messagebox.showwarning("Peringatan", "Isi nama dan jenis hewan terlebih dahulu")
        return
    if not gejala_terpilih:
        messagebox.showwarning("Peringatan", "Pilih minimal satu gejala")
        return

    hasil = diagnosa(gejala_terpilih)
    output_text.set("\n".join(hasil))

    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "waktu": waktu,
        "nama": nama_hewan,
        "jenis": jenis_hewan,
        "gejala": ", ".join(gejala_terpilih),
        "hasil": ", ".join(hasil)
    }
    riwayat_diagnosa.append(data)
    update_riwayat()
    simpan_ke_csv(data)
    reset_form()

def update_riwayat():
    text_riwayat.delete("1.0", tk.END)
    for r in riwayat_diagnosa:
        teks = f"[{r['waktu']}] {r['nama']} ({r['jenis']}): {r['hasil']}\n"
        text_riwayat.insert(tk.END, teks)

def simpan_ke_csv(data):
    try:
        file_exists = os.path.exists("riwayat_diagnosa.csv")
        with open("riwayat_diagnosa.csv", mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["waktu", "nama", "jenis", "gejala", "hasil"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        messagebox.showerror("Gagal Simpan", f"Terjadi kesalahan saat menyimpan data: {e}")

def reset_form():
    entry_nama.delete(0, tk.END)
    combo_jenis.set('')
    for var in gejala_vars.values():
        var.set(0)

def show_about():
    messagebox.showinfo("Tentang", "Aplikasi Diagnosa Penyakit Hewan v1.0\nProgram ini dibuat untuk membantu mendiagnosa penyakit pada hewan peliharaan seperti kucing dan anjing.\n\nPengembang:ahli klimatologi\nEmail:ari@gmail.com")

# GUI setup
root = tk.Tk()
root.title("Diagnosa Penyakit Kucing & Anjing")
root.geometry("550x720")

# Menu bar
menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Tentang", command=show_about)
menu_bar.add_cascade(label="Bantuan", menu=help_menu)
root.config(menu=menu_bar)

judul = tk.Label(root, text=" Diagnosa Penyakit Hewan Kucing dan Anjing", font=("Arial", 14, "bold"))
judul.pack(pady=10)

frame_info = tk.Frame(root)
frame_info.pack(pady=5)

lbl_nama = tk.Label(frame_info, text="Nama Hewan:")
lbl_nama.grid(row=0, column=0, sticky='w')
entry_nama = tk.Entry(frame_info, width=30)
entry_nama.grid(row=0, column=1, padx=5)

lbl_jenis = tk.Label(frame_info, text="Jenis Hewan:")
lbl_jenis.grid(row=1, column=0, sticky='w')
combo_jenis = ttk.Combobox(frame_info, values=["Kucing", "Anjing"], state="readonly", width=27)
combo_jenis.grid(row=1, column=1, padx=5)

lbl_gejala = tk.Label(root, text="Pilih Gejala yang Dialami:", font=("Arial", 12))
lbl_gejala.pack(pady=10)

frame_gejala = tk.Frame(root)
frame_gejala.pack()

gejala_list = list(set(g for gejala in penyakit_db.values() for g in gejala))
gejala_list.sort()
gejala_vars = {}

# Gejala dalam 2 kolom
for idx, gejala in enumerate(gejala_list):
    var = tk.IntVar()
    cb = tk.Checkbutton(frame_gejala, text=gejala, variable=var)
    cb.grid(row=idx // 2, column=idx % 2, sticky='w', padx=5, pady=2)
    gejala_vars[gejala] = var

tombol = tk.Button(root, text="Diagnosa", command=proses_diagnosa, bg="orange")
tombol.pack(pady=10)

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, wraplength=450, justify="left", font=("Arial", 12), fg="blue")
output_label.pack(pady=10)

frame_riwayat = tk.LabelFrame(root, text="Riwayat Diagnosa", font=("Arial", 11))
frame_riwayat.pack(fill="both", expand=True, padx=10, pady=10)

text_riwayat = tk.Text(frame_riwayat, height=10, wrap="word")
text_riwayat.pack(fill="both", expand=True, padx=5, pady=5)

root.mainloop()
