
import pandas as pd


def normalize_events(login, files, usb):

    # Add source information to each dataset
    login["source"] = "LOGIN"
    files["source"] = "FILE"
    usb["source"] = "USB"

    # Combine all activity records
    all_events = pd.concat(
        [login, files, usb],
        ignore_index=True
    )

    # Select common event columns
    normalized_events = all_events[
        [
            "timestamp",
            "user",
            "action",
            "object",
            "source",
            "source_reference"
        ]
    ].copy()

    # Sort events by timestamp
    normalized_events = normalized_events.sort_values(
        by="timestamp"
    )

    # Reset row numbers
    normalized_events = normalized_events.reset_index(
        drop=True
    )

    # Generate unique event IDs
    normalized_events.insert(
        0,
        "event_id",
        range(1, len(normalized_events) + 1)
    )

    return normalized_events

