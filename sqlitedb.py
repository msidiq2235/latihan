import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Koneksi SQLite
conn = sqlite3.connect('nilai_siswa.db')  # Membuat atau membuka database SQLite
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nama_siswa TEXT,                       
    biologi INTEGER,                       
    fisika INTEGER,                        
    inggris INTEGER,                       
    prediksi_fakultas TEXT                 
)
''')
conn.commit()  # Menyimpan perubahan di database

# Fungsi untuk memproses input dan memberikan prediksi
def hasil_prediksi():
    try:
        # Mengambil input dari pengguna
        nama = nama_entry.get()  # Nama siswa
        biologi = int(biologi_entry.get())  # Nilai Biologi
        fisika = int(fisika_entry.get())  # Nilai Fisika
        inggris = int(inggris_entry.get())  # Nilai Inggris

        # Validasi nilai
        if not (0 <= biologi <= 100 and 0 <= fisika <= 100 and 0 <= inggris <= 100):
            raise ValueError("Nilai harus antara 0 dan 100.")  # Memastikan nilai di rentang 0-100
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")  # Memastikan nama tidak kosong
        
        # Prediksi Fakultas berdasarkan nilai tertinggi
        if biologi > fisika and biologi > inggris:
            fakultas = "Kedokteran"
        elif fisika > biologi and fisika > inggris:
            fakultas = "Teknik"
        elif inggris > biologi and inggris > fisika:
            fakultas = "Bahasa"
        else:
            fakultas = "Tidak Dapat Ditentukan (Nilai Sama)"  # Jika ada nilai yang sama tertinggi

        # Menyimpan data ke database SQLite
        cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
        ''', (nama, biologi, fisika, inggris, fakultas))
        conn.commit()  # Menyimpan perubahan

        # Menampilkan hasil prediksi pada label
        hasil_label.config(text=f"Prodi Pilihan: {fakultas}")
        messagebox.showinfo("Sukses", "Data berhasil disimpan dan diproses!")  # Dialog sukses

        # Memperbarui tampilan data di tabel
        tampilkan_data()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))  # Menampilkan pesan error jika validasi gagal

# Fungsi untuk menampilkan data dari database ke Treeview
def tampilkan_data():
    # Hapus semua data dari Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Ambil data dari database
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()

    # Masukkan data ke Treeview
    for row in rows:
        tree.insert("", "end", values=row)

# GUI
root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")  # Judul aplikasi
root.geometry("600x600")  # Ukuran jendela
root.configure(bg="#800000")  # Warna latar belakang

# Judul aplikasi
judul_label = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 16, "bold"), bg="#800000", fg="white")
judul_label.pack(pady=10)

# Frame untuk form input
frame = tk.Frame(root, bg="#800000")
frame.pack(pady=10)

# Input nama siswa
tk.Label(frame, text="Nama Siswa:", bg="#800000", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
nama_entry = tk.Entry(frame)
nama_entry.grid(row=0, column=1, padx=5, pady=5)

# Input nilai Biologi
tk.Label(frame, text="Nilai Biologi:", bg="#800000", fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
biologi_entry = tk.Entry(frame)
biologi_entry.grid(row=1, column=1, padx=5, pady=5)

# Input nilai Fisika
tk.Label(frame, text="Nilai Fisika:", bg="#800000", fg="white").grid(row=2, column=0, sticky="w", padx=5, pady=5)
fisika_entry = tk.Entry(frame)
fisika_entry.grid(row=2, column=1, padx=5, pady=5)

# Input nilai Inggris
tk.Label(frame, text="Nilai Inggris:", bg="#800000", fg="white").grid(row=3, column=0, sticky="w", padx=5, pady=5)
inggris_entry = tk.Entry(frame)
inggris_entry.grid(row=3, column=1, padx=5, pady=5)

# Tombol Submit
submit_button = tk.Button(root, text="Submit", command=hasil_prediksi, bg="#FFFFFF", fg="#800000")
submit_button.pack(pady=20)

# Label untuk menampilkan hasil prediksi
hasil_label = tk.Label(root, text="Prodi Pilihan: ", font=("Arial", 12), bg="#800000", fg="white")
hasil_label.pack(pady=10)

# Frame untuk tabel Treeview
tabel_frame = tk.Frame(root)
tabel_frame.pack(pady=20)

# Membuat Treeview untuk menampilkan data
tree = ttk.Treeview(tabel_frame, columns=("ID", "Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi Fakultas"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama Siswa", text="Nama Siswa")
tree.heading("Biologi", text="Biologi")
tree.heading("Fisika", text="Fisika")
tree.heading("Inggris", text="Inggris")
tree.heading("Prediksi Fakultas", text="Prediksi Fakultas")

# Mengatur lebar kolom dan posisi teks
tree.column("ID", width=30, anchor="center")
tree.column("Nama Siswa", width=150)
tree.column("Biologi", width=60, anchor="center")
tree.column("Fisika", width=60, anchor="center")
tree.column("Inggris", width=60, anchor="center")
tree.column("Prediksi Fakultas", width=120)

tree.pack()

# Menampilkan data awal dari database
tampilkan_data()

# Menjalankan aplikasi
root.mainloop()
