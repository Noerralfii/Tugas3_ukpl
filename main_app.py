import tkinter as tk
from tkinter import messagebox, ttk
from diagnosa import diagnosa, get_all_gejala
from utils import simpan_ke_csv, buat_data_riwayat
import os

riwayat_diagnosa = []

def proses_diagnosa():
    nama_hewan = entry_nama.get().strip()
    jenis_hewan = combo_jenis.get().strip()
    gejala_dari_checkbox = [g for g, var in gejala_vars.items() if var.get() == 1]
    gejala_dari_manual = [g.strip() for g in entry_gejala_manual.get().split(",") if g.strip()]
    gejala_valid = get_all_gejala()

    # Validasi input
    if not nama_hewan or not jenis_hewan:
        messagebox.showwarning("Peringatan", "Isi nama dan jenis hewan terlebih dahulu")
        return

    gejala_tidak_valid = [g for g in gejala_dari_manual if g not in gejala_valid]
    if gejala_tidak_valid:
        messagebox.showerror("Error", f"Gejala tidak valid: {', '.join(gejala_tidak_valid)}")
        return

    # Gabungkan gejala tanpa duplikat
    gejala_terpilih = list(dict.fromkeys(gejala_dari_checkbox + gejala_dari_manual))
    if not gejala_terpilih:
        messagebox.showwarning("Peringatan", "Pilih atau ketik minimal satu gejala")
        return

    hasil = diagnosa(gejala_terpilih)
    output_text.set("\n".join(hasil))

    data = buat_data_riwayat(nama_hewan, jenis_hewan, gejala_terpilih, hasil)
    riwayat_diagnosa.append(data)
    simpan_ke_csv(data)
    update_riwayat()
    reset_form()

def update_riwayat():
    text_riwayat.delete("1.0", tk.END)
    if os.path.exists("riwayat_diagnosa.csv"):
        with open("riwayat_diagnosa.csv", "r") as file:
            lines = file.readlines()
            if len(lines) <= 1:
                text_riwayat.insert(tk.END, "Belum ada riwayat diagnosa.")
            else:
                for line in lines:
                    text_riwayat.insert(tk.END, line)
    else:
        text_riwayat.insert(tk.END, "Belum ada riwayat diagnosa.")

def filter_riwayat():
    keyword = entry_filter.get().strip().lower()
    text_riwayat.delete("1.0", tk.END)

    if not keyword:
        update_riwayat()
        return

    if not os.path.exists("riwayat_diagnosa.csv"):
        return

    with open("riwayat_diagnosa.csv", "r") as file:
        lines = file.readlines()
        header = lines[0]
        data = lines[1:]
        filtered = [line for line in data if keyword in line.lower()]

        if filtered:
            text_riwayat.insert(tk.END, header)
            for line in filtered:
                text_riwayat.insert(tk.END, line)
        else:
            text_riwayat.insert(tk.END, "Tidak ditemukan riwayat yang sesuai.\n")

def reset_form():
    entry_nama.delete(0, tk.END)
    combo_jenis.set('')
    entry_gejala_manual.delete(0, tk.END)
    for var in gejala_vars.values():
        var.set(0)

def show_about():
    messagebox.showinfo("Tentang", "Aplikasi Diagnosa Penyakit Hewan v2.0\nPengembang: ahli klimatologi\nEmail: ari@gmail.com")

# Login Window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

def login():
    if entry_user.get() == "213" and entry_pass.get() == "213":
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Login Gagal", "Username atau Password salah")

tk.Label(login_window, text="Login", font=("Arial", 12, "bold")).pack(pady=10)
frame_login = tk.Frame(login_window)
frame_login.pack()

entry_user = tk.Entry(frame_login)
entry_pass = tk.Entry(frame_login, show="*")

tk.Label(frame_login, text="Username:").grid(row=0, column=0)
tk.Label(frame_login, text="Password:").grid(row=1, column=0)
entry_user.grid(row=0, column=1)
entry_pass.grid(row=1, column=1)

tk.Button(login_window, text="Login", command=login, bg="orange").pack(pady=10)

# Main App
def main_app():
    global entry_nama, combo_jenis, gejala_vars, output_text, text_riwayat, entry_gejala_manual, entry_filter

    root = tk.Tk()
    root.title("Sistem Diagnosa Penyakit Hewan - v2.0")
    root.geometry("600x750")

    menu_bar = tk.Menu(root)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Tentang", command=show_about)
    menu_bar.add_cascade(label="Bantuan", menu=help_menu)
    root.config(menu=menu_bar)

    tk.Label(root, text="Diagnosa Penyakit Kucing & Anjing", font=("Arial", 14, "bold")).pack(pady=10)

    frame_info = tk.Frame(root)
    frame_info.pack(pady=5)

    tk.Label(frame_info, text="Nama Hewan:").grid(row=0, column=0, sticky='w')
    entry_nama = tk.Entry(frame_info, width=30)
    entry_nama.grid(row=0, column=1)

    tk.Label(frame_info, text="Jenis Hewan:").grid(row=1, column=0, sticky='w')
    combo_jenis = ttk.Combobox(frame_info, values=["Kucing", "Anjing"], state="readonly", width=27)
    combo_jenis.grid(row=1, column=1)

    tk.Label(root, text="Pilih Gejala:", font=("Arial", 12)).pack(pady=10)
    frame_gejala = tk.Frame(root)
    frame_gejala.pack()

    gejala_vars = {}
    for idx, gejala in enumerate(get_all_gejala()):
        var = tk.IntVar()
        cb = tk.Checkbutton(frame_gejala, text=gejala, variable=var)
        cb.grid(row=idx // 2, column=idx % 2, sticky='w')
        gejala_vars[gejala] = var

    tk.Label(root, text="Atau Ketik Gejala Manual (pisahkan dengan koma):").pack()
    entry_gejala_manual = tk.Entry(root, width=60)
    entry_gejala_manual.pack(pady=5)

    tk.Button(root, text="Diagnosa", command=proses_diagnosa, bg="orange").pack(pady=10)

    output_text = tk.StringVar()
    tk.Label(root, textvariable=output_text, wraplength=500, justify="left", font=("Arial", 12), fg="blue").pack(pady=10)

    frame_riwayat = tk.LabelFrame(root, text="Riwayat Diagnosa", font=("Arial", 11))
    frame_riwayat.pack(fill="both", expand=True, padx=10, pady=10)

    text_riwayat = tk.Text(frame_riwayat, height=10, wrap="word")
    text_riwayat.pack(fill="both", expand=True, padx=5, pady=5)

    frame_filter = tk.Frame(root)
    frame_filter.pack(pady=5)
    tk.Label(frame_filter, text="Filter Riwayat (penyakit/tanggal):").pack(side="left")
    entry_filter = tk.Entry(frame_filter, width=30)
    entry_filter.pack(side="left", padx=5)
    tk.Button(frame_filter, text="Terapkan Filter", command=filter_riwayat).pack(side="left")

    update_riwayat()
    root.mainloop()

login_window.mainloop()
