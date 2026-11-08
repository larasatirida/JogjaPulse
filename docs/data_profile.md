# Data Profile (otomatis)


## home_maids_vs_population_kapanewon.csv
- Baris: 78 | Kolom: 5
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| KAB_KOTA | str | 0 | 5 |  |  | YOGYAKARTA |
| KEC_KAPN | str | 0 | 77 |  |  | GONDOMANAN |
| n_users | int64 | 0 | 78 | 256 | 39609 | 28874 |
| pop_actual | float64 | 0 | 78 | 9190.0 | 130980.0 | 12850.0 |
| ratio | float64 | 0 | 78 | 0.0093590470788429 | 2.247003891050584 | 2.247003891050584 |

## od_home_visits_kapanewon_monthly.csv
- Baris: 9,894 | Kolom: 11
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| month | str | 0 | 5 |  |  | 2021-12 |
| origin_kab_code | float64 | 0 | 5 | 34.01 | 34.71 | 34.01 |
| origin_kab_kota | str | 0 | 5 |  |  | KULON PROGO |
| origin_code | str | 0 | 78 |  |  | 34.01.01 |
| origin_kapanewon | str | 0 | 77 |  |  | TEMON |
| dest_kab_code | float64 | 0 | 5 | 34.01 | 34.71 | 34.01 |
| dest_kab_kota | str | 0 | 5 |  |  | KULON PROGO |
| dest_code | str | 0 | 78 |  |  | 34.01.01 |
| dest_kapanewon | str | 0 | 77 |  |  | TEMON |
| n_maids | int64 | 0 | 566 | 5 | 7961 | 569 |
| reduced_quality | bool | 0 | 2 | False | True | False |

## od_origin_homes_monthly.csv
- Baris: 390 | Kolom: 8
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| month | str | 0 | 5 |  |  | 2021-12 |
| origin_kab_code | float64 | 0 | 5 | 34.01 | 34.71 | 34.01 |
| origin_kab_kota | str | 0 | 5 |  |  | KULON PROGO |
| origin_code | str | 0 | 78 |  |  | 34.01.01 |
| origin_kapanewon | str | 0 | 77 |  |  | TEMON |
| n_homed_maids | int64 | 0 | 307 | 5 | 9495 | 658 |
| n_homed_maids_daytime | int64 | 0 | 316 | 5 | 8428 | 610 |
| reduced_quality | bool | 0 | 2 | False | True | False |

## od_summary.csv
- Baris: 1 | Kolom: 7
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| k | int64 | 0 | 1 | 5 | 5 | 5 |
| min_nights | int64 | 0 | 1 | 2 | 2 | 2 |
| od_rows_total | int64 | 0 | 1 | 19263 | 19263 | 19263 |
| od_rows_published | int64 | 0 | 1 | 9894 | 9894 | 9894 |
| od_rows_suppressed_pct | float64 | 0 | 1 | 48.6 | 48.6 | 48.6 |
| inter_zonal_flow_kept_pct | float64 | 0 | 1 | 95.3 | 95.3 | 95.3 |
| origin_rows_published | int64 | 0 | 1 | 390 | 390 | 390 |

## presence_cell500m_daily.csv
- Baris: 183,548 | Kolom: 7
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| cell_id | str | 0 | 5,715 |  |  | E786_N18255 |
| x_min_utm | int64 | 0 | 167 | 393000 | 479500 | 393000 |
| y_min_utm | int64 | 0 | 129 | 9096000 | 9162000 | 9127500 |
| centroid_lon | float64 | 0 | 5,715 | 110.031602 | 110.816173 | 110.031602 |
| centroid_lat | float64 | 0 | 5,715 | -8.17589 | -7.578602 | -7.8899 |
| date | str | 0 | 151 |  |  | 2021-12-01 |
| n_maids | int64 | 0 | 1,319 | 5 | 10971 | 9 |

⚠️ Nilai negatif: {'centroid_lat': 183548}

## presence_kapanewon_hourly.csv
- Baris: 230,418 | Kolom: 8
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| kab_code | float64 | 0 | 5 | 34.01 | 34.71 | 34.01 |
| kab_kota | str | 0 | 5 |  |  | KULON PROGO |
| kapanewon_code | str | 0 | 78 |  |  | 34.01.01 |
| kapanewon | str | 0 | 77 |  |  | TEMON |
| date | str | 0 | 151 |  |  | 2021-12-01 |
| hour | int64 | 0 | 24 | 0 | 23 | 0 |
| n_maids | int64 | 0 | 1,298 | 5 | 2506 | 16 |
| n_pings | int64 | 0 | 3,195 | 5 | 10210 | 66 |

## tier1_summary.csv
- Baris: 2 | Kolom: 8
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| pings_inside_diy_pct | float64 | 0 | 1 | 100.0 | 100.0 | 100.0 |
| product | str | 0 | 2 |  |  | A_cell500m_daily |
| k | int64 | 0 | 1 | 5 | 5 | 5 |
| rows_total | int64 | 0 | 2 | 273979 | 518176 | 518176 |
| rows_published | int64 | 0 | 2 | 183548 | 230418 | 183548 |
| rows_suppressed_pct | float64 | 0 | 2 | 15.9 | 64.6 | 64.6 |
| maid_presence_suppressed_pct | float64 | 0 | 2 | 0.7 | 6.6 | 6.6 |
| n_cells_published | int64 | 0 | 2 | 78 | 5715 | 5715 |

## validation_night_presence_kapanewon.csv
- Baris: 156 | Kolom: 7
- Duplikat penuh: 0 | Missing total: 0

| Kolom | Tipe | Null | Unik | Min | Max | Contoh |
|---|---|---|---|---|---|---|
| period | str | 0 | 2 |  |  | Dec 2021 - Apr 2022 |
| kab_kota | str | 0 | 5 |  |  | BANTUL |
| kapanewon | str | 0 | 77 |  |  | BAMBANGLIPURO |
| night_presence | float64 | 0 | 156 | 5.631578947368421 | 278.01612903225805 | 23.980036297640652 |
| slots_published_pct | float64 | 0 | 111 | 3.2008830022075054 | 100.0 | 60.81677704194261 |
| n_users | int64 | 0 | 78 | 256 | 39609 | 4497 |
| pop_actual | float64 | 0 | 78 | 9190.0 | 130980.0 | 41070.0 |