# JogjaPulse

# Human Mobility Analysis in Daerah Istimewa Yogyakarta

## Project Overview

Proyek ini bertujuan untuk menganalisis pola mobilitas manusia di wilayah Daerah Istimewa Yogyakarta (DIY) berdasarkan data mobilitas berbasis perangkat seluler dan sumber data pendukung lainnya.

Analisis dilakukan dengan mengolah dan mengintegrasikan data dari beberapa sumber untuk memperoleh informasi mengenai pola kehadiran perangkat, persebaran mobilitas berdasarkan wilayah dan waktu, serta hubungan antara wilayah asal dan tujuan (_Origin-Destination_).

Proses pengerjaan mencakup pengumpulan data, pemahaman karakteristik dataset, preprocessing, integrasi, analisis, dan visualisasi. Proyek ini merupakan bagian dari tugas mata kuliah Rekayasa Data.

## Objectives

Tujuan dari proyek ini adalah:

1. Mengumpulkan dan mengintegrasikan data mobilitas dari beberapa sumber.
2. Melakukan preprocessing untuk memastikan data siap digunakan dalam analisis.
3. Menganalisis pola mobilitas berdasarkan dimensi spasial dan temporal.
4. Membandingkan karakteristik mobilitas antarwilayah.
5. Menyajikan hasil analisis dalam bentuk visualisasi yang informatif.

## Dataset Sources

### 1. JogjaPulse – Human Mobility Dataset

| Information         | Description                        |
| ------------------- | ---------------------------------- |
| Dataset Name        | JogjaPulse                         |
| Platform            | Zenodo                             |
| Record ID           | 23157460                           |
| Geographic Coverage | Daerah Istimewa Yogyakarta         |
| Observation Period  | 1 December 2021 – 30 April 2022    |
| Data Format         | CSV                                |
| Spatial Resolution  | 500-meter grid and kapanewon level |

Dataset JogjaPulse menyediakan data mobilitas agregat yang mencakup:

- Kehadiran perangkat berdasarkan grid 500 meter setiap hari.
- Kehadiran perangkat berdasarkan kapanewon setiap jam.
- Estimasi lokasi rumah perangkat.
- Hubungan wilayah asal dan tujuan (_Origin-Destination_).
- Ringkasan statistik dan informasi kualitas publikasi data.

Data ini menggunakan Mobile Advertising ID (MAID) sebagai representasi perangkat. Oleh karena itu, jumlah perangkat yang tercatat tidak dapat secara langsung diartikan sebagai jumlah individu atau penduduk.

### 2. Additional Data Sources

Proyek ini juga menggunakan sumber data pendukung untuk melengkapi analisis mobilitas, seperti data statistik wilayah dan data spasial batas administratif.

Data pendukung tersebut digunakan untuk memberikan konteks tambahan dalam analisis, khususnya dalam memahami karakteristik wilayah dan membandingkan pola mobilitas antarwilayah.

Detail sumber, tautan, periode, dan atribut data tambahan akan dicantumkan setelah proses pengumpulan dan verifikasi data selesai.

## Repository Structure

```text
JogjaPulse/
│
├── data/
│   ├── raw/
│   │   └── zenodo/
│   │       ├── home_maids_vs_population_kapanewon.csv
│   │       ├── od_home_visits_kapanewon_monthly.csv
│   │       ├── od_origin_homes_monthly.csv
│   │       ├── od_summary.csv
│   │       ├── presence_cell500m_daily.csv
│   │       ├── presence_kapanewon_hourly.csv
│   │       ├── tier1_summary.csv
│   │       ├── validation_night_presence_kapanewon.csv
│   │       └── README.md
│   │
│   ├── clean/
│   └── integrated/
│
├── docs/
│   ├── data_profile.md
│   └── data_profile_complete.md
│
├── notebooks/
│   ├── outputs/
│   │   ├── inventory/
│   │   │   └── zenodo_inventory.csv
│   │   │
│   │   └── quality_reports/
│   │       ├── data_dictionary_completed.csv
│   │       ├── data_dictionary_template.csv
│   │       └── data_quality_report.csv
│   │
│   └── src/
│       ├── 00_download_data.py
│       └── 01_inspect_zenodo.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

**Folder Description:**

| Folder / File        | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| `data/raw/`          | Menyimpan dataset asli yang diperoleh dari sumber data.                    |
| `data/clean/`        | Menyimpan data yang telah melalui proses preprocessing dan pembersihan.    |
| `data/integrated/`   | Menyimpan data hasil integrasi dari beberapa sumber.                       |
| `docs/`              | Menyimpan dokumentasi terkait dataset.                                     |
| `notebooks/`         | Menyediakan tempat untuk notebook eksplorasi, preprocessing, dan analisis. |
| `notebooks/outputs/` | Menyimpan hasil inventarisasi dan pemeriksaan kualitas data.               |
| `notebooks/src/`     | Menyimpan script Python untuk pengunduhan dan pemeriksaan dataset.         |
| `requirements.txt`   | Berisi daftar library Python yang dibutuhkan untuk menjalankan proyek.     |
| `.gitignore`         | Mengatur file dan folder yang tidak perlu dimasukkan ke repository.        |

## Data Documentation

Dokumentasi pendukung proyek tersedia pada folder `docs/` dan `notebooks/outputs/quality_reports/`.

| File                                                              | Description                                                                                         |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `docs/data_profile.md`                                            | Gambaran umum dataset, cakupan wilayah dan waktu, karakteristik, kualitas, serta keterbatasan data. |
| `docs/data_profile_complete.md`                                   | Dokumentasi profil dataset hasil penyusunan dan pelengkapan informasi.                              |
| `notebooks/outputs/inventory/zenodo_inventory.csv`                | Inventaris file dataset yang diperoleh dari Zenodo.                                                 |
| `notebooks/outputs/quality_reports/data_dictionary_completed.csv` | Penjelasan atribut, tipe data, satuan, dan contoh nilai dari setiap kolom.                          |
| `notebooks/outputs/quality_reports/data_dictionary_template.csv`  | Template awal penyusunan Data Dictionary.                                                           |
| `notebooks/outputs/quality_reports/data_quality_report.csv`       | Hasil pemeriksaan kualitas dataset.                                                                 |

## Methodology

Tahapan pengerjaan proyek secara umum meliputi:

1. **Data Collection:** Mengumpulkan dataset mobilitas dan sumber data pendukung dari berbagai sumber.
2. **Data Understanding:** Memeriksa struktur, atribut, karakteristik, dan dokumentasi dataset untuk memahami informasi yang tersedia.
3. **Data Quality Assessment:** Memeriksa kualitas data, termasuk missing values, duplikasi, tipe data, dan keterbatasan dataset.
4. **Data Preprocessing:** Membersihkan, menyesuaikan, dan menyiapkan data agar dapat digunakan dalam proses analisis.
5. **Data Integration:** Menggabungkan data dari berbagai sumber sesuai kebutuhan analisis.
6. **Data Analysis:** Menganalisis pola mobilitas berdasarkan aspek spasial, temporal, dan perbandingan antarwilayah.
7. **Data Visualization:** Menyajikan hasil analisis dalam bentuk visualisasi yang informatif.
8. **Documentation:** Mendokumentasikan proses, hasil pengolahan, dan temuan selama pengerjaan proyek.

## Tools and Technologies

Tools dan teknologi yang digunakan dalam proyek ini meliputi:

- **Python:** Bahasa pemrograman untuk pengolahan dan analisis data.
- **Pandas:** Library untuk manipulasi dan pengolahan data tabular.
- **Jupyter Notebook:** Lingkungan untuk eksplorasi, preprocessing, dan analisis data.

Daftar kebutuhan library dan dependency proyek tersedia pada file `requirements.txt`.

## Team Members

| No. | Name                                             |
| --- | ------------------------------------------------ |
| 1   | Shafa Aura Yogadiasa (22/496508/TK/54406)        |
| 2   | Sri Wahyuni Arista (23/521971/TK/57593)          |
| 3   | Mayravivania Syahda Charisa (24/538308/TK/59701) |
| 4   | Rida Larasati (24/539400/TK/59821)               |
| 5   | Zahira Anindya Putri (24/543202/TK/60347)        |
| 6   | Monica Anastasya Dantina (24/544527/TK/60525)    |
| 7   | Sukmawati (24/545512/TK/60686)                   |

## Project Status

Proyek saat ini berada pada tahap pengumpulan data, data understanding, dan persiapan preprocessing. Dataset utama telah diperoleh dan melalui pemeriksaan awal untuk memahami struktur, karakteristik, serta kualitas data.

Tahapan selanjutnya meliputi pengumpulan sumber data pendukung, preprocessing, integrasi data, analisis mobilitas, dan visualisasi hasil.
