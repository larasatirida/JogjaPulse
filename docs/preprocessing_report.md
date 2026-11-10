# Laporan Preprocessing

| File | Pengecekan | Hasil |
|---|---|---|
| kapanewon_lookup | jumlah kapanewon | 78 |
| dim_kapanewon | disimpan | 78 baris x 4 kolom |
| presence_kapanewon_hourly | baris mentah | 230418 |
| presence_kapanewon_hourly | missing | 0 |
| presence_kapanewon_hourly | duplikat | 0 |
| presence_kapanewon_hourly | kode/nama tidak cocok (kapanewon_code) | 0 |
| presence_kapanewon_hourly | n_pings < n_maids | 0 |
| presence_kapanewon_hourly | slot terbit / teoritis | 230,418 / 282,672 (81.5%) |
| coverage_kapanewon_hourly | disimpan | 11,451 baris x 6 kolom |
| presence_kapanewon_hourly | disimpan | 230,418 baris x 16 kolom |
| presence_cell500m_daily | baris mentah | 183548 |
| presence_cell500m_daily | missing | 0 |
| presence_cell500m_daily | duplikat | 0 |
| presence_cell500m_daily | centroid di dalam bbox DIY | True |
| presence_cell500m_daily | disimpan | 183,548 baris x 13 kolom |
| od_origin_homes_monthly | baris mentah | 390 |
| od_origin_homes_monthly | missing | 0 |
| od_origin_homes_monthly (origin) | kode/nama tidak cocok (kapanewon_code) | 0 |
| od_home_visits_kapanewon_monthly | baris mentah | 9894 |
| od_home_visits_kapanewon_monthly | missing | 0 |
| od_home_visits_kapanewon_monthly | duplikat | 0 |
| od_home_visits_kapanewon_monthly (origin) | kode/nama tidak cocok (kapanewon_code) | 0 |
| od_home_visits_kapanewon_monthly (dest) | kode/nama tidak cocok (kapanewon_code) | 0 |
| od_home_visits_kapanewon_monthly | reduced_quality = True | 2022 |
| od_home_visits_kapanewon_monthly | baris tanpa pembagi | 0 |
| od_home_visits_kapanewon_monthly | disimpan | 9,894 baris x 14 kolom |
| od_origin_homes_monthly | disimpan | 390 baris x 8 kolom |
| home_maids_vs_population_kapanewon | baris tanpa kapanewon_code | 0 |
| home_maids_vs_population_kapanewon | selisih maks ratio | 1.11e-16 |
| home_maids_vs_population_kapanewon | disimpan | 78 baris x 8 kolom |
| validation_night_presence_kapanewon | isi kolom period | {'Dec 2021 - Apr 2022': 78, 'Dec 2021 - Jan 2022': 78} |
| validation_night_presence_kapanewon | baris tanpa kapanewon_code | 0 |
| validation_night_presence_kapanewon | missing | 0 |
| validation_night_presence_kapanewon | disimpan | 156 baris x 9 kolom |
| tier1_summary | disimpan | 2 baris x 8 kolom |
| od_summary | disimpan | 1 baris x 7 kolom |
| bps_population_kapanewon_diy_2021_2022 | baris mentah | 156 |
| bps_population_kapanewon_diy_2021_2022 | kode/nama tidak cocok (kapanewon_code) | 0 |
| bps_population_kapanewon_diy_2021_2022 | NaN laki_laki/perempuan | 36 |
| bps_population_kapanewon_diy_2021_2022 | duplikat | 0 |
| bps_population_kapanewon_diy_2021_2022 | flag_total_mismatch = True | 7 |
| bps_population_kapanewon_diy_2021_2022 | disimpan | 156 baris x 10 kolom |
