# Algoritma_Closest_Pair_of_Points_Hasnidar-D082261004-
Analisis Algoritma Closest Pair of Points pada Studi Kasus Penentuan Dua Gedung Kampus Terdekat
Closest Pair of Points: Brute Force vs Divide and Conquer
Tugas Analisis Algoritma Komputasi, Magister Teknik Informatika. Studi kasus: menentukan dua gedung kampus yang paling berdekatan.
Isi repositori
Berkas	Fungsi
closest_pair.py	Seluruh kode: brute force, divide and conquer, uji, eksperimen, studi kasus
eksperimen_tambahan.py	Jumlah perhitungan jarak, uji sebaran titik, uji sensitivitas studi kasus
hasil_eksperimen.csv	Hasil pengukuran waktu (rata-rata dan simpangan baku)
hasil_operasi.csv	Jumlah perhitungan jarak tiap ukuran input
hasil_sebaran.csv	Hasil uji berbagai sebaran titik
hasil_sensitivitas.csv	Hasil uji sensitivitas studi kasus
Pustaka
Tidak ada pustaka eksternal. Algoritma ditulis dari nol, termasuk pembangkit bilangan acak (LCG) dan perhitungan rata-rata serta simpangan baku. Modul bawaan Python yang dipakai hanya time (mengukur waktu) dan math (cos, sin, asin untuk proyeksi koordinat dan Haversine pada studi kasus). Grafik pada laporan dibuat terpisah dengan matplotlib dan tidak diperlukan untuk menjalankan kode ini.
Kebutuhan
Python 3.8 atau lebih baru.
Cara menjalankan
python closest_pair.py uji          # 3 kasus uji manual + 300 uji acak
python closest_pair.py eksperimen   # ukur waktu, simpan ke hasil_eksperimen.csv
python closest_pair.py studi_kasus  # dua gedung kampus terdekat
python eksperimen_tambahan.py       # jumlah operasi, sebaran titik, sensitivitas
Eksperimen memakan waktu sekitar 2 menit (brute force pada n = 10.000 paling lama).
Contoh keluaran (uji)
Kasus 3: pasangan terdekat melintasi garis pembagi
  harapan (hitung manual) : 1.4142
  brute force             : 1.4142 ((4, 3), (5, 4))
  divide and conquer      : 1.4142 ((4, 3), (5, 4))
  status                  : LULUS
Mengganti data studi kasus
Ubah daftar GEDUNG di closest_pair.py dengan format ("Nama gedung", lintang, bujur), lalu jalankan python closest_pair.py studi_kasus.
Sumber kode dan alat bantu AI
Kode inti disusun berdasarkan algoritma Divide and Conquer dari Shamos dan Hoey dan ditulis tanpa menyalin dari repositori, buku, atau forum. Penyusunan kode dibantu alat bantu AI; rinciannya dilaporkan pada lampiran laporan.

