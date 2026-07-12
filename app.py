from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = 'sekolah.db'

def inisialisasi_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS berita (id INTEGER PRIMARY KEY, judul TEXT, tanggal TEXT, isi TEXT, gambar TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pengumuman (id INTEGER PRIMARY KEY, kategori TEXT, isi TEXT)''')
    
    if cursor.execute('SELECT COUNT(*) FROM berita').fetchone()[0] == 0:
        data_berita = [
            ('Prestasi Gemilang Tim Pramuka', '05 April 2026', 'Isi berita pramuka...', 'pramuka.jpeg'),
            ('Pelaksanaan Simulasi ANBK 2026', '24 Juni 2026', 'Isi berita ANBK...', 'anbk.jpeg')
        ]
        cursor.executemany("INSERT INTO berita (judul, tanggal, isi, gambar) VALUES (?, ?, ?, ?)", data_berita)
    
    if cursor.execute('SELECT COUNT(*) FROM pengumuman').fetchone()[0] == 0:
        data_pengumuman = [
            ('Info', 'Pendaftaran PPDB telah dibuka.'),
            ('Info', 'Jadwal libur semester genap dimulai pada tanggal 29 Juli 2026 sampai tanggal 12 Juli 2026.'),
            ('Info', 'Pengambilan rapor siswa kelas 7 dan 8 dilakukan tanggal 27 Juli 2026.')
        ]
        cursor.executemany("INSERT INTO pengumuman (kategori, isi) VALUES (?, ?)", data_pengumuman)
    
    conn.commit()
    conn.close()

def get_pengumuman():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    pengumuman = conn.execute('SELECT * FROM pengumuman ORDER BY id DESC').fetchall()
    conn.close()
    return pengumuman

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    berita = conn.execute('SELECT * FROM berita ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', sekolah="UPT SMP NEGERI 1 PATAMPANUA", slogan="Mewujudkan Generasi Cerdas dan Berakhlak", berita=berita, pengumuman=get_pengumuman())

@app.route('/visi_misi')
def visi_misi():
    return render_template('visi_misi.html', sekolah="UPT SMP NEGERI 1 PATAMPANUA", slogan="Mewujudkan Generasi Cerdas dan Berakhlak", pengumuman=get_pengumuman())

@app.route('/berita')
def halaman_berita():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    berita = conn.execute('SELECT * FROM berita ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('semua_berita.html', berita=berita, sekolah="UPT SMP NEGERI 1 PATAMPANUA", slogan="Mewujudkan Generasi Cerdas dan Berakhlak", pengumuman=get_pengumuman())

# --- TAMBAHAN ROUTE SIPPN ---
@app.route('/sippn')
def sippn():
    return render_template('sippn.html', 
                           sekolah="UPT SMP NEGERI 1 PATAMPANUA", 
                           slogan="Mewujudkan Generasi Cerdas dan Berakhlak",
                           pengumuman=get_pengumuman())

if __name__ == '__main__':
    inisialisasi_db()
    app.run(debug=True)