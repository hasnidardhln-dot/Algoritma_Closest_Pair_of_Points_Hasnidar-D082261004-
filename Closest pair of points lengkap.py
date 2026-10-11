from math import sin, cos, radians, sqrt, asin
from time import perf_counter


# Nama gedung, lintang, bujur
GEDUNG = [
    ("Gedung A", -5.13100, 119.48700),
    ("Gedung B", -5.13160, 119.48830),
    ("Gedung C", -5.13050, 119.48960),
    ("Gedung D", -5.13240, 119.48620),
    ("Gedung E", -5.13300, 119.48900),
    ("Gedung F", -5.12980, 119.48780),
    ("Gedung G", -5.13190, 119.48990),
    ("Gedung H", -5.13370, 119.48740),
    ("Gedung I", -5.13020, 119.48870),
    ("Gedung J", -5.13280, 119.48560),
    ("Gedung K", -5.13140, 119.48745),
    ("Gedung L", -5.13410, 119.48990),
]

R = 6_371_000  # jari-jari rata-rata Bumi dalam meter


def konversi_ke_meter(data):
    """Proyeksi equirectangular lokal untuk area kampus."""
    phi0 = sum(radians(lat) for _, lat, _ in data) / len(data)
    lambda0 = sum(radians(lon) for _, _, lon in data) / len(data)
    hasil = []
    for nama, lat, lon in data:
        phi = radians(lat)
        lam = radians(lon)
        x = R * (lam - lambda0) * cos(phi0)
        y = R * (phi - phi0)
        hasil.append((nama, x, y, lat, lon))
    return hasil


def jarak(a, b):
    """Jarak Euclidean pada koordinat lokal dalam meter."""
    return sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def haversine(lat1, lon1, lat2, lon2):
    """Pemeriksaan jarak geografis langsung, dalam meter."""
    p1, p2 = radians(lat1), radians(lat2)
    dp = radians(lat2 - lat1)
    dl = radians(lon2 - lon1)
    h = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * R * asin(sqrt(h))


def brute_force(titik):
    if len(titik) < 2:
        raise ValueError("Minimal diperlukan 2 gedung.")
    terbaik = jarak(titik[0], titik[1])
    pasangan = (titik[0], titik[1])
    for i in range(len(titik)):
        for j in range(i + 1, len(titik)):
            d = jarak(titik[i], titik[j])
            if d < terbaik:
                terbaik = d
                pasangan = (titik[i], titik[j])
    return terbaik, pasangan


def gabung_y(kiri, kanan):
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        if kiri[i][2] <= kanan[j][2]:
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def rekursi(titik_x):
    n = len(titik_x)

    # Kasus dasar: paling banyak tiga titik, periksa langsung.
    if n <= 3:
        d, pasangan = brute_force(titik_x)
        return d, pasangan, sorted(titik_x, key=lambda p: p[2])

    # Divide: pecah daftar yang sudah terurut menurut x.
    tengah = n // 2
    x_garis = titik_x[tengah][1]
    kiri = titik_x[:tengah]
    kanan = titik_x[tengah:]

    d_kiri, pas_kiri, y_kiri = rekursi(kiri)
    d_kanan, pas_kanan, y_kanan = rekursi(kanan)

    # Pilih hasil terbaik dari kedua bagian.
    if d_kiri <= d_kanan:
        d, pasangan = d_kiri, pas_kiri
    else:
        d, pasangan = d_kanan, pas_kanan

    # Combine: gabungkan daftar yang sudah terurut menurut y.
    urut_y = gabung_y(y_kiri, y_kanan)

    # Periksa titik dalam strip dekat garis pembagi.
    strip = [p for p in urut_y if abs(p[1] - x_garis) < d]
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][2] - strip[i][2] < d:
            d_baru = jarak(strip[i], strip[j])
            if d_baru < d:
                d = d_baru
                pasangan = (strip[i], strip[j])
            j += 1

    return d, pasangan, urut_y


def closest_pair(titik):
    if len(titik) < 2:
        raise ValueError("Minimal diperlukan 2 gedung.")
    titik_x = sorted(titik, key=lambda p: p[1])
    d, pasangan, _ = rekursi(titik_x)
    return d, pasangan


def main():
    titik = konversi_ke_meter(GEDUNG)

    print("=" * 65)
    print("CLOSEST PAIR OF POINTS - GEDUNG KAMPUS")
    print("Metode: Divide and Conquer | Python tanpa library eksternal")
    print("=" * 65)
    print("\nDATA GEDUNG (koordinat lokal dalam meter)")
    for nama, x, y, lat, lon in titik:
        print(f"{nama:10s} lintang={lat:.5f}, bujur={lon:.5f}, "
              f"x={x:8.2f} m, y={y:8.2f} m")

    mulai = perf_counter()
    d_dc, pasangan_dc = closest_pair(titik)
    waktu_dc = (perf_counter() - mulai) * 1000

    mulai = perf_counter()
    d_bf, pasangan_bf = brute_force(titik)
    waktu_bf = (perf_counter() - mulai) * 1000

    a, b = pasangan_dc
    d_hav = haversine(a[3], a[4], b[3], b[4])

    print("\nHASIL DIVIDE AND CONQUER")
    print(f"Pasangan gedung terdekat : {a[0]} dan {b[0]}")
    print(f"Jarak Euclidean          : {d_dc:.2f} meter")
    print(f"Waktu eksekusi           : {waktu_dc:.4f} ms")

    print("\nPEMBANDING BRUTE FORCE")
    print(f"Pasangan gedung terdekat : {pasangan_bf[0][0]} dan "
          f"{pasangan_bf[1][0]}")
    print(f"Jarak Euclidean          : {d_bf:.2f} meter")
    print(f"Waktu eksekusi           : {waktu_bf:.4f} ms")

    print("\nPEMERIKSAAN HAVERSINE")
    print(f"Jarak geografis pasangan hasil : {d_hav:.2f} meter")
    print(f"Selisih dengan Euclidean       : {abs(d_hav - d_dc):.4f} meter")

    print("\nVALIDASI")
    if abs(d_dc - d_bf) < 1e-9:
        print("LULUS: Divide and Conquer dan Brute Force menghasilkan jarak sama.")
    else:
        print("GAGAL: hasil kedua algoritma berbeda.")


if __name__ == "__main__":
    main()
