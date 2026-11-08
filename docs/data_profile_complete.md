# Data Profile

## 1. Dataset Overview

Dataset yang digunakan dalam proyek ini merupakan data mobilitas berbasis perangkat seluler di wilayah Daerah Istimewa Yogyakarta (DIY). Dataset menyediakan informasi mengenai kehadiran perangkat berdasarkan lokasi dan waktu, estimasi lokasi rumah perangkat, serta hubungan wilayah asal dan tujuan.

Data yang digunakan merupakan data agregat, bukan rekaman perjalanan individu secara langsung. Setiap MAID (_Mobile Advertising ID_) merepresentasikan identitas perangkat, sehingga jumlah perangkat yang tercatat tidak dapat disamakan dengan jumlah penduduk.

Dataset ini digunakan sebagai sumber utama untuk mendukung analisis pola mobilitas dan persebaran perangkat di wilayah DIY.

## 2. Data Source

| Informasi          | Keterangan                               |
| ------------------ | ---------------------------------------- |
| Nama dataset       | JogjaPulse                               |
| Sumber             | Zenodo                                   |
| Record ID          | 23157460                                 |
| Jenis data         | Aggregated spatio-temporal mobility data |
| Wilayah pengamatan | Daerah Istimewa Yogyakarta               |
| Format data        | CSV                                      |

Dataset diperoleh melalui publikasi Zenodo dengan Record ID 23157460. Data yang tersedia telah melalui proses agregasi dan penyaringan sebelum dipublikasikan.

Informasi mengenai lisensi dan ketentuan penggunaan data perlu mengacu pada metadata publikasi Zenodo.

## 3. Geographic and Temporal Coverage

### Geographic Coverage

Dataset mencakup wilayah Daerah Istimewa Yogyakarta dengan unit administratif berupa kabupaten/kota dan kapanewon atau kecamatan.

Data menyediakan dua tingkat representasi spasial utama:

- Grid berukuran 500 meter untuk data kehadiran perangkat harian.
- Kapanewon atau kecamatan untuk data kehadiran perangkat per jam, estimasi lokasi rumah, dan data Origin-Destination.

Berdasarkan hasil pemeriksaan, terdapat 78 kode unit wilayah kapanewon/kecamatan. Jumlah nama unik yang ditemukan adalah 77, sehingga identifikasi wilayah sebaiknya menggunakan kode administratif, bukan nama wilayah saja.

### Temporal Coverage

Periode pengamatan utama berlangsung dari 1 Desember 2021 hingga 30 April 2022, dengan total 151 hari.

Data tersedia dalam beberapa tingkat waktu, yaitu:

- Harian pada data grid 500 meter.
- Per jam pada data kehadiran perangkat berdasarkan kapanewon.
- Bulanan pada data Origin-Destination dan estimasi lokasi rumah.

## 4. Dataset Structure

Dataset terdiri atas delapan file CSV dengan fungsi yang berbeda.

| No. | Nama File                                 | Jumlah Baris | Jumlah Kolom | Deskripsi                                                                                                          |
| --- | ----------------------------------------- | -----------: | -----------: | ------------------------------------------------------------------------------------------------------------------ |
| 1   | `presence_cell500m_daily.csv`             |      183.548 |            7 | Data jumlah perangkat yang terdeteksi pada setiap grid 500 meter setiap hari.                                      |
| 2   | `presence_kapanewon_hourly.csv`           |      230.418 |            8 | Data jumlah perangkat dan catatan lokasi berdasarkan kapanewon setiap jam.                                         |
| 3   | `home_maids_vs_population_kapanewon.csv`  |           78 |            5 | Perbandingan jumlah perangkat berdasarkan estimasi lokasi rumah dengan jumlah penduduk aktual pada setiap wilayah. |
| 4   | `validation_night_presence_kapanewon.csv` |          156 |            7 | Data indikator kehadiran malam hari dan informasi publikasi data berdasarkan kapanewon.                            |
| 5   | `od_home_visits_kapanewon_monthly.csv`    |        9.894 |           11 | Data hubungan wilayah asal dan tujuan berdasarkan jumlah perangkat yang tercatat setiap bulan.                     |
| 6   | `od_origin_homes_monthly.csv`             |          390 |            8 | Data jumlah perangkat berdasarkan estimasi lokasi rumah pada setiap wilayah dan bulan.                             |
| 7   | `tier1_summary.csv`                       |            2 |            8 | Ringkasan statistik publikasi dan suppression pada produk data presence.                                           |
| 8   | `od_summary.csv`                          |            1 |            7 | Ringkasan statistik publikasi dan suppression pada data Origin-Destination.                                        |

Secara keseluruhan, delapan file tersebut memiliki 424.479 baris dan 61 kolom.

Penjelasan lebih rinci mengenai setiap kolom tersedia dalam dokumen `data_dictionary_template.csv`.

## 5. Data Characteristics

Berdasarkan hasil pemeriksaan terhadap delapan file CSV, beberapa karakteristik data yang ditemukan adalah sebagai berikut:

1. Data terdiri atas informasi geografis, temporal, jumlah perangkat, serta ringkasan kualitas publikasi.
2. Kolom tanggal pada dataset disimpan dalam format string dengan pola `YYYY-MM-DD`, sedangkan data bulanan menggunakan format `YYYY-MM`.
3. Identitas wilayah direpresentasikan melalui nama dan kode administratif kabupaten/kota maupun kapanewon.
4. Data kehadiran perangkat menggunakan MAID sebagai representasi perangkat yang terdeteksi.
5. Data spasial grid menyediakan koordinat UTM dan koordinat geografis berupa longitude dan latitude.
6. Dataset Origin-Destination menyediakan informasi mengenai wilayah asal dan tujuan berdasarkan perangkat yang teridentifikasi.

Pada data spasial, nilai latitude yang negatif merupakan representasi koordinat geografis wilayah DIY yang berada di belahan bumi selatan.

## 6. Data Quality Assessment

Pemeriksaan kualitas dilakukan terhadap seluruh file CSV untuk mengetahui struktur data, nilai kosong, dan duplikasi baris secara keseluruhan.

### 6.1 General Data Quality

Hasil pemeriksaan menunjukkan:

| Indikator                  |   Hasil |
| -------------------------- | ------: |
| Jumlah file yang diperiksa |       8 |
| Total baris                | 424.479 |
| Total kolom                |      61 |
| Total missing values       |       0 |
| Total duplikat penuh       |       0 |

Berdasarkan pemeriksaan tersebut, tidak ditemukan nilai kosong maupun duplikasi penuh pada baris data yang dipublikasikan dalam kedelapan file CSV.

Namun, hasil tersebut tidak berarti seluruh data awal tersedia secara lengkap. Beberapa nilai atau baris telah melalui mekanisme suppression sebelum dipublikasikan.

### 6.2 Suppression

Dataset menggunakan mekanisme suppression dengan ambang batas `k = 5`. Mekanisme ini membatasi publikasi data yang tidak memenuhi ambang batas minimum untuk menjaga privasi perangkat.

Berdasarkan `tier1_summary.csv`, ringkasan suppression pada produk data presence adalah:

| Produk             | Total Baris | Baris Dipublikasikan | Suppression |
| ------------------ | ----------: | -------------------: | ----------: |
| A_cell500m_daily   |     518.176 |              183.548 |       64,6% |
| B_kapanewon_hourly |     273.979 |              230.418 |       15,9% |

Sementara itu, berdasarkan `od_summary.csv`, data Origin-Destination memiliki 19.263 baris sebelum suppression dan 9.894 baris yang berhasil dipublikasikan. Persentase baris yang mengalami suppression adalah 48,6%.

Data yang tidak dipublikasikan akibat suppression tidak boleh dianggap memiliki nilai nol.

### 6.3 Temporal Data Quality

Data Origin-Destination memiliki penanda `reduced_quality` untuk menunjukkan periode dengan kualitas data yang berkurang.

Berdasarkan dokumentasi sumber, data OD periode Maret hingga April 2022 memiliki penanda tersebut. Oleh karena itu, analisis kuantitatif OD perlu mempertimbangkan keterbatasan ini. Dokumentasi sumber menyarankan agar analisis kuantitatif OD dapat dibatasi pada periode Desember 2021 hingga Februari 2022.

## 7. Data Limitations

Beberapa keterbatasan dataset yang perlu diperhatikan dalam proses pengolahan dan analisis adalah:

1. **Representasi perangkat:** MAID merepresentasikan perangkat, bukan individu. Jumlah perangkat tidak dapat langsung diinterpretasikan sebagai jumlah penduduk.
2. **Keterwakilan data:** Data berasal dari perangkat yang terekam melalui sumber berbasis aplikasi atau SDK, sehingga tidak selalu mewakili seluruh populasi DIY.
3. **Suppression:** Sebagian data tidak dipublikasikan karena mekanisme perlindungan privasi dengan ambang batas minimum `k = 5`.
4. **Perubahan cakupan temporal:** Jumlah perangkat yang teramati mengalami perubahan sepanjang periode pengamatan. Perbandingan antarwaktu perlu mempertimbangkan perubahan cakupan perangkat.
5. **Kualitas data OD:** Data Origin-Destination pada Maret hingga April 2022 ditandai mengalami penurunan kualitas, sehingga perlu diperlakukan secara hati-hati.
6. **Non-additive device counts:** Perangkat yang sama dapat terhitung pada beberapa wilayah. Oleh karena itu, penjumlahan jumlah perangkat antarwilayah tidak selalu menghasilkan jumlah perangkat unik secara keseluruhan.
7. **Keterbatasan informasi spasial:** Sistem koordinat dan zona UTM yang digunakan perlu dipastikan kembali melalui metadata sumber sebelum melakukan pengolahan spasial lebih lanjut.

## 8. Notes for Further Analysis

Sebelum digunakan dalam tahap preprocessing, integrasi, dan analisis, terdapat beberapa hal yang perlu diperhatikan:

- Kolom tanggal sebaiknya dikonversi menjadi tipe datetime agar dapat digunakan dalam analisis temporal.
- Kode administratif seperti `kab_code`, `origin_kab_code`, dan `dest_kab_code` sebaiknya diperlakukan sebagai identifier bertipe string.
- Penggabungan data berdasarkan wilayah sebaiknya menggunakan kode administratif yang sesuai agar tidak terjadi kesalahan akibat kesamaan nama wilayah.
- Data yang mengalami suppression tidak boleh diisi dengan nilai nol tanpa dasar metodologis.
- Analisis Origin-Destination perlu mempertimbangkan penanda `reduced_quality`.
- Perbandingan jumlah perangkat dengan populasi resmi harus memperhatikan perbedaan antara representasi perangkat dan jumlah penduduk.

Dokumen ini disusun berdasarkan hasil pemeriksaan struktur delapan file CSV dan informasi yang tersedia pada dokumentasi dataset sumber. Penjelasan metodologi yang belum tersedia perlu diverifikasi lebih lanjut sebelum digunakan sebagai dasar analisis.
