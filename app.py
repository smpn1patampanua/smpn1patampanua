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
                'PGRI.jpg'
            )
        ''')
        
        # 2. Berita Pramuka (Versi Lengkap)
        cursor.execute('''
            INSERT INTO berita (judul, tanggal, isi, gambar) 
            VALUES (
                'Prestasi Gemilang Tim Pramuka', 
                '20 Juni 2026', 
                'Kabar membanggakan kembali datang dari dunia ekstrakurikuler sekolah. Tim Pramuka pangkalan UPT SMP Negeri 1 Patampanua berhasil mengukir prestasi gemilang dengan meraih gelar Juara Umum pada ajang Perkemahan Bakti Tingkat Daerah yang diselenggarakan pekan ini.\n\nDalam kompetisi yang diikuti oleh puluhan sekolah tersebut, tim regu putra dan putri SMPN 1 Patampanua sukses mendominasi berbagai cabang lomba, mulai dari lomba ketangkasan baris-berbaris (LKBB), pionering, hingga lomba sandi dan semaphore. Keberhasilan ini merupakan buah dari latihan keras dan disiplin tinggi yang dijalani para siswa selama dua bulan terakhir di bawah bimbingan para pembina Pramuka.\n\nPihak sekolah menyampaikan apresiasi yang setinggi-tingginya atas dedikasi dan semangat juang para siswa. Piala bergilir Juara Umum kini resmi dipajang di ruang piala sekolah sebagai simbol motivasi bagi seluruh peserta didik lainnya.', 
                'pramuka.jpg'
            )
        ''')
        
        # 3. Berita Rapat Kelulusan (Versi Lengkap)
        cursor.execute('''
            INSERT INTO berita (judul, tanggal, isi, gambar) 
            VALUES (
                'Rapat Kelulusan Siswa Kelas 9', 
                '25 Juni 2026', 
                'Dewan guru beserta jajaran staf UPT SMP Negeri 1 Patampanua telah selesai menggelar rapat pleno tertutup terkait evaluasi akhir dan penentuan kelulusan bagi siswa kelas 9 Tahun Ajaran 2025/2026.\n\nRapat yang dipimpin langsung oleh Kepala Sekolah ini berfokus pada penilaian akumulatif siswa, mencakup aspek akademis, nilai ujian sekolah, hingga penilaian karakter dan kehadiran selama tiga tahun menempuh pendidikan. Berdasarkan hasil musyawarah mufakat, dewan guru merumuskan keputusan akhir yang objektif demi masa depan kelanjutan studi para siswa ke jenjang SMA/SMK sederajat.\n\nPengumuman resmi kelulusan rencananya akan dipublikasikan secara daring melalui portal resmi ini pada tanggal yang telah ditentukan, guna menghindari kerumunan siswa di lingkungan sekolah.', 
                'mengecat.jpg'
            )
        ''')
        
    # Isi data pengumuman awal
    cursor.execute("SELECT COUNT(*) FROM pengumuman")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pengumuman (kategori, isi) VALUES ('PPDB 2026', 'Pendaftaran Jalur Zonasi segera dibuka bulan Juli ini.')")
        cursor.execute("INSERT INTO pengumuman (kategori, isi) VALUES ('ANBK 2026', 'Simulasi utama untuk kelas 8 akan dilaksanakan pekan depan.')")
        cursor.execute("INSERT INTO pengumuman (kategori, isi) VALUES ('Libur Sekolah', 'Libur semester genap dimulai tanggal 29 Juni hingga 12 Juli 2026.')")
        
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
    
    nama_sekolah = "MASIH UJI COBA"
    tagline = "Cerdas, Berkarakter, dan Berteknologi"
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
        
    nama_sekolah = "MASIH UJI COBA"
    tagline = "Cerdas, Berkarakter, dan Berteknologi"
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
    
    nama_sekolah = "MASIH UJI COBA"
    tagline = "Cerdas, Berkarakter, dan Berteknologi"
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
    
    nama_sekolah = "MASIH UJI COBA"
    tagline = "Cerdas, Berkarakter, dan Berteknologi"
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