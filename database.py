import sqlite3

# Fungsi untuk menyiapkan database dan tabel
def setup_database():
    db = sqlite3.connect("laporan_error.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tiket (nama TEXT, masalah TEXT)")
    db.commit()
    db.close()

# Fungsi untuk menyimpan laporan baru
def simpan_tiket(nama, masalah):
    db = sqlite3.connect("laporan_error.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO tiket (nama, masalah) VALUES (?, ?)", (nama, masalah))
    db.commit()
    db.close()

# Fungsi untuk mengambil semua laporan
def ambil_semua_tiket():
    db = sqlite3.connect("laporan_error.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tiket")
    semua_tiket = cursor.fetchall()
    db.close()
    return semua_tiket
