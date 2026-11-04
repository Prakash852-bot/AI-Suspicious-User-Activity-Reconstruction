
import pandas as pd


def reconstruct_timeline(events):

    # Create a copy of the normalized events
    timeline = events.copy()

    # Convert timestamp into datetime format
    timeline["timestamp"] = pd.to_datetime(
        timeline["timestamp"]
    )

    # Sort events by date and time
    timeline = timeline.sort_values(
        by=["timestamp", "user"]
    )

    # Calculate time difference between consecutive events
    timeline["time_difference"] = (
        timeline["timestamp"].diff()
    )

    # Reset event numbering
    timeline = timeline.reset_index(drop=True)

    print("\nUSER ACTIVITY TIMELINE")
    print("=" * 70)

    for _, event in timeline.iterrows():

        print("\nEvent ID:", event["event_id"])
        print("Timestamp:", event["timestamp"])
        print("User:", event["user"])
        print("Activity:", event["action"])
        print("Object:", event["object"])
        print("Source:", event["source"])
        print("Reference:", event["source_reference"])

    return timeline
