from report_generation import generate_forensic_report
from evidence_integrity import verify_evidence_integrity
from data_ingestion import load_all_logs
from data_normalization import normalize_events
from timeline_reconstruction import reconstruct_timeline
from activity_correlation import detect_suspicious_activity

from database_storage import (
    create_database,
    save_dataframe,
    display_database_records
)

# STEP 1: Load logs
login, files, usb = load_all_logs()

# STEP 2: Normalize events
events = normalize_events(login, files, usb)

# STEP 3: Reconstruct timeline
timeline = reconstruct_timeline(events)

# STEP 4: Detect correlated activities
findings = detect_suspicious_activity(timeline)

# STEP 5: Create database
create_database()

# STEP 6: Save all records
save_dataframe(events, "normalized_events")
save_dataframe(timeline, "activity_timeline")
save_dataframe(findings, "suspicious_findings")

# STEP 7: Display stored records
display_database_records()

print("\nFORENSIC DATABASE OPERATION COMPLETED!")
# STEP 8: Verify evidence integrity
integrity_data = verify_evidence_integrity()

print("\nEVIDENCE INTEGRITY REPORT")
print(integrity_data.to_string(index=False))
# STEP 9: Generate forensic PDF report

generate_forensic_report(
    timeline,
    findings,
    integrity_data
)

print("\nALL PROJECT MODULES EXECUTED SUCCESSFULLY!")
