"""Jalankan seluruh pipeline: python src/run_pipeline.py [--with-download]"""
import argparse
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
STEPS = [
    ("download", "00_download_data.py"),
    ("preprocessing", "03_preprocessing.py"),
    ("integration", "04_integration.py"),
]

parser = argparse.ArgumentParser()
parser.add_argument("--with-download", action="store_true",
                    help="unduh ulang data Zenodo/BPS (lewati jika data raw sudah ada)")
args = parser.parse_args()

for nama, file in STEPS:
    if nama == "download" and not args.with_download:
        print("[skip] download (pakai --with-download untuk menjalankan)")
        continue
    print(f"\n=== {nama}: {file} ===")
    subprocess.run([sys.executable, str(SRC / file)], check=True)

print("\nPipeline selesai.")