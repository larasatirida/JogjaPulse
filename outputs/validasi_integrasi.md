# Validasi Integrasi

- Anti-join hourly vs dim: 0 kode hanya di hourly, 0 kode hanya di dim
- Anti-join bps vs dim: 0 kode hanya di bps, 0 kode hanya di dim
- Anti-join hm vs dim: 0 kode hanya di hm, 0 kode hanya di dim
- JETIS: 2 baris, kode 34.02.09, 34.71.02
- Join per jam: 230,418 baris sebelum, 230,418 sesudah
- Baris tanpa pasangan BPS: 0; duplikat (kode, datetime): 0
- integrated_kapanewon: 156 baris (78 kapanewon x 2 tahun), tanpa kehadiran: 0
- agg_regime: 234 baris (78 kapanewon x 3 regime)
- Tabel DuckDB: dim_kapanewon, bps_population, fact_presence_hourly, integrated_kapanewon, integrated_kapanewon_regime, od_home_visits_monthly, od_origin_homes_monthly, fact_presence_cell500m_daily

## Catatan penting
- Join memakai `kapanewon_code`, bukan nama (JETIS ada di Bantul dan Kota Yogyakarta).
- Slot jam kosong = disensor (device < 5), bukan nol; tidak diisi.
- `mean_n_maids` antar tahun/regime TIDAK sebanding (jumlah device berubah 1 Jan dan 16 Feb 2022; 2021 hanya Desember). Untuk perbandingan antar waktu pakai `mean_share_in_hour`.
- `n_users`, `ratio` berlaku untuk seluruh periode; jangan dijumlahkan antar tahun.
- Malam = jam 22-05. Data OD Mar-Apr 2022 berkualitas rendah (`reduced_quality`).
