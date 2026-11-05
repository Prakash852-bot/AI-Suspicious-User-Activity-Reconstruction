
from rag_engine import retrieve_context


def generate_rag_explanation(activity_details):

    context = retrieve_context(
        "digital forensics suspicious login sensitive file USB activity"
    )

    # Convert investigation records into a dictionary
    if isinstance(activity_details, dict):
        records = activity_details
    else:
        records = {"Investigation Records": activity_details}

    recorded_events = []

    def extract_events(data, parent=""):
        if isinstance(data, dict):
            for key, value in data.items():
                current_key = f"{parent} {key}".strip()

                if isinstance(value, dict):
                    extract_events(value, current_key)

                elif isinstance(value, list):
                    for index, item in enumerate(value, start=1):
                        extract_events(item, f"{current_key} {index}")

                else:
                    recorded_events.append(
                        f"{current_key}: {value}"
                    )

        elif isinstance(data, list):
            for index, item in enumerate(data, start=1):
                extract_events(item, f"{parent} {index}")

        else:
            recorded_events.append(f"{parent}: {data}")

    extract_events(records)

    facts = "\n".join(
        f"- {event}" for event in recorded_events
    ) if recorded_events else "- No recorded information available."

    explanation = f"""
RECORDED FACTS

The investigation contains the following recorded information:

{facts}


TIMELINE ANALYSIS

- Events are organized using the timestamps available in the investigation records.
- The recorded sequence is presented without assuming missing events.
- Time differences are included only when available in the source records.


INVESTIGATION OBSERVATIONS

- Review successful and failed login activities.
- Examine sensitive file access records.
- Review USB device connection records.
- Correlate related events within the available time window.
- Verify suspicious activity against the original evidence.


LIMITATIONS

- A USB connection alone does not prove that files were copied.
- The available records cannot independently establish a person's intention or guilt.
- All findings require verification using original evidence.


CONCLUSION

The investigation provides potential leads for further forensic examination.

All findings should be reviewed and verified before reaching a final conclusion.


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
