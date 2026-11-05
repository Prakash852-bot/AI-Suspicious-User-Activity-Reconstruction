
from rag_engine import retrieve_context



from rag_engine import retrieve_context


def generate_rag_explanation(activity_details):

    context = retrieve_context(
        "digital forensics suspicious login sensitive file USB activity"
    )

    records = activity_details if isinstance(activity_details, dict) else {}

    timeline = records.get("timeline", [])

    if hasattr(timeline, "to_dict"):
        timeline = timeline.to_dict(orient="records")

    if not isinstance(timeline, list):
        timeline = []

    # Create short event summaries
    event_lines = []

    for event in timeline:
        if not isinstance(event, dict):
            continue

        timestamp = event.get("timestamp", "Time unavailable")
        user = event.get("user", "Unknown user")
        action = event.get("action", "Unknown action")
        obj = event.get("object", "")

        event_text = f"- {timestamp} | {user} | {action}"

        if obj:
            event_text += f" | {obj}"

        event_lines.append(event_text)

    facts = "\n".join(event_lines) if event_lines else \
        "- No timeline events available."

    explanation = f"""
RECORDED FACTS

- Total recorded events: {len(timeline)}
- Investigation data is summarized below.

TIMELINE ANALYSIS

{facts}

INVESTIGATION OBSERVATIONS

- Review unusual login activity and sensitive file access.
- Examine USB connections and related events.
- Correlated activities require further investigation.

LIMITATIONS

- USB connection alone does not prove file copying.
- Available records cannot establish intention or guilt.

CONCLUSION

Findings are investigation leads and must be verified
against the original digital evidence.

KNOWLEDGE BASE

{str(context)[:500]}
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
