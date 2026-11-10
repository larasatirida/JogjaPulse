# Dokumentasi Sumber Data Sekunder
## 1. Ringkasan
## 2. Data batas wilayah
   - Sumber utama: aaronsanger/idn-geojson (link, commit/tanggal akses, asal: cahyadsn + referensi GADM 4.1)
   - Pembanding: GADM 4.1 level 3
   - Cakupan: 78 kapanewon/kemantren DIY; CRS: EPSG:4326
   - Atribut: kolom dan artinya (tabel)
   - Hasil validasi: 78 = 78, 1 beda ejaan, bbox konsisten
   - Lisensi dan atribusi
## 3. Data penduduk BPS
   - Tabel per wilayah: judul, URL, tahun, tanggal diperbarui, tanggal akses
   - Kolom hasil agregat (nama, tipe, arti, satuan, contoh)
   - Cara agregasi (kelurahan → kapanewon), catatan wilayah tanpa jenis kelamin
## 4. Kesesuaian dengan dataset Zenodo (periode, wilayah, jumlah unit)
## 5. Key integrasi
   - Kunci utama: kode wilayah 34.xx.xx
   - Peringatan: nama kapanewon tidak unik (contoh JETIS) → gunakan kab_kota + kapanewon
   - Aturan normalisasi nama
## 6. Keterbatasan
## 7. Cara menjalankan ulang
# Dokumentasi Sumber Data Sekunder & Batas Wilayah (Anggota 2)

**Proyek:** Group Project Human Mobility (Rekayasa Data, DTETI UGM)
**Dataset utama:** Zenodo [23157460](https://zenodo.org/records/23157460), DIY, 78 kapanewon, periode Des 2021 – Apr 2022
**Notebook:** `notebooks/02_secondary_data_boundaries.ipynb`

## 1. Ringkasan
| Item | Hasil |
|---|---|
| Batas wilayah | 78 poligon kapanewon DIY (GeoJSON, WGS84), sumber utama aaronsanger/idn-geojson, pembanding GADM 4.1 level 3 |
| Dataset kedua | Jumlah penduduk per kapanewon, 2021 dan 2022, 78 × 2 = 156 baris (BPS kab/kota dan Satu Data Bantul) |
| Key join | `kapanewon_code` (format `34.xx.xx`) atau pasangan `kab_kota` + `kapanewon` |
| Kecocokan dengan Zenodo | 78 dari 78 kapanewon cocok (nama dan jumlah) pada batas wilayah maupun data penduduk |

## 2. Batas wilayah
### 2.1 Sumber
| | Sumber utama | Pembanding |
|---|---|---|
| Nama | aaronsanger/idn-geojson (`districts/34_01, 34_02, 34_03, 34_04, 34_71`) | GADM 4.1 level 3 (`gadm41_IDN_3.json`) |
| Link | https://github.com/aaronsanger/idn-geojson | https://gadm.org/download_country.html |
| Versi / tahun | Export 8 Sep 2026. Asal data upstream: cahyadsn (rujukan GADM 4.1). **Tahun batas tidak tercatat.** | GADM versi 4.1 |
| Lisensi | Tidak ada file LICENSE di repo; mengikuti syarat GADM | https://gadm.org/license.html |
| Tanggal akses | 09 November 2026 | 09 November 2026 |

### 2.2 Atribut kunci
| Hal | aaronsanger | GADM |
|---|---|---|
| Nama kapanewon | `name` (mis. `KEC. GAMPING`) | `NAME_3` (mis. `Gamping`) |
| Nama kab/kota | `parent_name` (mis. `KAB. SLEMAN`) | `NAME_2` |
| Kode wilayah | `code` / `bps_code` (`34.04.01`, sama dengan Zenodo) | `GID_3` (`IDN.33.1.1_1`, kode GADM, **tidak bisa dipakai join**) |

### 2.3 Hasil validasi
- Jumlah fitur: aaronsanger 78, GADM (filter DIY) 78, Zenodo 78.
- Perbandingan nama aaronsanger vs GADM: seluruh pasangan (kab/kota, kapanewon) cocok. Satu selisih awal (`kotagede` vs `gede`) **bukan perbedaan data**, melainkan efek fungsi normalisasi yang membuang awalan "kota"; sudah diperbaiki di notebook.
- Bounding box aaronsanger: lon 110.004 – 110.839, lat -8.206 – -7.541; GADM: lon 110.014 – 110.835, lat -8.204 – -7.542. Keduanya berada di DIY.
- **CRS:** EPSG:4326 (WGS84, derajat lon/lat). File tidak mencantumkan `crs`, sehingga berlaku standar GeoJSON; dibuktikan dari rentang koordinat. File grid 500 m di Zenodo memakai UTM (meter), sehingga perlu `to_crs` bila ditumpuk.

### 2.4 File keluaran
| File | Isi |
|---|---|
| `kapanewon_diy_boundary.geojson` | 78 poligon, ditambah properti `kapanewon_clean`, `kab_kota_clean`, `join_key` |
| `kapanewon_lookup.csv` | `kapanewon_code`, `kab_kota`, `kapanewon` (78 baris) |
| `gadm_diy.geojson` | GADM DIY (pembanding) |

## 3. Data penduduk (dataset kedua)
### 3.1 Sumber
| Kab/Kota | Sumber | Tahun | Isi | Catatan |
|---|---|---|---|---|
| Kota Yogyakarta | [BPS Kota Yogyakarta](https://jogjakota.bps.go.id/id/statistics-table/1/MzgjMQ==/jumlah-penduduk-menurut-jenis-kelamin-dan-kelurahan-2018-2022.html) | 2018–2022 | L/P/total per **kelurahan** | Diagregasi ke 14 kecamatan |
| Sleman | [BPS Sleman](https://slemankab.bps.go.id/id/statistics-table/2/ODAjMg==/jumlah-penduduk-hasil-sp2020-menurut-kecamatan-dan-jenis-kelamin.html) | 2021, 2022 | L/P/total | |
| Kulon Progo | [BPS Kulon Progo](https://kulonprogokab.bps.go.id/id/statistics-table/2/NDQ0IzI=/jumlah-penduduk-menurut-kecamatan-dan-jenis-kelamin-tahun-2020.html) | 2021, 2022 | L/P/total | |
| Gunungkidul | [BPS Gunungkidul](https://gunungkidulkab.bps.go.id/id/statistics-table/2/NTE0IzI=/jumlah-penduduk-pertengahan-tahun-menurut-kapanewon--jiwa-.html) | 2021, 2022 | **Total saja** | Penduduk pertengahan tahun |
| Bantul | [Satu Data Bantul](https://data.bantulkab.go.id/search/detail?data_id=2.12.0063&ryear=2020+-+2022) | 2021, 2022 (2020 = n/a) | L/P/total | Angka bertitik ribuan |

Tanggal akses: 09 November 2026. Lisensi: mengikuti ketentuan masing-masing portal (BPS / Satu Data Bantul); cantumkan atribusi.

### 3.2 Kamus data: `bps_population_kapanewon_diy_2021_2022.csv`
| Kolom | Tipe | Arti | Contoh |
|---|---|---|---|
| `kapanewon_code` | string | Kode wilayah (key join) | `34.01.01` |
| `kab_kota` | string | Kabupaten/kota (huruf besar) | `KULON PROGO` |
| `kapanewon` | string | Nama kapanewon/kecamatan (huruf besar) | `TEMON` |
| `tahun` | int | Tahun data | `2021` |
| `laki_laki` | Int64 | Penduduk laki-laki (jiwa); kosong untuk Gunungkidul | `14159` |
| `perempuan` | Int64 | Penduduk perempuan (jiwa); kosong untuk Gunungkidul | `14278` |
| `total` | Int64 | L+P bila tersedia, selain itu total BPS | `28437` |
| `total_published` | Int64 | Total sebagaimana tertulis di sumber | `28437` |
| `flag_total_mismatch` | bool | `True` bila L+P ≠ total di sumber (selisih > 1) | `False` |
| `sumber` | string | Sumber baris tersebut | |

Dimensi: 156 baris (78 kapanewon × 2 tahun). Total DIY: 3.695.058 (2021) dan 3.713.247 (2022).

### 3.3 Perlakuan khusus
- **Kota Yogyakarta:** 45 kelurahan dijumlahkan ke 14 kecamatan; kolom kecamatan di-*forward fill*; ejaan `KEC.Matrijeron` dikoreksi menjadi `MANTRIJERON`; awalan `KEC.`/`KEC ` dibuang.
- **Bantul:** hierarki dibaca dari jumlah titik pada kolom `Kode`; titik ribuan dihapus.
- **Gunungkidul:** L/P dibiarkan kosong, tidak diperkirakan.
- Baris total kabupaten dibuang agar tidak terhitung ganda.

## 4. Kesesuaian dengan Zenodo
- **Wilayah:** 78 kapanewon di semua sumber; tidak ada yang tanpa pasangan.
- **Periode:** BPS tahunan (2021, 2022) vs Zenodo Des 2021 – Apr 2022. **Tahun 2021** digunakan untuk analisis utama; 2022 sebagai pembanding.
- **Perbandingan dengan kolom `pop_actual` Zenodo (BPS 2021 / `pop_actual`):**

| Kab/Kota | BPS 2021 | `pop_actual` | Rasio per kapanewon (min – maks) |
|---|---|---|---|
| Sleman | 1.136.474 | 1.134.150 | ≈ 1,002 |
| Kulon Progo | 438.195 | 438.190 | ≈ 1,000 |
| Gunungkidul | 748.269 | 748.270 | 0,996 – 1,001 |
| Bantul | 956.513 | 991.890 | 0,908 – 1,024 |
| Kota Yogyakarta | 415.607 | 375.280 | 1,037 – 1,208 |

Tiga kabupaten hampir identik. Kota Yogyakarta dan sebagian Bantul (Banguntapan, Kasihan, Sewon) berbeda, kemungkinan karena sumber atau tahun yang dipakai pada `pop_actual` berbeda.

## 5. Key integrasi dan aturan nama
- **Key utama:** `kapanewon_code`. File Zenodo yang memuat kode (mis. `presence_kapanewon_hourly`, `od_*`) bisa di-join langsung.
- **File Zenodo tanpa kode** (mis. `validation_night_presence_kapanewon.csv`, `home_maids_vs_population_kapanewon.csv`): join dengan **`kab_kota` + `kapanewon`** (huruf besar, tanpa awalan).
- **Jangan join dengan nama kapanewon saja:** `JETIS` ada di Bantul (`34.02.09`) dan Kota Yogyakarta (`34.71.02`).
- Normalisasi: huruf besar, buang awalan `KEC.`/`KAB.`/`KOTA`, rapikan spasi. Pada nama kapanewon, kata "Kota" (mis. `KOTAGEDE`) **tidak boleh dibuang**.

## 6. Keterbatasan
1. Tahun/versi batas wilayah tidak tercatat; bukan data resmi BIG/BPS, melainkan dari GADM.
2. Tahun BPS (2021/2022) tidak persis sama dengan rentang Zenodo (Des 2021 – Apr 2022).
3. Gunungkidul tidak memiliki rincian jenis kelamin per kapanewon.
4. Tujuh baris Kota Yogyakarta memiliki L+P ≠ total di sumber (ditandai `flag_total_mismatch`).
5. Angka penduduk BPS untuk Kota Yogyakarta dan sebagian Bantul tidak sama dengan `pop_actual` Zenodo.
6. Penduduk BPS berbasis tempat tinggal terdaftar, sedangkan data mobilitas berbasis perangkat; perbandingan keduanya bukan ukuran yang setara satu-satu.

## 7. Cara menjalankan ulang
1. Clone repo, taruh file CSV BPS asli di `data/raw/bps/`, file GADM di folder kerja, dan `validation_night_presence_kapanewon.csv` dari Zenodo.
2. Buka `notebooks/secondary_data_boundaries.ipynb`, sesuaikan sel **Konfigurasi Path**, lalu *Restart and run all*.
3. Hasil ada di `outputs/`.
