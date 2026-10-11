"""
Eksperimen tambahan (tanpa pustaka eksternal):
  1. Menghitung jumlah perhitungan jarak (tidak bergantung pada kecepatan komputer)
  2. Menguji pengaruh sebaran titik terhadap waktu Divide and Conquer
  3. Uji sensitivitas studi kasus: bila titik tiap gedung bergeser

Cara menjalankan:  python eksperimen_tambahan.py
Hasil disimpan ke hasil_operasi.csv, hasil_sebaran.csv, hasil_sensitivitas.csv
"""

import math
import closest_pair as cp


# ---------------------------------------------------------------------------
# 1. Menghitung jumlah pemanggilan fungsi jarak
# ---------------------------------------------------------------------------
def hitung_jarak(fungsi, titik):
    """Menjalankan fungsi dan menghitung berapa kali jarak() dipanggil."""
    cacah = [0]
    asli = cp.jarak

    def pembungkus(p, q):
        cacah[0] += 1
        return asli(p, q)

    cp.jarak = pembungkus  # fungsi lain di closest_pair.py memakai jarak ini
    try:
        hasil = fungsi(titik)
    finally:
        cp.jarak = asli
    return cacah[0], hasil


def eksperimen_operasi():
    baris = ["n,brute_force,divide_conquer,n_log2_n,rasio_dc_terhadap_nlogn,rasio_bf_terhadap_dc"]
    print("n, BF, D&C, n log2 n, D&C/(n log2 n), BF/D&C")
    for n in [100, 500, 1000, 2000, 5000, 10000, 50000, 100000]:
        titik = cp.buat_titik(n, seed=2026 + n)
        c_dc, _ = hitung_jarak(cp.closest_pair, titik)
        if n <= 2000:  # brute force benar-benar dihitung untuk n kecil
            c_bf, _ = hitung_jarak(cp.brute_force, titik)
            # n(n-1)/2 pasangan + 1 perhitungan awal untuk pasangan pertama
            assert c_bf == n * (n - 1) // 2 + 1
        else:
            c_bf = n * (n - 1) // 2 + 1
        nlogn = n * math.log2(n)
        baris.append("%d,%d,%d,%.1f,%.4f,%.2f" % (n, c_bf, c_dc, nlogn, c_dc / nlogn, c_bf / c_dc))
        print(n, c_bf, c_dc, round(nlogn), round(c_dc / nlogn, 3), round(c_bf / c_dc, 1))
    with open("hasil_operasi.csv", "w") as f:
        f.write("\n".join(baris) + "\n")


# ---------------------------------------------------------------------------
# 2. Pengaruh sebaran titik
# ---------------------------------------------------------------------------
def sebaran_seragam(n, seed):
    return cp.buat_titik(n, seed)


def sebaran_berklaster(n, seed):
    g = cp.Acak(seed)
    pusat = [(100000 * g.berikut(), 100000 * g.berikut()) for _ in range(20)]
    hasil = []
    for i in range(n):
        c = pusat[i % 20]
        dx = (g.berikut() + g.berikut() + g.berikut() - 1.5) * 2000
        dy = (g.berikut() + g.berikut() + g.berikut() - 1.5) * 2000
        hasil.append((c[0] + dx, c[1] + dy))
    return hasil


def sebaran_segaris(n, seed):
    g = cp.Acak(seed)
    return [(100000 * g.berikut(), 500.0) for _ in range(n)]


def sebaran_strip_sempit(n, seed):
    g = cp.Acak(seed)
    return [(100 * g.berikut(), 100000 * g.berikut()) for _ in range(n)]


def sebaran_kisi(n, seed):
    sisi = int(n ** 0.5)
    return [(10.0 * (i % sisi), 10.0 * (i // sisi)) for i in range(sisi * sisi)]


SEBARAN = [
    ("seragam", sebaran_seragam),
    ("berklaster", sebaran_berklaster),
    ("segaris", sebaran_segaris),
    ("strip_sempit", sebaran_strip_sempit),
    ("kisi_teratur", sebaran_kisi),
]


def eksperimen_sebaran():
    n = 20000
    ulangan = 5
    baris = ["sebaran,n,rata_rata_ms,simpangan_baku_ms,jumlah_jarak,uji_benar"]
    print("sebaran, n, rata-rata (ms), simpangan baku (ms), jumlah jarak, uji benar")
    for nama, pembuat in SEBARAN:
        # uji kebenaran pada n kecil terhadap brute force
        kecil = pembuat(1000, 99)
        benar = abs(cp.closest_pair(kecil)[0] - cp.brute_force(kecil)[0]) < 1e-9

        waktu = []
        for r in range(ulangan):
            titik = pembuat(n, 3000 + r)
            t, _ = cp.ukur(cp.closest_pair, titik)
            waktu.append(t)
        titik = pembuat(n, 3000)
        cacah, _ = hitung_jarak(cp.closest_pair, titik)
        m, s = cp.rata_rata(waktu), cp.simpangan_baku(waktu)
        baris.append("%s,%d,%.4f,%.4f,%d,%s" % (nama, len(titik), m, s, cacah, "ya" if benar else "tidak"))
        print(nama, len(titik), round(m, 3), round(s, 3), cacah, benar, flush=True)
    with open("hasil_sebaran.csv", "w") as f:
        f.write("\n".join(baris) + "\n")


# ---------------------------------------------------------------------------
# 3. Sensitivitas studi kasus terhadap letak titik gedung
# ---------------------------------------------------------------------------
def eksperimen_sensitivitas():
    """
    Setiap gedung digeser acak sejauh paling jauh r meter pada sumbu x dan y.
    Dihitung berapa persen percobaan yang masih menghasilkan pasangan terdekat
    yang sama dengan data asli.
    """
    titik = cp.proyeksi(cp.GEDUNG)
    indeks_asli = {titik[i]: i for i in range(len(titik))}
    d0, (a0, b0) = cp.closest_pair(titik)
    pasangan_asli = {indeks_asli[a0], indeks_asli[b0]}
    percobaan = 1000

    baris = ["radius_m,percobaan,pasangan_sama,persen_sama,jarak_min_m,jarak_maks_m"]
    print("radius (m), pasangan sama, persen, jarak min, jarak maks")
    for r in [10, 20, 30, 40, 50]:
        g = cp.Acak(500 + r)
        sama = 0
        d_min = None
        d_maks = None
        for _ in range(percobaan):
            geser = []
            for (x, y) in titik:
                geser.append((x + (2 * g.berikut() - 1) * r,
                              y + (2 * g.berikut() - 1) * r))
            indeks = {geser[i]: i for i in range(len(geser))}
            d, (a, b) = cp.closest_pair(geser)
            if {indeks[a], indeks[b]} == pasangan_asli:
                sama += 1
            if d_min is None or d < d_min:
                d_min = d
            if d_maks is None or d > d_maks:
                d_maks = d
        baris.append("%d,%d,%d,%.1f,%.2f,%.2f" % (r, percobaan, sama, 100.0 * sama / percobaan, d_min, d_maks))
        print(r, sama, round(100.0 * sama / percobaan, 1), round(d_min, 2), round(d_maks, 2), flush=True)
    with open("hasil_sensitivitas.csv", "w") as f:
        f.write("\n".join(baris) + "\n")


if __name__ == "__main__":
    eksperimen_operasi()
    print()
    eksperimen_sebaran()
    print()
    eksperimen_sensitivitas()
