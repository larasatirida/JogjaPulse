from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
LOG: list[dict] = []

K_MIN = 5 # ambang k-anonymity dataset Zenodo
DATE_START, DATE_END = pd.Timestamp("2021-12-01"), pd.Timestamp("2022-04-30")
BREAK_1, BREAK_2 = pd.Timestamp("2022-01-01"), pd.Timestamp("2022-02-16")
ANOMALY_DAYS = [pd.Timestamp("2022-03-08")] 

# Helper
def log(file: str, check: str, result) -> None:
    LOG.append({"file": file, "pengecekan": check, "hasil": str(result)})
    print(f"[{file}] {check}: {result}")

def read_csv_safe(path: Path, **kw) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "latin1"):
        try:
            return pd.read_csv(path, encoding=enc, **kw)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Encoding tidak dikenali: {path}")

def normalize_kab(s: pd.Series) -> pd.Series:
    s = s.astype("string").str.upper().str.strip()
    s = s.str.replace(r"^(KAB\.?|KABUPATEN|KOTA)\s+", "", regex=True)
    return s.str.replace(r"\s+", " ", regex=True)

def normalize_kec(s: pd.Series) -> pd.Series:
    # "KOTA" di nama kapanewon (KOTAGEDE) tidak dibuang
    s = s.astype("string").str.upper().str.strip()
    s = s.str.replace(r"^(KEC\.?|KAPANEWON|KEMANTREN)\s*", "", regex=True)
    return s.str.replace(r"\s+", " ", regex=True)

def check_codes(df: pd.DataFrame, code_col: str, name_col: str, lookup: pd.DataFrame, name: str) -> None:
    ref = lookup[["kapanewon_code", "kapanewon"]].rename(
        columns={"kapanewon_code": "_code_ref", "kapanewon": "_name_ref"})
    m = df[[code_col, name_col]].drop_duplicates().merge(
        ref, left_on=code_col, right_on="_code_ref", how="left")
    bad = m[m["_name_ref"].isna() | (m[name_col] != m["_name_ref"])]
    log(name, f"kode/nama tidak cocok ({code_col})", len(bad))
    assert bad.empty, bad

def add_code(df: pd.DataFrame, kab_col: str, kec_col: str, lookup: pd.DataFrame, name: str) -> pd.DataFrame:
    # join pakai (kab_kota, kapanewon) karena ada nama kapanewon yang kembar (Jetis)
    df = df.copy()
    df["kab_kota"] = normalize_kab(df[kab_col])
    df["kapanewon"] = normalize_kec(df[kec_col])
    out = df.merge(lookup, on=["kab_kota", "kapanewon"], how="left", validate="m:1")
    log(name, "baris tanpa kapanewon_code", int(out["kapanewon_code"].isna().sum()))
    assert out["kapanewon_code"].notna().all()
    return out

def add_supply_flags(df: pd.DataFrame) -> pd.DataFrame:
    df["supply_regime"] = np.select([df["date"] < BREAK_1, df["date"] < BREAK_2], ["A", "B"], default="C")
    df["is_anomaly_day"] = df["date"].isin(ANOMALY_DAYS)
    return df

def save(df: pd.DataFrame, name: str) -> None:
    CLEAN.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CLEAN / f"{name}.parquet", index=False)
    if len(df) < 20_000:
        df.to_csv(CLEAN / f"{name}.csv", index=False)
    log(name, "disimpan", f"{len(df):,} baris x {df.shape[1]} kolom")

# Dimensi wilayah
def clean_lookup() -> pd.DataFrame:
    lk = pd.read_csv(RAW / "boundaries" / "kapanewon_lookup.csv", dtype=str)
    lk["kab_kota"] = normalize_kab(lk["kab_kota"])
    lk["kapanewon"] = normalize_kec(lk["kapanewon"])
    lk["kab_code"] = lk["kapanewon_code"].str[:5]
    assert lk["kapanewon_code"].is_unique
    assert not lk.duplicated(["kab_kota", "kapanewon"]).any()
    log("kapanewon_lookup", "jumlah kapanewon", len(lk))
    save(lk, "dim_kapanewon")
    return lk

# Zenodo
def clean_hourly(lk: pd.DataFrame) -> pd.DataFrame:
    f = "presence_kapanewon_hourly"
    df = read_csv_safe(RAW / "zenodo" / f"{f}.csv", dtype={"kab_code": str, "kapanewon_code": str})
    log(f, "baris mentah", len(df))
    log(f, "missing", int(df.isna().sum().sum()))
    log(f, "duplikat", int(df.duplicated(["kapanewon_code", "date", "hour"]).sum()))
    df = df.drop_duplicates(["kapanewon_code", "date", "hour"])

    df["kab_kota"] = normalize_kab(df["kab_kota"])
    df["kapanewon"] = normalize_kec(df["kapanewon"])
    check_codes(df, "kapanewon_code", "kapanewon", lk, f)

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["hour"] = df["hour"].astype("int8")
    df["n_maids"] = df["n_maids"].astype("int32")
    df["n_pings"] = df["n_pings"].astype("int32")

    # validasi
    assert df["hour"].between(0, 23).all()
    assert df["date"].between(DATE_START, DATE_END).all()
    assert (df["n_maids"] >= K_MIN).all()
    log(f, "n_pings < n_maids", int((df["n_pings"] < df["n_maids"]).sum()))

    # kolom turunan
    df["datetime"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")
    df["dayofweek"] = df["date"].dt.dayofweek.astype("int8") # 0 = Senin
    df["is_weekend"] = df["dayofweek"] >= 5
    df["month"] = df["date"].dt.strftime("%Y-%m")
    df["pings_per_maid"] = (df["n_pings"] / df["n_maids"]).astype("float32")
    df = add_supply_flags(df)
    tot = df.groupby("datetime")["n_maids"].transform("sum")
    df["share_in_hour"] = (df["n_maids"] / tot).astype("float32")

    # slot yang tidak ada = disuppress (k-anonymity), bukan nol
    expected = lk["kapanewon_code"].nunique() * df["date"].nunique() * 24
    log(f, "slot terbit / teoritis", f"{len(df):,} / {expected:,} ({len(df) / expected:.1%})")
    cov = (df.groupby(["kapanewon_code", "date"]).size().rename("jam_terbit").reset_index()
           .merge(lk[["kapanewon_code", "kab_kota", "kapanewon"]], on="kapanewon_code"))
    cov["jam_terbit_pct"] = (cov["jam_terbit"] / 24).round(3)
    save(cov, "coverage_kapanewon_hourly")

    cols = ["kapanewon_code", "kab_code", "kab_kota", "kapanewon", "datetime", "date", "hour",
            "dayofweek", "is_weekend", "month", "n_maids", "n_pings",
            "pings_per_maid", "share_in_hour", "supply_regime", "is_anomaly_day"]
    df = df[cols].sort_values(["kapanewon_code", "datetime"]).reset_index(drop=True)
    save(df, f)
    return df


def clean_cell():
    f = "presence_cell500m_daily"
    df = read_csv_safe(RAW / "zenodo" / f"{f}.csv", dtype={"cell_id": str}, low_memory=False)
    log(f, "baris mentah", len(df))
    log(f, "missing", int(df.isna().sum().sum()))
    log(f, "duplikat", int(df.duplicated(["cell_id", "date"]).sum()))
    df["cell_id"] = df["cell_id"].str.strip().str.upper()
    df = df.drop_duplicates(["cell_id", "date"])
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    assert df["date"].between(DATE_START, DATE_END).all()
    assert (df["n_maids"] >= K_MIN).all()

    df["n_maids"] = df["n_maids"].astype("int32")
    for c in ("x_min_utm", "y_min_utm"):
        df[c] = df[c].astype("int32")
    df["dayofweek"] = df["date"].dt.dayofweek.astype("int8")
    df["is_weekend"] = df["dayofweek"] >= 5
    df["month"] = df["date"].dt.strftime("%Y-%m")
    df = add_supply_flags(df)
    df["share_in_day"] = (df["n_maids"] / df.groupby("date")["n_maids"].transform("sum")).astype("float32")

    inside = df["centroid_lon"].between(109.9, 111.0).all() and df["centroid_lat"].between(-8.3, -7.4).all()
    log(f, "centroid di dalam bbox DIY", bool(inside))
    df = df.sort_values(["cell_id", "date"]).reset_index(drop=True)
    save(df, f)
    return df

def _clean_od_common(df, prefixes, lk, f):
    df = df.copy()
    for p in prefixes:
        df[f"{p}_kab_kota"] = normalize_kab(df[f"{p}_kab_kota"])
        df[f"{p}_kapanewon"] = normalize_kec(df[f"{p}_kapanewon"])
        check_codes(df.rename(columns={f"{p}_code": "kapanewon_code", f"{p}_kapanewon": "kapanewon"}),
                    "kapanewon_code", "kapanewon", lk, f"{f} ({p})")
    df["month"] = pd.to_datetime(df["month"].astype("string").str.strip(), format="%Y-%m") # tgl 1 tiap bulan
    df["reduced_quality"] = df["reduced_quality"].astype(bool)
    return df

def clean_od(lk):
    # denominator: rumah per kapanewon asal
    f2 = "od_origin_homes_monthly"
    d2 = read_csv_safe(RAW / "zenodo" / f"{f2}.csv", dtype={"origin_kab_code": str, "origin_code": str})
    log(f2, "baris mentah", len(d2))
    log(f2, "missing", int(d2.isna().sum().sum()))
    d2 = d2.drop_duplicates(["month", "origin_code"])
    d2 = _clean_od_common(d2, ["origin"], lk, f2)
    for c in ["n_homed_maids", "n_homed_maids_daytime"]:
        d2[c] = d2[c].astype("int32")
    d2 = d2.sort_values(["month", "origin_code"]).reset_index(drop=True)

    # unjungan origin -> destination
    f1 = "od_home_visits_kapanewon_monthly"
    d1 = read_csv_safe(RAW / "zenodo" / f"{f1}.csv",
                       dtype={"origin_kab_code": str, "dest_kab_code": str, "origin_code": str, "dest_code": str})
    log(f1, "baris mentah", len(d1))
    log(f1, "missing", int(d1.isna().sum().sum()))
    log(f1, "duplikat", int(d1.duplicated(["month", "origin_code", "dest_code"]).sum()))
    d1 = d1.drop_duplicates(["month", "origin_code", "dest_code"])
    d1 = _clean_od_common(d1, ["origin", "dest"], lk, f1)
    d1["n_maids"] = d1["n_maids"].astype("int32")
    assert (d1["n_maids"] >= K_MIN).all()
    d1["is_intra"] = d1["origin_code"] == d1["dest_code"] # kunjungan di kapanewon asal sendiri
    log(f1, "reduced_quality = True", int(d1["reduced_quality"].sum()))

    # share_of_origin = n_maids / device berumah di asal yang teramati siang hari
    d1 = d1.merge(d2[["month", "origin_code", "n_homed_maids_daytime"]],
                  on=["month", "origin_code"], how="left", validate="m:1")
    log(f1, "baris tanpa pembagi", int(d1["n_homed_maids_daytime"].isna().sum()))
    d1["share_of_origin"] = (d1["n_maids"] / d1["n_homed_maids_daytime"]).astype("float32")
    d1 = d1.sort_values(["month", "origin_code", "dest_code"]).reset_index(drop=True)

    save(d1, f1)
    save(d2, f2)
    return d1, d2

def clean_home_vs_pop(lk: pd.DataFrame) -> pd.DataFrame:
    f = "home_maids_vs_population_kapanewon"
    df = read_csv_safe(RAW / "zenodo" / f"{f}.csv")
    df = add_code(df, "KAB_KOTA", "KEC_KAPN", lk, f)
    df = df.drop(columns=[c for c in ["KAB_KOTA", "KEC_KAPN"] if c in df])
    assert df["kapanewon_code"].is_unique and len(df) == len(lk)
    df["n_users"] = df["n_users"].astype("int32")
    df["pop_actual"] = df["pop_actual"].astype("float64")
    diff = (df["ratio"] - df["n_users"] / df["pop_actual"]).abs().max()
    log(f, "selisih maks ratio", f"{diff:.2e}")
    df["ratio_gt_1"] = df["ratio"] > 1 # device lebih banyak dari penduduk
    df = df[["kapanewon_code", "kab_code", "kab_kota", "kapanewon",
             "n_users", "pop_actual", "ratio", "ratio_gt_1"]]
    save(df.sort_values("kapanewon_code").reset_index(drop=True), f)
    return df

def clean_validation(lk: pd.DataFrame) -> pd.DataFrame:
    f = "validation_night_presence_kapanewon"
    df = read_csv_safe(RAW / "zenodo" / f"{f}.csv")
    df["period"] = df["period"].astype("string").str.strip()
    log(f, "isi kolom period", df["period"].value_counts().to_dict())
    df = add_code(df, "kab_kota", "kapanewon", lk, f)
    for c in ["night_presence", "slots_published_pct", "pop_actual"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["n_users"] = df["n_users"].astype("int32")
    log(f, "missing", int(df.isna().sum().sum()))
    df = df[["kapanewon_code", "kab_code", "kab_kota", "kapanewon", "period",
             "night_presence", "slots_published_pct", "n_users", "pop_actual"]]
    save(df.sort_values(["period", "kapanewon_code"]).reset_index(drop=True), f)
    return df

def copy_summaries() -> None:
    for name in ("tier1_summary", "od_summary"):
        p = RAW / "zenodo" / f"{name}.csv"
        if p.exists():
            save(read_csv_safe(p), name)

# BPS
def clean_bps(lk: pd.DataFrame) -> pd.DataFrame:
    f = "bps_population_kapanewon_diy_2021_2022"
    df = read_csv_safe(RAW / "bps" / f"{f}.csv", dtype={"kapanewon_code": str})
    log(f, "baris mentah", len(df))
    df["kab_kota"] = normalize_kab(df["kab_kota"])
    df["kapanewon"] = normalize_kec(df["kapanewon"])
    check_codes(df, "kapanewon_code", "kapanewon", lk, f)
    df["tahun"] = df["tahun"].astype("int16")
    for c in ["laki_laki", "perempuan", "total", "total_published"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    assert df["total"].notna().all()
    log(f, "NaN laki_laki/perempuan", int(df["laki_laki"].isna().sum()))
    log(f, "duplikat", int(df.duplicated(["kapanewon_code", "tahun"]).sum()))
    df = df.drop_duplicates(["kapanewon_code", "tahun"])
    df["flag_total_mismatch"] = df["flag_total_mismatch"].astype(bool)
    log(f, "flag_total_mismatch = True", int(df["flag_total_mismatch"].sum()))
    df = df.drop(columns=["sumber"], errors="ignore").merge(lk[["kapanewon_code", "kab_code"]], on="kapanewon_code")
    save(df.sort_values(["tahun", "kapanewon_code"]).reset_index(drop=True), f)
    return df

# Laporan + pipeline
def write_report() -> None:
    out = ROOT / "docs" / "preprocessing_report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Laporan Preprocessing", "", "| File | Pengecekan | Hasil |", "|---|---|---|"]
    lines += [f"| {r['file']} | {r['pengecekan']} | {r['hasil']} |" for r in LOG]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

def run_all() -> None:
    LOG.clear()
    lk = clean_lookup()
    clean_hourly(lk)
    clean_cell()
    clean_od(lk)
    clean_home_vs_pop(lk)
    clean_validation(lk)
    copy_summaries()
    clean_bps(lk)
    write_report()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=RAW)
    ap.add_argument("--clean", type=Path, default=CLEAN)
    args = ap.parse_args()
    RAW, CLEAN = args.raw, args.clean
    run_all()