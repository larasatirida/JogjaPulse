from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "zenodo"
INVENTORY_DIR = BASE_DIR / "outputs" / "inventory"
QUALITY_DIR = BASE_DIR / "outputs" / "quality_reports"
DOCS_DIR = BASE_DIR / "docs"

for d in (INVENTORY_DIR, QUALITY_DIR, DOCS_DIR):
    d.mkdir(parents=True, exist_ok=True)


def read_csv_file(file_path):
    for enc in ("utf-8-sig", "utf-8", "latin1"):
        try:
            return pd.read_csv(file_path, encoding=enc, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise ValueError("Encoding tidak dikenali")


inventory, quality, dictionary = [], [], []
md_lines = ["# Data Profile (otomatis)\n"]

csv_files = sorted(DATA_DIR.glob("*.csv"))
if not csv_files:
    raise FileNotFoundError(f"Tidak ada CSV di {DATA_DIR}")

for fp in csv_files:
    print(f"\nMemeriksa: {fp.name}")
    try:
        df = read_csv_file(fp)
        n, k = len(df), df.shape[1]
        dup = int(df.duplicated().sum())
        miss = int(df.isna().sum().sum())

        inventory.append({
            "file_name": fp.name,
            "file_size_kb": round(fp.stat().st_size / 1024, 2),
            "total_rows": n, "total_columns": k,
            "duplicate_rows": dup,
            "total_missing_values": miss,
            "status": "Success",
        })

        md_lines += [f"\n## {fp.name}",
                     f"- Baris: {n:,} | Kolom: {k}",
                     f"- Duplikat penuh: {dup:,} | Missing total: {miss:,}\n",
                     "| Kolom | Tipe | Null | Unik | Min | Max | Contoh |",
                     "|---|---|---|---|---|---|---|"]

        neg_cols = {}
        for col in df.columns:
            s = df[col]
            non_null = s.dropna()
            is_num = pd.api.types.is_numeric_dtype(s)

            mn = non_null.min() if is_num and not non_null.empty else ""
            mx = non_null.max() if is_num and not non_null.empty else ""
            ex = str(non_null.iloc[0]) if not non_null.empty else ""

            if is_num and (s < 0).any():
                neg_cols[col] = int((s < 0).sum())

            quality.append({
                "file_name": fp.name, "column_name": col,
                "data_type": str(s.dtype), "total_rows": n,
                "missing_values": int(s.isna().sum()),
                "missing_percentage": round(s.isna().sum() / n * 100, 2) if n else 0,
                "unique_values": int(s.nunique()),
                "min": mn, "max": mx,
                "duplicate_rows_in_file": dup,
            })
            dictionary.append({
                "file_name": fp.name, "column_name": col,
                "data_type": str(s.dtype),
                "meaning": "", "unit": "",
                "example_value": ex,
            })
            md_lines.append(f"| {col} | {s.dtype} | {s.isna().sum():,} | {s.nunique():,} | {mn} | {mx} | {ex[:40]} |")

        if neg_cols:
            md_lines.append(f"\n⚠️ Nilai negatif: {neg_cols}")

    except Exception as e:
        inventory.append({"file_name": fp.name, "status": f"Failed: {e}"})
        print(f"  Gagal: {e}")

pd.DataFrame(inventory).to_csv(INVENTORY_DIR / "zenodo_inventory.csv", index=False)
pd.DataFrame(quality).to_csv(QUALITY_DIR / "data_quality_report.csv", index=False)
pd.DataFrame(dictionary).to_csv(QUALITY_DIR / "data_dictionary_template.csv", index=False)
(DOCS_DIR / "data_profile.md").write_text("\n".join(md_lines), encoding="utf-8")

print("\nSelesai. Output:")
print("- outputs/inventory/zenodo_inventory.csv")
print("- outputs/quality_reports/data_quality_report.csv")
print("- outputs/quality_reports/data_dictionary_template.csv")
print("- docs/data_profile.md")