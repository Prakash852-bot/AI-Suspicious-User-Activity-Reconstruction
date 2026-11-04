
import hashlib
import pandas as pd
from pathlib import Path

INPUT_FOLDER = Path("input_logs")
OUTPUT_FOLDER = Path("output")

OUTPUT_FOLDER.mkdir(exist_ok=True)


def calculate_sha256(file_path):

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:

        for block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(block)

    return sha256_hash.hexdigest()


def verify_evidence_integrity():

    evidence_files = [
        "login_logs.csv",
        "file_activity.csv",
        "usb_logs.csv"
    ]

    results = []

    for file_name in evidence_files:

        file_path = INPUT_FOLDER / file_name

        if not file_path.exists():
            print(f"File not found: {file_name}")
            continue

        file_hash = calculate_sha256(file_path)

        results.append({
            "file_name": file_name,
            "sha256_hash": file_hash,
            "integrity_status": "Hash generated successfully"
        })

        print("\nEvidence File:", file_name)
        print("SHA-256 Hash:", file_hash)

    integrity_data = pd.DataFrame(results)

    integrity_data.to_csv(
        OUTPUT_FOLDER / "evidence_integrity.csv",
        index=False
    )

    print("\nEvidence integrity verification completed!")

    return integrity_data
