"""04_integration.py - Integrasi data Zenodo (hourly) dengan BPS per kapanewon.

Input : data/clean/*.parquet (output 03_preprocessing.py)
Output: data/integrated/*.parquet, data/integrated/jogjapulse.duckdb,
        outputs/validasi_integrasi.md
Key join: kapanewon_code (BUKAN nama; JETIS ada di Bantul dan Kota Yogyakarta).
"""
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "data" / "integrated"
REPORT = ROOT / "outputs" / "validasi_integrasi.md"

NIGHT_HOURS = [22, 23, 0, 1, 2, 3, 4, 5]
# Regime A = Des 2021; B dan C = 2022 (jumlah device berubah 1 Jan & 16 Feb 2022)
REGIME_YEAR = {"A": 2021, "B": 2022, "C": 2022}


def _read(name: str) -> pd.DataFrame:
    return pd.read_parquet(CLEAN / f"{name}.parquet")


def _agg(df: pd.DataFrame, keys: list) -> pd.DataFrame:
    """Agregat kehadiran. Hanya slot yang terbit (device >= 5); slot kosong BUKAN nol."""
    base = (df.groupby(keys)
              .agg(n_slot_terbit=("n_maids", "size"),
                   mean_n_maids=("n_maids", "mean"),
                   mean_share_in_hour=("share_in_hour", "mean"),
                   total_pings=("n_pings", "sum"))
              .reset_index())
    night = (df[df["hour"].isin(NIGHT_HOURS)]
             .groupby(keys)["n_maids"].mean()
             .rename("mean_n_maids_malam").reset_index())
    return base.merge(night, on=keys, how="left", validate="one_to_one")


def run_integration() -> None:
    log = []

    def note(msg: str) -> None:
        print(msg)
        log.append(msg)

    dim = _read("dim_kapanewon")
    bps = _read("bps_population_kapanewon_diy_2021_2022")
    hourly = _read("presence_kapanewon_hourly")
    hm = _read("home_maids_vs_population_kapanewon")

    # ---- Validasi key ----
    assert not dim["kapanewon_code"].duplicated().any(), "dim: kode duplikat"
    assert not bps.duplicated(["kapanewon_code", "tahun"]).any(), "bps: key duplikat"
    jetis = dim[dim["kapanewon"].str.upper() == "JETIS"]
    assert len(jetis) == 2, "JETIS harus 2 baris (Bantul & Kota Yogyakarta)"
    kode = {"hourly": set(hourly["kapanewon_code"]), "bps": set(bps["kapanewon_code"]),
            "hm": set(hm["kapanewon_code"])}
    for nama, s in kode.items():
        selisih1, selisih2 = s - set(dim["kapanewon_code"]), set(dim["kapanewon_code"]) - s
        note(f"- Anti-join {nama} vs dim: {len(selisih1)} kode hanya di {nama}, "
             f"{len(selisih2)} kode hanya di dim")
        assert not selisih1 and not selisih2, f"kode tidak cocok: {nama}"
    note(f"- JETIS: {len(jetis)} baris, kode {', '.join(jetis['kapanewon_code'])}")

    # ---- Join per jam + BPS (kapanewon_code + tahun) ----
    hourly["tahun"] = hourly["date"].dt.year.astype("int16")
    bps_j = bps[["kapanewon_code", "tahun", "laki_laki", "perempuan", "total"]].rename(
        columns={"total": "pop_bps", "laki_laki": "pop_bps_laki",
                 "perempuan": "pop_bps_perempuan"})
    n0 = len(hourly)
    integrated_hourly = hourly.merge(bps_j, on=["kapanewon_code", "tahun"],
                                     how="left", validate="many_to_one")
    note(f"- Join per jam: {n0:,} baris sebelum, {len(integrated_hourly):,} sesudah")
    assert len(integrated_hourly) == n0, "baris membengkak setelah join"
    assert integrated_hourly["pop_bps"].notna().all(), "ada baris tanpa pasangan BPS"
    assert not integrated_hourly.duplicated(["kapanewon_code", "datetime"]).any()
    note("- Baris tanpa pasangan BPS: 0; duplikat (kode, datetime): 0")

    # ---- Agregat per kapanewon x tahun (granularitas BPS) ----
    agg_year = _agg(integrated_hourly, ["kapanewon_code", "tahun"])
    integrated_kapanewon = (
        dim.merge(bps_j, on="kapanewon_code", how="left", validate="one_to_many")
           .merge(agg_year, on=["kapanewon_code", "tahun"], how="left", validate="one_to_one")
           .merge(hm[["kapanewon_code", "n_users", "ratio", "ratio_gt_1"]],
                  on="kapanewon_code", how="left", validate="many_to_one"))
    integrated_kapanewon["maids_per_1000_penduduk"] = (
        integrated_kapanewon["mean_n_maids"] / integrated_kapanewon["pop_bps"] * 1000)
    assert len(integrated_kapanewon) == 156
    note(f"- integrated_kapanewon: {integrated_kapanewon.shape[0]} baris "
         f"(78 kapanewon x 2 tahun), tanpa kehadiran: "
         f"{integrated_kapanewon['mean_n_maids'].isna().sum()}")

    # ---- Agregat per kapanewon x supply_regime (aman untuk bandingkan antar waktu) ----
    agg_regime = _agg(integrated_hourly, ["kapanewon_code", "supply_regime"])
    agg_regime["tahun_pop"] = agg_regime["supply_regime"].map(REGIME_YEAR).astype("int16")
    agg_regime = (agg_regime
                  .merge(bps_j[["kapanewon_code", "tahun", "pop_bps"]],
                         left_on=["kapanewon_code", "tahun_pop"],
                         right_on=["kapanewon_code", "tahun"],
                         how="left", validate="many_to_one")
                  .drop(columns="tahun")
                  .merge(dim, on="kapanewon_code", how="left", validate="many_to_one"))
    agg_regime["maids_per_1000_penduduk"] = (
        agg_regime["mean_n_maids"] / agg_regime["pop_bps"] * 1000)
    assert len(agg_regime) == 78 * 3 and agg_regime["pop_bps"].notna().all()
    note(f"- agg_regime: {len(agg_regime)} baris (78 kapanewon x 3 regime)")

    # ---- Simpan ----
    OUT.mkdir(parents=True, exist_ok=True)
    integrated_hourly.to_parquet(OUT / "integrated_hourly.parquet", index=False)
    integrated_kapanewon.to_parquet(OUT / "integrated_kapanewon.parquet", index=False)
    agg_regime.to_parquet(OUT / "integrated_kapanewon_regime.parquet", index=False)

    tabel = {
        "dim_kapanewon": dim,
        "bps_population": bps,
        "fact_presence_hourly": integrated_hourly,
        "integrated_kapanewon": integrated_kapanewon,
        "integrated_kapanewon_regime": agg_regime,
        "od_home_visits_monthly": _read("od_home_visits_kapanewon_monthly"),
        "od_origin_homes_monthly": _read("od_origin_homes_monthly"),
        "fact_presence_cell500m_daily": _read("presence_cell500m_daily"),
    }
    con = duckdb.connect(str(OUT / "jogjapulse.duckdb"))
    for nama, df in tabel.items():
        con.register("tmp_df", df)
        con.execute(f"CREATE OR REPLACE TABLE {nama} AS SELECT * FROM tmp_df")
        con.unregister("tmp_df")
    note(f"- Tabel DuckDB: {', '.join(tabel)}")
    con.close()

    # ---- Laporan validasi ----
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "# Validasi Integrasi\n\n" + "\n".join(log) + "\n\n"
        "## Catatan penting\n"
        "- Join memakai `kapanewon_code`, bukan nama (JETIS ada di Bantul dan Kota Yogyakarta).\n"
        "- Slot jam kosong = disensor (device < 5), bukan nol; tidak diisi.\n"
        "- `mean_n_maids` antar tahun/regime TIDAK sebanding (jumlah device berubah "
        "1 Jan dan 16 Feb 2022; 2021 hanya Desember). Untuk perbandingan antar waktu "
        "pakai `mean_share_in_hour`.\n"
        "- `n_users`, `ratio` berlaku untuk seluruh periode; jangan dijumlahkan antar tahun.\n"
        "- Malam = jam 22-05. Data OD Mar-Apr 2022 berkualitas rendah (`reduced_quality`).\n",
        encoding="utf-8")
    print(f"Laporan: {REPORT}")


if __name__ == "__main__":
    run_integration()