# JogjaPulse

## Human Mobility Analysis in Daerah Istimewa Yogyakarta

## Project Overview

JogjaPulse merupakan proyek analisis mobilitas manusia di wilayah Daerah Istimewa Yogyakarta (DIY) yang dikembangkan sebagai bagian dari tugas mata kuliah **Rekayasa Data**.

Proyek ini menggunakan dataset mobilitas berbasis perangkat seluler yang tersedia melalui Zenodo, serta data pendukung berupa jumlah penduduk dan batas wilayah administratif. Data dari berbagai sumber tersebut diolah dan diintegrasikan untuk memahami pola kehadiran perangkat, persebaran aktivitas, serta karakteristik mobilitas berdasarkan wilayah dan waktu.

Proses pengerjaan mencakup pengumpulan data, data understanding, preprocessing, integrasi, analisis temporal dan spasial, analisis komparatif, serta visualisasi hasil.

Data mobilitas yang digunakan bersifat agregat. Jumlah perangkat yang tercatat tidak dapat secara langsung diartikan sebagai jumlah individu atau penduduk.

## Objectives

Tujuan dari proyek ini adalah:

1. Mengumpulkan dan memahami karakteristik dataset mobilitas serta data pendukung dari berbagai sumber.
2. Melakukan pemeriksaan kualitas dan preprocessing agar data siap digunakan untuk analisis.
3. Mengintegrasikan data mobilitas dengan data jumlah penduduk dan informasi administratif wilayah.
4. Menganalisis pola mobilitas berdasarkan dimensi temporal dan spasial.
5. Membandingkan karakteristik aktivitas perangkat antarwilayah serta hubungannya dengan jumlah penduduk.
6. Menyajikan hasil analisis melalui visualisasi dan dokumentasi yang informatif.

## Dataset Sources

Proyek ini menggunakan dataset mobilitas sebagai sumber utama dan beberapa sumber data pendukung.

### 1. JogjaPulse – Aggregated Human Mobility Dataset

| Information | Description |
|---|---|
| Dataset Name | JogjaPulse |
| Platform | Zenodo |
| Record ID | 23157460 |
| Geographic Coverage | Daerah Istimewa Yogyakarta |
| Observation Period | 1 December 2021 – 30 April 2022 |
| Data Format | CSV |
| Spatial Resolution | 500-meter grid and kapanewon level |
| Source Link | https://zenodo.org/records/23157460 |

Dataset JogjaPulse menyediakan data mobilitas agregat yang mencakup:

- Kehadiran perangkat pada grid 500 meter berdasarkan hari.
- Kehadiran perangkat pada tingkat kapanewon berdasarkan jam.
- Estimasi lokasi rumah perangkat.
- Hubungan wilayah asal dan tujuan (*Origin-Destination*).
- Informasi validasi dan ringkasan kualitas publikasi data.

Dataset utama terdiri atas delapan file CSV:

| File | Description |
|---|---|
| `presence_cell500m_daily.csv` | Kehadiran perangkat pada grid 500 meter setiap hari. |
| `presence_kapanewon_hourly.csv` | Kehadiran perangkat berdasarkan kapanewon dan jam. |
| `home_maids_vs_population_kapanewon.csv` | Perbandingan jumlah perangkat berdasarkan estimasi lokasi rumah dengan populasi. |
| `validation_night_presence_kapanewon.csv` | Indikator kehadiran perangkat pada malam hari dan informasi validasi. |
| `od_home_visits_kapanewon_monthly.csv` | Data hubungan wilayah asal dan tujuan secara bulanan. |
| `od_origin_homes_monthly.csv` | Jumlah perangkat berdasarkan estimasi wilayah rumah setiap bulan. |
| `tier1_summary.csv` | Ringkasan publikasi dan suppression pada data presence. |
| `od_summary.csv` | Ringkasan publikasi dan suppression pada data Origin-Destination. |

Dataset mencakup **78 kode wilayah kapanewon/kecamatan** dengan periode pengamatan selama **151 hari**.

Data menggunakan *Mobile Advertising ID* (MAID) sebagai representasi perangkat. Oleh karena itu, jumlah MAID tidak dapat disamakan secara langsung dengan jumlah orang yang melakukan perjalanan.

### 2. Population Data – BPS and Satu Data Bantul

Data jumlah penduduk digunakan sebagai sumber pendukung untuk memberikan konteks demografis dalam analisis mobilitas.

| Information | Description |
|---|---|
| Data | Jumlah penduduk menurut kapanewon/kecamatan |
| Sources | BPS kabupaten/kota dan Satu Data Bantul |
| Geographic Coverage | Daerah Istimewa Yogyakarta |
| Observation Period | 2021–2022 |
| Administrative Coverage | 78 kapanewon/kecamatan |
| Processed Dataset | `bps_population_kapanewon_diy_2021_2022.csv` |

Data diperoleh dari sumber statistik wilayah yang mencakup Kota Yogyakarta, Kabupaten Sleman, Kulon Progo, Gunungkidul, dan Bantul.

Data dari masing-masing sumber disesuaikan ke tingkat kapanewon/kecamatan agar dapat diintegrasikan dengan dataset mobilitas utama.

Hasil pengolahan mencakup 156 baris data, yaitu 78 wilayah untuk masing-masing tahun 2021 dan 2022.

Sumber dan proses pengolahan data penduduk dijelaskan lebih lanjut dalam `docs/secondary_data_sources.md`.

### 3. Administrative Boundary Data

Data batas wilayah administratif digunakan untuk mendukung pemetaan dan analisis spasial.

| Information | Description |
|---|---|
| Data | Batas wilayah kapanewon/kecamatan DIY |
| Primary Source | aaronsanger/idn-geojson |
| Reference Source | GADM 4.1 |
| Geographic Coverage | 78 kapanewon/kecamatan |
| Format | GeoJSON |
| Coordinate Reference System | EPSG:4326 (WGS84) |

Sumber data:

- https://github.com/aaronsanger/idn-geojson
- https://gadm.org/

Data batas wilayah digunakan untuk menghubungkan hasil analisis dengan representasi geografis masing-masing kapanewon/kecamatan.

File yang digunakan antara lain:

- `kapanewon_diy_boundary.geojson`
- `gadm_diy.geojson`
- `kapanewon_lookup.csv`

Penggabungan data menggunakan kode administratif `kapanewon_code` untuk menghindari kesalahan akibat nama wilayah yang sama pada kabupaten/kota berbeda.

Informasi sumber, atribut, normalisasi, dan hasil validasi tersedia dalam `docs/secondary_data_sources.md`.

## Repository Structure

Struktur utama repository adalah sebagai berikut:

```text
JogjaPulse/
│
├── data/
│   ├── raw/
│   │   ├── zenodo/
│   │   ├── bps/
│   │   └── boundaries/
│   │
│   ├── clean/
│   └── integrated/
│
├── docs/
│   ├── data_profile.md
│   ├── data_profile_complete.md
│   ├── preprocessing_report.md
│   └── secondary_data_sources.md
│
├── notebooks/
│   ├── 03_preprocessing_eksplorasi.ipynb
│   ├── 04_integration_eksplorasi.ipynb
│   ├── 05_temporal_analytics.ipynb
│   ├── 06_spatial_analytics.ipynb
│   ├── 07_comparative_analytics.ipynb
│   └── secondary_data_boundaries.ipynb
│
├── outputs/
│   ├── inventory/
│   ├── quality_reports/
│   ├── preprocessing/
│   ├── temporal/
│   ├── spatial/
│   ├── comparative/
│   ├── arsitektur_pipeline.png
│   └── validasi_integrasi.md
│
├── src/
│   ├── 00_download_data.py
│   ├── 01_inspect_zenodo.py
│   ├── 03_preprocessing.py
│   ├── 04_integration.py
│   └── run_pipeline.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

Struktur di atas menampilkan folder dan file utama. Dataset hasil pengolahan, visualisasi, dan berkas pendukung lainnya tersedia di dalam masing-masing direktori.

### Folder Description

| Folder / File | Description |
|---|---|
| `data/raw/` | Menyimpan dataset asli dari sumber utama dan pendukung. |
| `data/clean/` | Menyimpan dataset hasil preprocessing dalam format CSV dan/atau Parquet. |
| `data/integrated/` | Menyimpan hasil integrasi data, termasuk Parquet dan database DuckDB. |
| `docs/` | Menyimpan dokumentasi sumber, karakteristik, dan pengolahan data. |
| `notebooks/` | Menyimpan notebook eksplorasi, integrasi, dan analisis data. |
| `outputs/` | Menyimpan inventaris, laporan kualitas, visualisasi, dan hasil analisis. |
| `src/` | Menyimpan script Python untuk pengunduhan, inspeksi, preprocessing, dan integrasi data. |
| `requirements.txt` | Berisi daftar dependency Python yang digunakan dalam proyek. |
| `.gitignore` | Mengatur file dan direktori yang tidak perlu dilacak Git. |

## Methodology

Proyek dikembangkan melalui beberapa tahapan pengolahan dan analisis data.

### 1. Data Collection

Dataset utama diperoleh dari Zenodo, sedangkan data pendukung dikumpulkan dari BPS, Satu Data Bantul, dan sumber batas wilayah administratif.

Data asli disimpan pada direktori `data/raw/` dengan pemisahan berdasarkan sumbernya.

### 2. Data Understanding and Quality Assessment

Pemeriksaan awal dilakukan untuk memahami struktur dan karakteristik dataset, meliputi:

- Jumlah baris dan kolom.
- Nama atribut dan tipe data.
- Missing values.
- Duplikasi baris.
- Rentang nilai dan jumlah nilai unik.
- Cakupan spasial dan temporal.
- Keterbatasan dan karakteristik publikasi data.

Hasil pemeriksaan didokumentasikan melalui data profile, data dictionary, inventaris dataset, dan laporan kualitas data.

### 3. Data Preprocessing

Tahap preprocessing bertujuan menyiapkan data agar memiliki struktur dan tipe data yang sesuai untuk analisis.

Proses yang dilakukan mencakup pemeriksaan konsistensi atribut, penyesuaian tipe data, normalisasi nama dan kode wilayah, serta penyusunan dataset bersih.

Hasil preprocessing disimpan pada direktori `data/clean/`.

Script utama:

`src/03_preprocessing.py`

Dokumentasi hasil:

`docs/preprocessing_report.md`

### 4. Data Integration

Tahap integrasi menggabungkan data mobilitas dengan data penduduk dan informasi administratif wilayah.

Penggabungan dilakukan menggunakan kode wilayah `kapanewon_code`, bukan hanya nama kapanewon, karena terdapat nama wilayah yang sama pada kabupaten/kota berbeda.

Hasil integrasi disimpan dalam format Parquet dan database DuckDB.

Beberapa file hasil integrasi:

- `integrated_hourly.parquet`
- `integrated_kapanewon.parquet`
- `integrated_kapanewon_regime.parquet`
- `jogjapulse.duckdb`

Script utama:

`src/04_integration.py`

Dokumentasi validasi:

`outputs/validasi_integrasi.md`

### 5. Temporal Analytics

Analisis temporal digunakan untuk mengamati karakteristik aktivitas perangkat berdasarkan waktu.

Cakupan analisis meliputi:

- Pola aktivitas berdasarkan jam.
- Perbandingan hari kerja dan akhir pekan.
- Perubahan aktivitas harian.
- Perbandingan pola aktivitas pada periode berbeda.
- Eksplorasi tren dan peramalan.

Notebook:

`notebooks/05_temporal_analytics.ipynb`

Visualisasi:

`outputs/temporal/`

### 6. Spatial Analytics

Analisis spasial digunakan untuk memahami persebaran aktivitas perangkat antarwilayah di DIY.

Cakupan analisis meliputi:

- Persebaran aktivitas pada tingkat kapanewon.
- Identifikasi wilayah dengan aktivitas tinggi.
- Visualisasi hotspot pada grid spasial.
- Analisis hubungan wilayah asal dan tujuan.
- Visualisasi arus mobilitas antarwilayah.

Notebook:

`notebooks/06_spatial_analytics.ipynb`

Visualisasi dan hasil:

`outputs/spatial/`

### 7. Comparative Analytics

Analisis komparatif dilakukan untuk membandingkan indikator mobilitas dengan jumlah penduduk dan karakteristik wilayah.

Cakupan analisis meliputi:

- Perbandingan jumlah perangkat dengan populasi.
- Analisis hubungan antara indikator mobilitas dan jumlah penduduk.
- Identifikasi perbedaan karakteristik antarwilayah.
- Analisis perbandingan berdasarkan periode pengamatan.

Notebook:

`notebooks/07_comparative_analytics.ipynb`

Visualisasi dan hasil:

`outputs/comparative/`

### 8. Data Visualization and Documentation

Hasil analisis disajikan dalam bentuk grafik, peta, tabel, dan dokumentasi pendukung.

Visualisasi disimpan pada direktori `outputs/` sesuai kategori analisis agar dapat digunakan dalam penyusunan laporan, video, dan presentasi proyek.

## Data Documentation

Dokumentasi proyek tersedia pada direktori `docs/` dan `outputs/`.

| File | Description |
|---|---|
| `docs/data_profile.md` | Profil dataset hasil inspeksi otomatis. |
| `docs/data_profile_complete.md` | Dokumentasi karakteristik, kualitas, dan keterbatasan dataset utama. |
| `docs/secondary_data_sources.md` | Dokumentasi sumber data penduduk dan batas wilayah. |
| `docs/preprocessing_report.md` | Ringkasan pemeriksaan dan hasil preprocessing. |
| `outputs/inventory/zenodo_inventory.csv` | Inventaris file dataset Zenodo. |
| `outputs/quality_reports/data_dictionary_completed.csv` | Data dictionary yang dilengkapi dengan penjelasan atribut. |
| `outputs/quality_reports/data_dictionary_template.csv` | Template data dictionary hasil inspeksi otomatis. |
| `outputs/quality_reports/data_quality_report.csv` | Hasil pemeriksaan kualitas dataset utama. |
| `outputs/validasi_integrasi.md` | Hasil validasi integrasi data. |
| `outputs/arsitektur_pipeline.png` | Diagram arsitektur pipeline pengolahan data. |

## Tools and Technologies

Teknologi yang digunakan dalam proyek ini meliputi:

| Technology | Usage |
|---|---|
| Python | Pengunduhan, pengolahan, integrasi, dan analisis data. |
| Pandas | Manipulasi dan pengolahan data tabular. |
| PyArrow | Penyimpanan dan pembacaan data dalam format Parquet. |
| DuckDB | Penyimpanan dan pengelolaan dataset terintegrasi. |
| GeoPandas | Pengolahan data spasial. |
| Matplotlib | Visualisasi data. |
| Seaborn | Visualisasi statistik. |
| Plotly | Visualisasi data interaktif. |
| Folium | Visualisasi peta. |
| SciPy | Analisis statistik dan komputasi ilmiah. |
| Statsmodels | Analisis statistik dan deret waktu. |
| Jupyter Notebook | Eksplorasi, analisis, dan dokumentasi berbasis notebook. |
| Git & GitHub | Version control dan kolaborasi kelompok. |

Daftar dependency Python tersedia dalam `requirements.txt`.

## Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/larasatirida/JogjaPulse.git
cd JogjaPulse
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Aktivasi virtual environment pada Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Pada Linux atau macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Inspect Dataset

Untuk menjalankan pemeriksaan dataset Zenodo:

```bash
python src/01_inspect_zenodo.py
```

Script ini menghasilkan ulang inventaris, laporan kualitas, template data dictionary, dan profil dataset otomatis.

**Catatan:** Jalankan script inspeksi hanya jika ingin memperbarui file hasil otomatis. Script ini menulis ulang beberapa file pada `outputs/` dan `docs/data_profile.md`.

### 5. Run Data Pipeline

Untuk menjalankan preprocessing dan integrasi menggunakan data raw yang sudah tersedia:

```bash
python src/run_pipeline.py
```

Untuk menjalankan pipeline dengan tahap pengunduhan dataset Zenodo:

```bash
python src/run_pipeline.py --with-download
```

Pipeline menjalankan tahap pengunduhan (opsional), preprocessing, dan integrasi.

Script pipeline dapat menulis ulang dataset hasil pengolahan dan laporan terkait. Pastikan file raw yang diperlukan sudah tersedia sebelum menjalankannya.

### 6. Explore Analysis Notebooks

Notebook analisis tersedia dalam direktori `notebooks/`.

Jalankan Jupyter Notebook:

```bash
jupyter notebook
```

Buka notebook sesuai kategori analisis yang ingin dipelajari.

## Data Quality and Limitations

Interpretasi hasil analisis perlu memperhatikan karakteristik dan keterbatasan dataset.

1. **Device-based representation.** Dataset menggunakan MAID sebagai representasi perangkat. Jumlah perangkat tidak sama dengan jumlah individu atau penduduk.

2. **Aggregated data.** Data yang dipublikasikan merupakan hasil agregasi, bukan data perjalanan individu secara langsung.

3. **Privacy suppression.** Dataset menerapkan ambang batas minimum `k = 5`. Baris yang tidak dipublikasikan akibat suppression tidak boleh langsung dianggap bernilai nol.

4. **Sampling bias.** Data berasal dari perangkat yang tercakup oleh sumber data lokasi, sehingga belum tentu merepresentasikan seluruh populasi DIY secara merata.

5. **Changes in device coverage.** Jumlah perangkat yang teramati berubah selama periode pengamatan. Perbandingan tren antarwaktu perlu mempertimbangkan perubahan cakupan tersebut.

6. **Origin-Destination quality.** Sebagian data Origin-Destination pada Maret–April 2022 memiliki penanda `reduced_quality`, sehingga interpretasi pada periode tersebut memerlukan kehati-hatian.

7. **Administrative identifiers.** Identifikasi dan integrasi wilayah sebaiknya menggunakan kode administratif karena nama kapanewon tidak selalu unik.

8. **Population comparison.** Data jumlah perangkat dan populasi resmi memiliki definisi serta cakupan pengukuran yang berbeda, sehingga hasil perbandingannya tidak dapat langsung diinterpretasikan sebagai tingkat mobilitas penduduk.

9. **Temporal and spatial coverage.** Hasil analisis berlaku dalam konteks wilayah, periode, dan cakupan data yang digunakan pada proyek ini.

Keterbatasan tersebut menjadi pertimbangan dalam preprocessing, integrasi, analisis, dan interpretasi hasil.

## Team Members

| No. | Name | Student ID |
|---|---|---|
| 1 | Shafa Aura Yogadiasa | 22/496508/TK/54406 |
| 2 | Sri Wahyuni Arista | 23/521971/TK/57593 |
| 3 | Mayravivania Syahda Charisa | 24/538308/TK/59701 |
| 4 | Rida Larasati | 24/539400/TK/59821 |
| 5 | Zahira Anindya Putri | 24/543202/TK/60347 |
| 6 | Monica Anastasya Dantina | 24/544527/TK/60525 |
| 7 | Sukmawati | 24/545512/TK/60686 |

## Project Status

Proyek telah memiliki dataset utama dan pendukung, dokumentasi data, script preprocessing dan integrasi, serta notebook dan visualisasi untuk analisis temporal, spasial, dan komparatif.

Repository juga menyediakan hasil pengolahan data dalam format CSV, Parquet, dan DuckDB, serta laporan validasi dan dokumentasi pendukung.

Tahap akhir proyek difokuskan pada pemeriksaan kelengkapan hasil, konsistensi dokumentasi, interpretasi analisis, dan persiapan materi pengumpulan serta presentasi.

## References

1. JogjaPulse – Aggregated Human Mobility Dataset. Zenodo. https://zenodo.org/records/23157460
2. Badan Pusat Statistik (BPS). https://www.bps.go.id/
3. Satu Data Bantul. https://data.bantulkab.go.id/
4. aaronsanger/idn-geojson. https://github.com/aaronsanger/idn-geojson
5. GADM – Database of Global Administrative Areas. https://gadm.org/

Rincian sumber data sekunder, tautan tabel statistik, dan informasi pengolahan tersedia dalam `docs/secondary_data_sources.md`.