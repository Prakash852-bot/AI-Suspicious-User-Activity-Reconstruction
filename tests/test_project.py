
import sys
from pathlib import Path

import pandas as pd

# Add the project folder to Python's import path
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from data_ingestion import load_all_logs
from data_normalization import normalize_events
from timeline_reconstruction import reconstruct_timeline
from activity_correlation import detect_suspicious_activity
from evidence_integrity import calculate_sha256


def get_test_data():

    login, files, usb = load_all_logs()

    events = normalize_events(login, files, usb)

    timeline = reconstruct_timeline(events)

    return events, timeline


# TEST 1: Check log loading
def test_log_loading():

    login, files, usb = load_all_logs()

    assert not login.empty
    assert not files.empty
    assert not usb.empty


# TEST 2: Check event normalization
def test_event_normalization():

    events, timeline = get_test_data()

    assert not events.empty
    assert "event_id" in events.columns
    assert "source" in events.columns


# TEST 3: Check timeline reconstruction
def test_timeline_reconstruction():

    events, timeline = get_test_data()

    assert timeline["timestamp"].is_monotonic_increasing


# TEST 4: Check activity correlation
def test_activity_correlation():

    events, timeline = get_test_data()

    findings = detect_suspicious_activity(timeline)

    assert isinstance(findings, pd.DataFrame)
    assert "finding" in findings.columns


# TEST 5: Check evidence hash generation
def test_evidence_hash():

    test_file = Path("input_logs/login_logs.csv")

    file_hash = calculate_sha256(test_file)

    assert len(file_hash) == 64
    assert all(
        character in "0123456789abcdef"
        for character in file_hash
    )


# TEST 6: Check PDF report generation
def test_pdf_report_exists():

    report = Path(
        "output/forensic_investigation_report.pdf"
    )

    assert report.exists()
    assert report.stat().st_size > 0
