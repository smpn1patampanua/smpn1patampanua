from flask import Flask, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def inisialisasi_database():
    koneksi = sqlite3.connect('sekolah.db')
    cursor = koneksi.cursor()
    
    # Membuat tabel berita
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS berita (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            isi TEXT NOT NULL,
            gambar TEXT
        )
    ''')
    
    # Membuat tabel pengumuman
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pengumuman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT NOT NULL,
            isi TEXT NOT NULL
        )
    ''')
    
    # ISI BERITA BARU (VERSI PANJANG DAN LENGKAP BERPARAGRAF)
    cursor.execute("SELECT COUNT(*) FROM berita")
    if cursor.fetchone()[0] == 0:
        # 1. Berita ANBK (Versi Lengkap)
        cursor.execute('''
            INSERT INTO berita (judul, tanggal, isi, gambar) 
            VALUES (
                'Pelaksanaan Simulasi ANBK 2026', 
                '24 Juni 2026', 
                'Dalam rangka menguji kesiapan teknis dan mental peserta didik, UPT SMP Negeri 1 Patampanua menggelar kegiatan simulasi Asesmen Nasional Berbasis Komputer (ANBK) tahun ajaran 2025/2026.\n\nKegiatan simulasi ini diikuti oleh seluruh siswa kelas 8 yang terbagi ke dalam beberapa sesi pengerjaan. Laboratorium komputer sekolah telah disiapkan secara matang dengan total 30 unit komputer yang terhubung ke jaringan internet stabil. Kepala sekolah menyampaikan bahwa simulasi ini sangat penting untuk meminimalisir kendala teknis seperti masalah login atau jaringan pada saat hari pelaksanaan ujian utama nanti.\n\nSelama simulasi berlangsung, para siswa tampak antusias and fokus mengerjakan soal-soal literasi serta numerasi. Proktor dan teknisi sekolah juga bersiaga penuh di dalam ruangan untuk memastikan seluruh proses berjalan tanpa hambatan berarti.', 
                'ANBK.jpeg'
            )
        ''')
        
        # 2. Berita Pramuka (Versi Lengkap)
        cursor.execute('''
            INSERT INTO berita (judul, tanggal, isi, gambar) 
            VALUES (
                'Prestasi Gemilang Tim Pramuka', 
                '05 April 2026', 
                'Prestasi gemilang di bulan April! Selamat atas keberhasilan siswa-siswi terbaik UPT SMP Negeri 1 Patampanua yang berhasil menyabet peringkat ke-3 dalam ajang Lomba Parade Semaphore di SMK Negeri 1 Pinrang. Penampilan yang kompak, penuh percaya diri, dan khidmat di arena perlombaan telah membuahkan hasil yang membanggakan. Terima kasih telah berjuang dengan sportivitas tinggi, kalian adalah kebanggaan kami semua!', 
                'pramuka.jpeg'
            )
        ''')
        
                 # 3. Berita PPDB (Versi Lengkap)
        cursor.execute('''
            INSERT INTO berita (judul, tanggal, isi, gambar) 
            VALUES (
                'Penuh Kekhidmatan, PPDB UPT SMP Negeri 1 Patampanua Sambut Generasi Emas', 
                '13 Mei 2026', 
                'Pelaksanaan Penerimaan Peserta Didik Baru (PPDB) di UPT SMP Negeri 1 Patampanua pada Rabu (13/5) berlangsung sangat khidmat dan tertib. Sejak pagi, antusiasme besar dari orang tua calon peserta didik disambut dengan pelayanan yang ramah, profesional, dan transparan oleh panitia.\n\nSinergi yang harmonis dan penuh kekeluargaan ini menciptakan suasana pendaftaran yang sejuk dan religius. Kelancaran kegiatan hari ini mencerminkan dedikasi tinggi seluruh warga sekolah. Momentum ini menjadi langkah awal yang optimis bagi UPT SMP Negeri 1 Patampanua dalam berkomitmen mencetak generasi masa depan yang cerdas, berkarakter, dan berakhlak mulia.', 
                'ppdb1.jpeg'
            )
        ''')

    # Isi data pengumuman awal
    cursor.execute("SELECT COUNT(*) FROM pengumuman")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pengumuman (kategori, isi) VALUES ('PPDB 2026', 'Pendaftaran Jalur Zonasi segera dibuka bulan Juli ini.')")
        cursor.execute("INSERT INTO pengumuman (kategori, isi) VALUES ('MPLS 2026', 'Kegiatan MPLS 2026 akan dimulai pada tanggal 13 sampai 18 Juli 2026.')")
        cursor.execute("INSERT INTO pengumuman (kategori, isi) VALUES ('Libur Sekolah', 'Libur semester genap dimulai tanggal 29 sampai 12 juli 2026.')")
        
    koneksi.commit()
    koneksi.close()

@app.route('/')
def home():
    koneksi = sqlite3.connect('sekolah.db')
    koneksi.row_factory = sqlite3.Row
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM berita ORDER BY id DESC")
    semua_berita = cursor.fetchall()
    cursor.execute("SELECT * FROM pengumuman ORDER BY id DESC")
    semua_pengumuman = cursor.fetchall()
    koneksi.close()
    
    nama_sekolah = "UPT SMP NEGERI 1 PATAMPANUA"
    tagline = "BERIMAN, BERILMU, BERBUDAYA DAN BERWAWASAN LINGKUNGAN"
    tahun_sekarang = datetime.now().year
    
    return render_template('index.html', sekolah=nama_sekolah, slogan=tagline, berita=semua_berita, pengumuman=semua_pengumuman, tahun=tahun_sekarang)

@app.route('/berita/<int:id_berita>')
def detail_berita(id_berita):
    koneksi = sqlite3.connect('sekolah.db')
    koneksi.row_factory = sqlite3.Row
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM berita WHERE id = ?", (id_berita,))
    berita_terpilih = cursor.fetchone()
    koneksi.close()
    
    if berita_terpilih is None:
        return "Berita tidak ditemukan!", 404
        
    nama_sekolah = "UPT SMP NEGERI 1 PATAMPANUA"
    tagline = "BERIMAN, BERILMU, BERBUDAYA DAN BERWAWASAN LINGKUNGAN"
    tahun_sekarang = datetime.now().year
    
    return render_template('detail.html', sekolah=nama_sekolah, slogan=tagline, berita=berita_terpilih, tahun=tahun_sekarang)

@app.route('/berita')
def halaman_semua_berita():
    koneksi = sqlite3.connect('sekolah.db')
    koneksi.row_factory = sqlite3.Row
    cursor = koneksi.cursor()
    
    # 1. Ambil data berita
    cursor.execute("SELECT * FROM berita ORDER BY id DESC")
    semua_berita = cursor.fetchall()
    
    # 2. Ambil data pengumuman
    cursor.execute("SELECT * FROM pengumuman ORDER BY id DESC")
    semua_pengumuman = cursor.fetchall()
    
    koneksi.close()
    
    nama_sekolah = "UPT SMP NEGERI 1 PATAMPANUA"
    tagline = "BERIMAN, BERILMU, BERBUDAYA DAN BERWAWASAN LINGKUNGAN"
    tahun_sekarang = datetime.now().year
    
    return render_template('semua_berita.html', sekolah=nama_sekolah, slogan=tagline, berita=semua_berita, pengumuman=semua_pengumuman, tahun=tahun_sekarang)


@app.route('/visi-misi')
def visi_misi():
    # PERBAIKAN DI SINI: Mengambil data pengumuman resmi dari database sqlite
    koneksi = sqlite3.connect('sekolah.db')
    koneksi.row_factory = sqlite3.Row
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM pengumuman ORDER BY id DESC")
    semua_pengumuman = cursor.fetchall()
    koneksi.close()
    
    nama_sekolah = "UPT SMP NEGERI 1 PATAMPANUA"
    tagline = "BERIMAN, BERILMU, BERBUDAYA DAN BERWAWASAN LINGKUNGAN"
    tahun_sekarang = datetime.now().year
    
    return render_template('visi_misi.html', 
                           sekolah=nama_sekolah, 
                           slogan=tagline,
                           pengumuman=semua_pengumuman, 
                           tahun=tahun_sekarang)

if __name__ == '__main__':
    if os.path.exists('sekolah.db'):
        try: os.remove('sekolah.db')
        except: pass
    inisialisasi_database()
    app.run(debug=True)