from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# --- KONFIGURASI APLIKASI ---
app = Flask(__name__)
# Kunci rahasia untuk enkripsi session agar data user tidak bisa dimanipulasi
app.secret_key = 'kunci_rahasia_sekolah'
# Nama file database yang akan menyimpan data berita dan pengumuman
DB_NAME = 'sekolah.db'

# --- FUNGSI DATABASE ---
def inisialisasi_db():
    # Menghubungkan ke file database (jika belum ada, akan dibuat otomatis)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Membuat tabel untuk menyimpan berita
    cursor.execute('''CREATE TABLE IF NOT EXISTS berita 
                      (id INTEGER PRIMARY KEY, judul TEXT, tanggal TEXT, isi TEXT, gambar TEXT)''')
    # Membuat tabel untuk menyimpan pengumuman
    cursor.execute('''CREATE TABLE IF NOT EXISTS pengumuman 
                      (id INTEGER PRIMARY KEY, kategori TEXT, isi TEXT)''')
    conn.commit()
    conn.close()

def get_pengumuman():
    # Mengambil semua daftar pengumuman untuk ditampilkan di halaman depan
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    pengumuman = conn.execute('SELECT * FROM pengumuman ORDER BY id DESC').fetchall()
    conn.close()
    return pengumuman

# --- ROUTES (HALAMAN WEBSITE) ---

@app.route('/')
def home():
    # Menampilkan halaman utama (Beranda) dengan data berita dan pengumuman
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    berita = conn.execute('SELECT * FROM berita ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', sekolah="UPT SMP NEGERI 1 PATAMPANUA", 
                           berita=berita, pengumuman=get_pengumuman())

@app.route('/berita')
def halaman_berita():
    # Menampilkan daftar semua berita yang sudah diunggah
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    berita = conn.execute('SELECT * FROM berita ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('semua_berita.html', berita=berita, pengumuman=get_pengumuman())

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Menangani proses login admin
    if request.method == 'POST':
        # Cek apakah username dan password cocok dengan data hardcoded
        if request.form.get('username') == 'admin' and request.form.get('password') == '123admin123':
            session['logged_in'] = True # Menandai bahwa sesi admin sudah aktif
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Halaman khusus admin untuk menambah berita baru
    if not session.get('logged_in'):
        return redirect(url_for('login')) # Jika belum login, lempar ke halaman login
    
    if request.method == 'POST':
        # Mengambil input dari form admin
        judul = request.form.get('judul')
        tanggal = request.form.get('tanggal')
        isi = request.form.get('isi')
        gambar = request.form.get('gambar')
        
        # Simpan data ke database jika input tidak kosong
        if judul and isi:
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO berita (judul, tanggal, isi, gambar) VALUES (?, ?, ?, ?)", 
                         (judul, tanggal, isi, gambar))
            conn.commit()
            conn.close()
            return redirect(url_for('halaman_berita'))
    return render_template('admin.html')

@app.route('/hapus_berita/<int:id>')
def hapus_berita(id):
    # Fungsi untuk menghapus berita berdasarkan ID
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_NAME)
    conn.execute('DELETE FROM berita WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('halaman_berita'))

# --- PENGUMUMAN ---

@app.route('/tambah_pengumuman', methods=['GET', 'POST'])
def tambah_pengumuman():
    # Menambah pengumuman baru melalui form admin
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        kategori = request.form.get('kategori')
        isi = request.form.get('isi')
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO pengumuman (kategori, isi) VALUES (?, ?)", (kategori, isi))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('tambah_pengumuman.html')

@app.route('/hapus_pengumuman/<int:id>')
def hapus_pengumuman(id):
    # Menghapus pengumuman berdasarkan ID
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_NAME)
    conn.execute('DELETE FROM pengumuman WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# --- AKSI UMUM & START SERVER ---

@app.route('/logout')
def logout():
    # Menghapus sesi login admin
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/visi_misi')
def visi_misi():
    return render_template('visi_misi.html')

@app.route('/sippn')
def sippn():
    return render_template('sippn.html')

if __name__ == '__main__':
    # Menjalankan database dan memulai aplikasi Flask
    inisialisasi_db()
    app.run(debug=True)