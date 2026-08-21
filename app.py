from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename

# --- KONFIGURASI APLIKASI ---
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_sekolah'
DB_NAME = 'sekolah.db'

# --- FUNGSI DATABASE ---
def inisialisasi_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS berita 
                      (id INTEGER PRIMARY KEY, judul TEXT, tanggal TEXT, isi TEXT, gambar TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pengumuman 
                      (id INTEGER PRIMARY KEY, kategori TEXT, isi TEXT)''')
    # Tabel baru untuk menyimpan informasi tambahan SIPPN
    cursor.execute('''CREATE TABLE IF NOT EXISTS sippn_info 
                      (id INTEGER PRIMARY KEY, judul TEXT, gambar TEXT)''')
    conn.commit()
    conn.close()

def get_pengumuman():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    pengumuman = conn.execute('SELECT * FROM pengumuman ORDER BY id DESC').fetchall()
    conn.close()
    return pengumuman

# --- ROUTES (HALAMAN WEBSITE) ---

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    berita = conn.execute('SELECT * FROM berita ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', sekolah="UPT SMP NEGERI 1 PATAMPANUA", 
                           berita=berita, pengumuman=get_pengumuman())

@app.route('/berita')
def halaman_berita():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    berita = conn.execute('SELECT * FROM berita ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('semua_berita.html', berita=berita, pengumuman=get_pengumuman())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        judul = request.form.get('judul')
        tanggal = request.form.get('tanggal')
        isi = request.form.get('isi')
        gambar = request.form.get('gambar')
        
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
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_NAME)
    conn.execute('DELETE FROM pengumuman WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# --- SIPPN & TAMBAH INFORMASI SIPPN ---

@app.route('/sippn')
def sippn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    sippn_list = conn.execute('SELECT * FROM sippn_info ORDER BY id ASC').fetchall()
    conn.close()
    return render_template('sippn.html', sippn_list=sippn_list)

@app.route('/tambah_sippn', methods=['GET', 'POST'])
def tambah_sippn():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        judul = request.form.get('judul_info')
        file = request.files.get('gambar_info')
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            os.makedirs('static', exist_ok=True)
            file.save(os.path.join('static', filename))
            
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO sippn_info (judul, gambar) VALUES (?, ?)", (judul, filename))
            conn.commit()
            conn.close()
            return redirect(url_for('sippn'))
            
    return render_template('tambah_sippn.html')

@app.route('/hapus_sippn/<int:id>')
def hapus_sippn(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_NAME)
    conn.execute('DELETE FROM sippn_info WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('sippn'))

# --- AKSI UMUM & START SERVER ---

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/visi_misi')
def visi_misi():
    return render_template('visi_misi.html')

if __name__ == '__main__':
    inisialisasi_db()
    app.run(debug=True)