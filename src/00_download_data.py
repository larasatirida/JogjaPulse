import requests
import hashlib
from pathlib import Path

RECORD_ID = "23157460"
API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"
OUTPUT_DIR = Path("data/raw/zenodo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 1 << 20  # 1 MB untuk MD5 & download


def calculate_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            md5.update(chunk)
    return md5.hexdigest()


def get_metadata():
    r = requests.get(API_URL, timeout=(10, 60))
    r.raise_for_status()
    return r.json()


def download_file(file_info):
    filename = file_info["key"]
    download_url = file_info["links"]["self"]
    expected = file_info["checksum"].split(":")[-1]
    file_path = OUTPUT_DIR / filename

    print(f"\nMemproses: {filename}")

    # SKIP jika sudah ada & sudah terverifikasi
    if file_path.exists():
        if calculate_md5(file_path) == expected:
            print("Status: SKIPPED (sudah ada & valid)")
            return True
        print("File lama tidak valid, download ulang...")
        file_path.unlink()

    r = requests.get(download_url, stream=True, timeout=(10, 300))
    r.raise_for_status()

    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    actual = calculate_md5(file_path)
    if actual == expected:
        print(f"Status: VERIFIED ({actual})")
        return True

    print(f"Status: FAILED\n  expected={expected}\n  actual  ={actual}")
    file_path.unlink()
    return False


def main():
    print("Mengambil metadata Zenodo...")
    metadata = get_metadata()
    print("Dataset:", metadata["metadata"]["title"])
    print("Jumlah file:", len(metadata["files"]))

    results = {f["key"]: download_file(f) for f in metadata["files"]}

    print("\nhasil download")
    ok = [k for k, v in results.items() if v]
    fail = [k for k, v in results.items() if not v]
    print(f"Berhasil: {len(ok)}")
    print(f"Gagal   : {len(fail)}")
    for k in fail:
        print(f"  - {k}")

    if fail:
        raise RuntimeError(f"{len(fail)} file gagal diverifikasi.")


if __name__ == "__main__":
    main()