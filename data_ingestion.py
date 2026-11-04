
import pandas as pd
from pathlib import Path

INPUT_FOLDER = Path("input_logs")

REQUIRED_COLUMNS = [
    "timestamp",
    "user",
    "action",
    "object",
    "source_reference"
]


def load_and_validate(file_name):
    file_path = INPUT_FOLDER / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    data = pd.read_csv(file_path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {file_name}: {missing_columns}"
        )

    data["timestamp"] = pd.to_datetime(
        data["timestamp"], errors="coerce"
    )

    if data["timestamp"].isna().any():
        raise ValueError(f"Invalid timestamps in {file_name}")

    if data[["user", "action", "object"]].isna().any().any():
        raise ValueError(f"Empty required values in {file_name}")

    print(f"Successfully validated: {file_name}")
    return data


def load_all_logs():
    login_data = load_and_validate("login_logs.csv")
    file_data = load_and_validate("file_activity.csv")
    usb_data = load_and_validate("usb_logs.csv")

    return login_data, file_data, usb_data
