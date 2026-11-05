
from rag_engine import retrieve_context


def generate_rag_explanation(activity_details):

    context = retrieve_context(
        "digital forensics suspicious login sensitive file USB activity"
    )

    # Convert investigation records into readable text
    if isinstance(activity_details, dict):
        records = activity_details
    else:
        records = {"Investigation Records": str(activity_details)}

    recorded_events = []

    def extract_events(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    extract_events(value)
                else:
                    recorded_events.append(f"{key}: {value}")

        elif isinstance(data, list):
            for item in data:
                extract_events(item)

    extract_events(records)

    facts = "\n".join(
        f"- {event}" for event in recorded_events
    ) if recorded_events else "Not available in the records."

    # Lightweight investigation explanation
    explanation = f"""
RECORDED FACTS

The investigation contains the following recorded information:
{facts}

TIMELINE ANALYSIS

The events are presented using the timestamps available in the investigation records.
No missing timestamps or event sequences have been assumed.

INVESTIGATION OBSERVATIONS

The records should be reviewed for unusual login activity, sensitive file access,
and USB device connections. These events may require further investigation.

LIMITATIONS

A USB connection alone does not prove that files were copied.
The available records cannot independently establish a person's intention or guilt.

CONCLUSION

The investigation results provide information for further forensic review.
All findings should be verified against the original evidence records.

KNOWLEDGE BASE

{context}
"""

    return explanation.strip()


if __name__ == "__main__":

    sample_activity = {
        "user": "demo",
        "event": "login_success",
        "timestamp": "09:02"
    }

    print("Generating forensic explanation...")

    result = generate_rag_explanation(sample_activity)

    print("\nFORENSIC EXPLANATION\n")
    print(result)
